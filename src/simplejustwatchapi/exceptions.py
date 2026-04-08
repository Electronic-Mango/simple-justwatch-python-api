"""
Exceptions raised by this library.

All exceptions inherit from [`JustWatchError`]
[simplejustwatchapi.exceptions.JustWatchError] for easier catching.

Specific exceptions are raised for non-`2xx` HTTP response status codes and GraphQL
API response errors.

Each exception includes relevant information for why it was raised, but not always in
any particular parsed format. For example, [`JustWatchApiError`]
[simplejustwatchapi.exceptions.JustWatchApiError] includes the list of errors from the
API response, but stored as a `dict`/JSON, as it was received from the API.

"""


class JustWatchError(Exception):
    """Common parent for all exceptions raised by this library."""


class JustWatchApiError(JustWatchError):
    """
    Raised when JustWatch API returned errors in JSON response.

    If this error is raised, then API responded with status code `2xx`, but there are
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
    Raised when JustWatch API returned a non-`2xx` status code.

    Any additional verification is not performed, ony the status code is checked.

    Attributes:
        code (int): HTTP status code returned by the API.
        message (str): HTTP message response from the API.

    """

    def __init__(self, code: int, message: str) -> None:
        """Init JustWatchHttpError with status code and message from response."""
        super().__init__(f"HTTP code {code}: {message}")
        self.code = code
        self.message = message
