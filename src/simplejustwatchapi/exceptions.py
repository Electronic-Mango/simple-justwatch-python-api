"""Module storing all raised exceptions."""


class JustWatchError(Exception):
    """Common parent for all exceptions raised by this library."""


class JustWatchCountryCodeError(JustWatchError):
    """
    Raised when user provided invalid country code.

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
    of request, or invalid node ID in functions like [`details`]
    [simplejustwatchapi.justwatch.details].

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
