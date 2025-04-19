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


@pytest.mark.parametrize(
    "source, publisher",
    [
        ("9789601655550", "16"),
        ("9781781682135", "78168"),
        ("9607073010", "7073"),
    ],
)
def test_isbn_publisher(source, publisher):
    isbn = ISBN(source)
    assert isbn.publisher == publisher


def test_isbn_publisher_raises():
    isbn = ISBN("9786328004567")  # there is no publisher that starts with 8 in group 63
    with pytest.raises(ISBNError) as exc:
        isbn.publisher
    assert str(exc.value) == "Could not find the Publisher of ISBN 9786328004567."
