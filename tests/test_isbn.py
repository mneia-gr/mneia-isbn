from unittest import mock

import pytest

from mneia_isbn import ISBN, ISBNInvalidCheckDigit, ISBNInvalidLength, ISBNInvalidPrefix


@mock.patch("mneia_isbn.isbn.clean", return_value="foo")
def test_isbn_init(mock_clean):
    """
    Test that the input is "cleaned" upon class instantiation.
    """
    isbn = ISBN("bar")
    mock_clean.assert_called_once_with("bar")
    assert isbn.source == "foo"


@mock.patch("mneia_isbn.isbn.validate", return_value=None)
def test_isbn_is_valid(mock_validate):
    isbn = ISBN("foo")
    assert isbn.is_valid is True
    mock_validate.assert_called_once_with("FOO")


@pytest.mark.parametrize(
    "side_effect",
    [
        (ISBNInvalidCheckDigit),
        (ISBNInvalidLength),
        (ISBNInvalidPrefix),
    ],
)
@mock.patch("mneia_isbn.isbn.validate")
def test_isbn_is_not_valid(mock_validate, side_effect):
    mock_validate.side_effect = side_effect

    isbn = ISBN("foo")
    assert isbn.is_valid is False
    mock_validate.assert_called_once_with("FOO")
