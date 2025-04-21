from isbn import ISBN


def test_isbn_str():
    isbn = ISBN("foo")
    assert str(isbn) == "FOO"


def test_isbn_repr():
    isbn = ISBN("bar")
    assert repr(isbn) == "<ISBN: BAR>"


def test_isbn_len():
    isbn = ISBN("foobar")
    assert len(isbn) == 6
