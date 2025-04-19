import pytest

from isbn import ISBN, ISBNError


@pytest.mark.parametrize(
    "source, prefix",
    [
        ("1234567890", "978"),
        ("978123456789", "978"),
        ("979123456789", "979"),
    ],
)
def test_isbn_prefix(source, prefix):
    isbn = ISBN(source)
    assert isbn.prefix == prefix


@pytest.mark.parametrize(
    "source, group",
    [
        ("9789601234567", "960"),
    ],
)
def test_isbn_group(source, group):
    isbn = ISBN(source)
    assert isbn.group == group


def test_isbn_group_raises():
    isbn = ISBN("9786101234567")  # there is no group 610
    with pytest.raises(ISBNError):
        isbn.group
