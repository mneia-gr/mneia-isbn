import pytest

from isbn import ISBNInvalidOperation
from isbn.utils.conversion import isbn10_to_isbn13, isbn13_to_isbn10


@pytest.mark.parametrize(
    "source, isbn13",
    [
        ("1781682135", "9781781682135"),
        ("9781234567890", "9781234567890"),
    ],
)
def test_isbn10_to_isbn13(source, isbn13):
    assert isbn10_to_isbn13(source) == isbn13


@pytest.mark.parametrize(
    "source, isbn10",
    [
        ("1781682135", "1781682135"),
        ("9789607073013", "9607073010"),
    ],
)
def test_isbn13_to_isbn10(source, isbn10):
    assert isbn13_to_isbn10(source) == isbn10


def test_isbn13_to_isbn10_raises():
    with pytest.raises(ISBNInvalidOperation) as exc:
        isbn13_to_isbn10("9791234567890")
    assert str(exc.value) == "Cannot convert ISBN13 that starts with 979 to ISBN10."
