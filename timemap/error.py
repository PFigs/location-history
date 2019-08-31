"""
    Error

    This module contains the exceptions thrown by
    timemap.

"""

import enum


class ErrorCodes(enum.Enum):
    """ Defines the codes associated with each error"""

    DATE_START = 1
    DATE_END = 2


class Error(Exception):
    """Base class for exceptions in this module."""


class DateStartError(Error):
    """Exception raised when a date is below an expected value."""

    def __init__(self):
        super(DateStartError, self).__init__()
        self.message = "date is below the expected start time"
        self.code = ErrorCodes.DATE_START


class DateEndError(Error):
    """Exception raised when a date is above an expected value."""

    def __init__(self):
        super(DateEndError, self).__init__()
        self.message = "date is above the expected start time"
        self.code = ErrorCodes.DATE_END
