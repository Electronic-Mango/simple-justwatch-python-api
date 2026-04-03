"""
Exception definitions raised by this library.

All exceptions inherit from [`JustWatchError`]
[simplejustwatchapi.exceptions.JustWatchError] for easier catching.

Specific exceptions are raised for invalid country codes, invalid language codes,
non-`2xx` HTTP status codes, GraphQL API response errors.

Each exception includes relevant information for why it was raised, but not always in
any particular parsed format. For example, [`JustWatchApiError`]
[simplejustwatchapi.exceptions.JustWatchApiError] includes the list of errors from the
API response, but stored as a `dict`/JSON, as it was received from the API.

"""


class JustWatchError(Exception):
    """Common parent for all exceptions raised by this library."""


class JustWatchHttpError(JustWatchError):
    """
    Raised when JustWatch API returned a non-`2xx` status code.

    Any additional verification is not performed, ony the status code is checked.

    Attributes:
        code (int): HTTP status code returned by the API.
        message (str): HTTP message response from the JustWatch API.

    """

    def __init__(self, code: int, message: str) -> None:
        """
        Init JustWatchHttpError with status code and message from response.

        Args:
            code (int): HTTP status code returned by the API.
            message (str): HTTP message response from the JustWatch API.

        """
        super().__init__(f"HTTP code {code}: {message}")
        self.code = code
        self.message = message


class JustWatchApiError(JustWatchError):
    """
    Raised when JustWatch API returned errors in JSON response.

    If this error is raised, then API responded with status code `2xx`, but there are
    listed errors in the internal JSON response. It can happen for too high complexity
    of request, invalid node ID in functions like [`details`]
    [simplejustwatchapi.justwatch.details], or unexpected country codes, or languages.

    Attributes:
        errors (list[dict]): List of all errors in the JSON response from the API.
            The `dict` elements are themselves basic JSONs, each with at least two
            keys - `message` and `code`.

    """

    def __init__(self, errors: list[dict]) -> None:
        """
        Init JustWatchApiError with internal errors from JSON response.

        Args:
            errors (list[dict]): List of all errors in the JSON response from the API.
                The `dict` elements are themselves basic JSONs, each with at least two
                keys - `message` and `code`.

        """
        super().__init__(f"Errors in JSON response: {errors}")
        self.errors = errors


class JustWatchLocaleError(JustWatchError):
    """Common parent for all locale-related exceptions."""


class JustWatchCountryCodeError(JustWatchLocaleError):
    """
    Raised when user provided invalid country code.

    Each country code must be exactly 2 letters long, e.g. `US`, `DE`, `GB`. The
    expected regex reported by JustWatch is `^[A-Z]{2}`, however this library
    automatically normalizes country codes to uppercase.

    JustWatch doesn't report exact standard, or format, other than expected regex.
    It seems to match ISO 3166-1 alpha-2 standard, but the only verification done by
    this library is done based on expected regex. If the code matches the regex,
    but doesn't match any codes JustWatch expected, the [`JustWatchApiError`]
    [simplejustwatchapi.exceptions.JustWatchApiError] will be raised instead.

    Attributes:
        code (str): Invalid country code which caused this exception.

    """

    def __init__(self, code: str) -> None:
        """
        Init JustWatchCountryCodeError with invalid country code.

        Args:
            code(str): Invalid country code which caused this exception.

        """
        super().__init__(f"Invalid country code: {code}!")
        self.code = code


class JustWatchLanguageCodeError(JustWatchLocaleError):
    """
    Raised when user provided invalid language code.

    Language codes are usually 2 letters long, e.g. `en`, `de`, `fr`, with optional
    suffix. The expected regex reported by JustWatch is `^[a-z]{2}(-[0-9A-Z]+)?$`.
    Unlike [`JustWatchCountryCodeError`]
    [simplejustwatchapi.exceptions.JustWatchCountryCodeError] the language code is not
    normalized by this library, and must be provided in the expected format.

    JustWatch doesn't report exact standard, or format, other than expected regex.
    It seems to match ISO 639-1/IETF BCP 47 standard, but the only verification done by
    this library is done based on expected regex. If the code matches the regex,
    but doesn't match any codes JustWatch expected, the [`JustWatchApiError`]
    [simplejustwatchapi.exceptions.JustWatchApiError] will be raised instead.

    Attributes:
        code (str): Invalid language code which caused this exception.

    """

    def __init__(self, code: str) -> None:
        """
        Init JustWatchLanguageError with invalid language code.

        Args:
            code(str): Invalid language code which caused this exception.

        """
        super().__init__(f"Invalid language code: {code}!")
        self.code = code
