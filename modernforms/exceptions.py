"""Modern Forms Exceptions.

These are exceptions that are throw as a result 
of a caught exception from the requests class.
These exceptions boil down all the possible exceptions
from the requests class.
"""


class ModernFormsException(IOError):
    """There was an ambiguous exception that occurred while handling your
    request.
    """

    def __init__(self, *args, **kwargs):
        """Initialize ModernFormsException with `request` and `response` objects."""
        response = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if response is not None and not self.request and hasattr(response, "request"):
            self.request = self.response.request
        super(ModernFormsException, self).__init__(*args, **kwargs)


class ConnectionError(ModernFormsException):
    """A Connection error occurred."""


class Timeout(ModernFormsException):
    """The request timed out."""
