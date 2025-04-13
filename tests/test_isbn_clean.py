from isbn import ISBN


def test_isbn_clean():
    """That that input has any whitespace removed, any dashes removed, and is uppercase."""
    isbn = ISBN("123 456-789\tx")
    assert isbn.source == "123456789X"
