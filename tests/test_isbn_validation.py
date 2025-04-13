import pytest

from isbn import ISBN, ISBNInvalidOperation, ISBNValidationError


def test_isbn_is_valid_cannot_be_set():
    """
    The `is_valid` property is read-only, and should not be able to set.
    """
    isbn = ISBN("9789605031114")

    with pytest.raises(ISBNInvalidOperation) as exc:
        isbn.is_valid = False
    assert str(exc.value) == "'is_valid' is a read-only property, it cannot be set"


@pytest.mark.parametrize(
    "source, expected",
    [
        ("123", False),  # too short
        ("123456789X", True),
    ],
)
def test_isbn_is_valid(source, expected):
    isbn = ISBN(source)
    assert isbn.is_valid is expected


@pytest.mark.parametrize(
    "source, message",
    [
        ("123", "The length of 123 is neither 10 nor 13, got length 3."),  # too short
    ],
)
def test_isbn_validate_raises(source, message):
    """Test that the correct exception is raised for invalid ISBNs."""
    isbn = ISBN(source)
    with pytest.raises(ISBNValidationError) as exc:
        isbn.validate()
    assert str(exc.value) == message
