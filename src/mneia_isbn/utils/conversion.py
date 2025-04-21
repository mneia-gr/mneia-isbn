from mneia_isbn import ISBNInvalidOperation
from mneia_isbn.utils.validation import calculate_isbn10_check_digit, calculate_isbn13_check_digit


def isbn10_to_isbn13(source: str) -> str:
    """
    Any ISBN10 can be converted to ISBN13 by prefixing it with "978" and recalculating the check digit."
    """
    if len(source) == 13:
        return source
    isbn13 = f"978{source}"
    isbn13 = isbn13[:-1] + calculate_isbn13_check_digit(isbn13)
    return isbn13


def isbn13_to_isbn10(source: str) -> str:
    """
    Any ISBN13 that starts with "978" can be converted to ISBN10 by removing the "978" prefix and recalculating the
    check digit. ISBN13s that start with "979" cannot be converted to ISBN10.
    """
    if len(source) == 10:
        return source
    if source.startswith("979"):
        raise ISBNInvalidOperation("Cannot convert ISBN13 that starts with 979 to ISBN10.")
    isbn10 = source[3:]
    isbn10 = isbn10[:-1] + calculate_isbn10_check_digit(isbn10)
    return isbn10
