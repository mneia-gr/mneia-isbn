from isbn import ISBN


def test_isbn_source_change_causes_invalidation():
    """
    If the `source` input of an `isbn` object changes, its validity should reset to `None`.
    """
    isbn = ISBN("9789605031114")

    assert isbn._is_valid is None  # original value before checking validity is None

    assert isbn.is_valid

    assert isbn._is_valid is True  # after checking the validity, this should not be None

    isbn.source = "123"  # we change the source

    assert isbn._is_valid is None  # so the validity is reset to `None`
