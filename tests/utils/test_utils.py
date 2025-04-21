from mneia_isbn.utils import clean


def test_clean():
    assert clean("123 456-789\tx") == "123456789X"
