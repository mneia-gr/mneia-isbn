from unittest import mock

import pytest

from isbn.exceptions import ISBNInvalidOperation, ISBNValidationError
from isbn.utils.validation import (
    calculate_check_digit,
    calculate_isbn10_check_digit,
    calculate_isbn13_check_digit,
    validate,
)


@pytest.mark.parametrize(
    "source",
    [
        ("1234567890"),  # 10 digits long
        ("1234567890123"),  # 13 digits long
    ],
)
@mock.patch("isbn.utils.validation.calculate_isbn13_check_digit", return_value="foo")
@mock.patch("isbn.utils.validation.calculate_isbn10_check_digit", return_value="bar")
def test_calculate_check_digit(mock_calculate_isbn10_check_digit, mock_calculate_isbn13_check_digit, source):
    check_digit = calculate_check_digit(source)
    if len(source) == 10:
        mock_calculate_isbn10_check_digit.assert_called_once()
        mock_calculate_isbn13_check_digit.assert_not_called()
        assert check_digit == "bar"
    else:
        mock_calculate_isbn10_check_digit.assert_not_called()
        mock_calculate_isbn13_check_digit.assert_called_once()
        assert check_digit == "foo"


def test_calculate_check_digit_raises():
    with pytest.raises(ISBNInvalidOperation) as exc:
        calculate_check_digit("123456789")
    assert str(exc.value) == "The length of 123456789 is neither 10 nor 13, got length 9."


@pytest.mark.parametrize(
    "source, check_digit",
    [
        ("960707301?", "0"),
        ("960417129?", "1"),
        ("960849601?", "2"),
        ("960020020?", "3"),
        ("960322138?", "4"),
        ("178168213?", "5"),
        ("960422478?", "6"),
        ("960234986?", "7"),
        ("960777133?", "8"),
        ("960705842?", "9"),
        ("960728013?", "X"),
    ],
)
def test_calculate_isbn10_check_digit(source, check_digit):
    assert calculate_isbn10_check_digit(source) == check_digit


def test_calculate_isbn10_check_digit_raises():
    with pytest.raises(ISBNInvalidOperation) as exc:
        calculate_isbn10_check_digit("123456789")
    assert str(exc.value) == "Cannot calculate check digit for ISBN10 because 123456789 is not 10 digits long."


@pytest.mark.parametrize(
    "source, check_digit",
    [
        ("978960165555?", "0"),
        ("978960782766?", "1"),
        ("978960469169?", "2"),
        ("978960688233?", "3"),
        ("9789605031114", "4"),
        ("978044656826?", "5"),
        ("978960503597?", "6"),
        ("978618808721?", "7"),
        ("978618223026?", "8"),
        ("978960023049?", "9"),
    ],
)
def test_calculate_isbn13_check_digit(source, check_digit):
    assert calculate_isbn13_check_digit(source) == check_digit


def test_calculate_isbn13_check_digit_raises():
    with pytest.raises(ISBNInvalidOperation) as exc:
        calculate_isbn13_check_digit("978960782766")
    assert str(exc.value) == "Cannot calculate check digit for ISBN13 because 978960782766 is not 13 digits long."


def test_validate_fails_for_length():
    with pytest.raises(ISBNValidationError) as exc:
        validate("123")
    assert str(exc.value) == "The length of 123 is neither 10 nor 13, got length 3."


@mock.patch("isbn.utils.validation.calculate_check_digit", return_value="A")
def test_validate_fails_for_check_digit(mock_calculate_check_digit):
    with pytest.raises(ISBNValidationError) as exc:
        validate("1234567890")
    assert str(exc.value) == "The check digit of 1234567890 is not valid, expected check digit A."
    mock_calculate_check_digit.assert_called_once_with("1234567890")
