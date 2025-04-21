import pytest

from mneia_isbn import ISBN


def test_isbn_str():
    isbn = ISBN("foo")
    assert str(isbn) == "FOO"


def test_isbn_repr():
    isbn = ISBN("bar")
    assert repr(isbn) == "<ISBN: BAR>"


def test_isbn_len():
    isbn = ISBN("foobar")
    assert len(isbn) == 6


@pytest.mark.parametrize(
    "source_a, source_b",
    [
        ("1781682135", "9781781682135"),
        ("1781682135", "1781682135"),
        ("9781781682135", "9781781682135"),
    ],
)
def test_isbn_eq(source_a, source_b):
    isbn_a = ISBN(source_a)
    isbn_b = ISBN(source_b)
    assert isbn_a == isbn_b


def test_isbn_not_eq():
    assert ISBN("9781781682135") != 5  # great test bro
    assert ISBN("9781781682135") != ISBN("9781781682133")  # last digit is different
