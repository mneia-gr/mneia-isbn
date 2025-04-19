import pytest

from isbn.exceptions import ISBNInvalidOperation
from isbn.utils.check_digit import calculate_isbn10_check_digit, calculate_isbn13_check_digit


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
