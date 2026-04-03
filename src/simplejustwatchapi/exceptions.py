"""Module storing all raised exceptions."""


class JustWatchError(Exception):
    """Common parent for all exceptions raised by this library."""


class JustWatchCountryCodeError(JustWatchError):
    """
    Raise when user provided invalid country code.

    Attributes:
        code (str): Invalid country code which caused this exception.

    """

    def __init__(self, code: str) -> None:
        """Init JustWatchCountryCodeError with invalid country code."""
        super().__init__(f"Invalid country code: {code}, it must be 2 characters long!")
        self.code = code


class JustWatchHttpError(JustWatchError):
    """
    Raise when JustWatch API returned a non-`2xx` status code.

    Attributes:
        code (int): HTTP status code received from API.
        message (str): Message received from API, alongside the non-`2xx` status code.

    """

    def __init__(self, code: int, message: str) -> None:
        """Init JustWatchHttpError with status code and message from response."""
        super().__init__(f"HTTP code {code}: {message}")
        self.code = code
        self.message = message


class JustWatchApiError(JustWatchError):
    """
    Raise when JustWatch API returned errors in JSON response.

    If this error is raised, then API responded with status code `2xx`, but there are
    listed errors in the internal JSON response. It can happen for too high complexity
    of request, or invalid node ID in functions like [`details`]
    [simplejustwatchapi.justwatch.details].

    Attributes:
        errors (list[dict]): List of errors from JSON response. Each dict contain
            at least two keys - "message" and "code".

    """

    def __init__(self, errors: list[dict]) -> None:
        """Init JustWatchApiError with internal errors from JSON response."""
        super().__init__(f"Errors in JSON response: {errors}")
        self.errors = errors
