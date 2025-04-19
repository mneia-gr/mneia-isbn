import pytest

from isbn import ISBN, ISBNInvalidOperation


@pytest.mark.parametrize(
    "source, as_isbn13",
    [
        ("1781682135", "9781781682135"),
        ("9781234567890", "9781234567890"),
    ],
)
def test_isbn_as_isbn13(source, as_isbn13):
    isbn = ISBN(source)
    assert isbn.as_isbn13 == as_isbn13


@pytest.mark.parametrize(
    "source, as_isbn10",
    [
        ("1781682135", "1781682135"),
        ("9789607073013", "9607073010"),
    ],
)
def test_as_isbn10(source, as_isbn10):
    isbn = ISBN(source)
    assert isbn.as_isbn10 == as_isbn10


def test_as_isbn10_raises():
    isbn = ISBN("9791234567890")
    with pytest.raises(ISBNInvalidOperation) as exc:
        isbn.as_isbn10
    assert str(exc.value) == "Cannot convert ISBN13 that starts with 979 to ISBN10."
