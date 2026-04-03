"""
Exception definitions raised by this library.

All exceptions inherit from [`JustWatchError`]
[simplejustwatchapi.exceptions.JustWatchError] for easier catching.

Specific exceptions are raised for invalid country codes, non-`2xx` HTTP status codes,
GraphQL API response errors.

Each exception includes relevant information for why it was raised, but not always in
any particular parsed format.
For example, [`JustWatchApiError`][simplejustwatchapi.exceptions.JustWatchApiError]
includes the list of errors from the API response, but stored as a `dict`/JSON, as it
was received from the API.

"""


class JustWatchError(Exception):
    """Common parent for all exceptions raised by this library."""


class JustWatchCountryCodeError(JustWatchError):
    """
    Raised when user provided invalid country code.

    Each country code must be exactly 2 characters long, e.g. `US`, `DE`, `GB`.

    JustWatch doesn't report exact standard, or format, other thay 2 characters.
    It seems to match ISO 3166-1 alpha-2 format, but the only verification done by this
    library is length check If the code is 2 characters long, but doesn't match any
    codes JustWatch expected, the [`JustWatchApiError`]
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
        super().__init__(f"Invalid country code: {code}, it must be 2 characters long!")
        self.code = code


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
