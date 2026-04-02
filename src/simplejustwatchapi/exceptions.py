"""Module storing all raised exceptions."""


class JustWatchError(Exception):
    """Common parent for all exceptions raised by this library."""


class JustWatchCountryCodeError(JustWatchError):
    """Raise when user provided invalid country code."""

    def __init__(self, code: str) -> None:
        """Init JustWatchCountryCodeError with invalid country code."""
        super().__init__(f"Invalid country code: {code}, it must be 2 characters long!")
        self.code = code


class JustWatchHttpError(JustWatchError):
    """Raise when JustWatch API returned a non-2xx status code."""


class JustWatchApiError(JustWatchError):
    """
    Raise when JustWatch API returned errors in JSON response.

    If this error is raised, then API responded with status code 2xx, but there are listed errors
    in the internal JSON response.
    """


class JustWatchTooHighComplexityError(JustWatchApiError):
    """
    Raise when JustWatch API responded with too high complexity error.

    This specifically means that API returned status code 2xx, but the query result would be too
    complex for JustWatch API to handle. Usually caused by :func:`search` or :func:`popular` with
    too high value of ``count``.
    """
