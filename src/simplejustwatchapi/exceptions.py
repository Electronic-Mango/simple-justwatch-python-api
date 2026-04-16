"""
Exceptions raised by this library.

All exceptions inherit from [`JustWatchError`]
[simplejustwatchapi.exceptions.JustWatchError] for easier catching.

Specific exceptions are raised for HTTP-related errors and GraphQL API response errors.
"""


class JustWatchError(Exception):
    """Common parent for all exceptions raised by this library."""


class JustWatchApiError(JustWatchError):
    """
    Raised when JustWatch API returned errors in JSON response.

    If this error is raised, then no HTTP-related error occurred, but there are
    listed errors in the internal JSON response. It can happen for too high complexity
    of request, invalid node ID in functions like [`details`]
    [simplejustwatchapi.justwatch.details], or invalid country or language codes.

    Attributes:
        errors (list[dict]): List of all errors in the JSON response from the API.
            The `dict` elements are themselves basic JSONs, each with at least two
            keys - `message` and `code`.

    """

    def __init__(self, errors: list[dict]) -> None:
        """Init JustWatchApiError with internal errors from JSON response."""
        super().__init__(f"Errors in JSON response: {errors}")
        self.errors = errors


class JustWatchHttpError(JustWatchError):
    """
    Raised when HTTP-related error occurs.

    This is a general exception for any HTTP-related errors, such as non-`2xx` status
    codes, network errors, timeouts, etc.

    Attributes:
        msg (str): Error message describing the HTTP error.
        response (str | None): Optional text of the HTTP response, if available.
            Usucally contains JSON with error responses from the API.

    """

    def __init__(self, msg: str, response: str | None = None) -> None:
        """Init JustWatchHttpError with error message and optional response text."""
        super().__init__(msg)
        self.response = response
