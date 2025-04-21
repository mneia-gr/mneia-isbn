from unittest import mock

from isbn import ISBN, ISBNValidationError


@mock.patch("isbn.isbn.clean", return_value="foo")
def test_isbn_init(mock_clean):
    """
    Test that the input is "cleaned" upon class instantiation.
    """
    isbn = ISBN("bar")
    mock_clean.assert_called_once_with("bar")
    assert isbn.source == "foo"


@mock.patch("isbn.isbn.validate", return_value=None)
def test_isbn_is_valid(mock_validate):
    isbn = ISBN("foo")
    assert isbn.is_valid is True
    mock_validate.assert_called_once_with("FOO")


@mock.patch("isbn.isbn.validate", side_effect=ISBNValidationError)
def test_isbn_is_not_valid(mock_validate):
    isbn = ISBN("foo")
    assert isbn.is_valid is False
    mock_validate.assert_called_once_with("FOO")
