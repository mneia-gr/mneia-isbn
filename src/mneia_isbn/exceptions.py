class ISBNInvalidOperation(Exception):
    pass


class ISBNError(Exception):
    pass


class ISBNInvalidLength(Exception):
    """Exception raised when the input is neither 10 nor 13 characters long."""

    pass


class ISBNInvalidPrefix(Exception):
    """Exception raised when the prefix of an ISBN13 is neither 978 nor 979."""

    pass


class ISBNInvalidCheckDigit(Exception):
    """Exception raised when the check digit of an ISBN is wrong."""

    pass
