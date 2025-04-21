from mneia_isbn.utils.conversion import isbn10_to_isbn13, isbn13_to_isbn10
from mneia_isbn.utils.validation import (
    calculate_check_digit,
    calculate_isbn10_check_digit,
    calculate_isbn13_check_digit,
    validate,
)


def clean(source: str) -> str:
    """
    Removes all non alphanumeric characters from an ISBN, such as whitespace and dashes, and converts it to uppercase.
    """
    return "".join([character.upper() for character in source if character.isalnum()])


__all__ = [
    "clean",
    "isbn10_to_isbn13",
    "isbn13_to_isbn10",
    "calculate_check_digit",
    "calculate_isbn10_check_digit",
    "calculate_isbn13_check_digit",
    "validate",
]
