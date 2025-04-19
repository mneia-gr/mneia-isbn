import pytest

from isbn import ISBN


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
