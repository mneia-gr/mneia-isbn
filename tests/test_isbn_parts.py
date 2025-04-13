import pytest

from isbn import ISBN


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
