from unittest import mock

import pytest

from isbn import ISBN, ISBNInvalidOperation


@pytest.mark.parametrize(
    "source",
    [
        ("1234567890"),  # 10 digits long
        ("1234567890123"),  # 13 digits long
    ],
)
@mock.patch("isbn.isbn.calculate_isbn13_check_digit")
@mock.patch("isbn.isbn.calculate_isbn10_check_digit")
def test_isbn_calculate_check_digit(mock_calculate_isbn10_check_digit, mock_calculate_isbn13_check_digit, source):
    isbn = ISBN(source)
    isbn.calculate_check_digit()
    if len(source) == 10:
        mock_calculate_isbn10_check_digit.assert_called_once()
        mock_calculate_isbn13_check_digit.assert_not_called()
    else:
        mock_calculate_isbn10_check_digit.assert_not_called()
        mock_calculate_isbn13_check_digit.assert_called_once()


def test_isbn_calculate_check_digit_raises():
    isbn = ISBN("123456789")  # 9 digits
    with pytest.raises(ISBNInvalidOperation) as exc:
        isbn.calculate_check_digit()
    assert str(exc.value) == "The length of 123456789 is neither 10 nor 13, got length 9."
