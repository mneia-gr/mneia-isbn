from unittest import mock

import pytest

from mneia_isbn import ISBN, ISBNError


@pytest.mark.parametrize(
    "source, prefix",
    [
        ("1234567890", None),
        ("9781234567890", "978"),
        ("9791234567890", "979"),
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


@pytest.mark.parametrize(
    "source, name",
    [
        ("9789601234567", "Greece"),
    ],
)
def test_isbn_group_name(source, name):
    isbn = ISBN(source)
    assert isbn.group_name == name


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


@pytest.mark.parametrize(
    "source, article",
    [
        ("9789601655550", "5555"),
        ("9781781682135", "213"),
        ("9607073010", "01"),
        ("960728013X", "13"),
    ],
)
def test_isbn_article(source, article):
    isbn = ISBN(source)
    assert isbn.article == article


@mock.patch("mneia_isbn.isbn.calculate_check_digit", return_value="foo")
def test_isbn_check_digit(mock_calculate_check_digit):
    isbn = ISBN("1234567890")
    assert isbn.check_digit == "foo"
    mock_calculate_check_digit.assert_called_once()
