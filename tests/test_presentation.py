from unittest import mock

from isbn import ISBN, ISBNInvalidOperation


@mock.patch("isbn.isbn.isbn10_to_isbn13", return_value="foo")
def test_as_isbn13(mock_isbn10_to_isbn13):
    isbn = ISBN("bar")
    as_isbn13 = isbn.as_isbn13
    mock_isbn10_to_isbn13.assert_called_once_with("BAR")
    assert as_isbn13 == "foo"


@mock.patch("isbn.isbn.isbn13_to_isbn10", return_value="foo")
def test_as_isbn10(mock_isbn13_to_isbn):
    isbn = ISBN("bar")
    as_isbn10 = isbn.as_isbn10
    mock_isbn13_to_isbn.assert_called_once_with("BAR")
    assert as_isbn10 == "foo"


@mock.patch("isbn.isbn.isbn13_to_isbn10", side_effect=ISBNInvalidOperation)
def test_as_isbn10_raises(mock_isbn13_to_isbn):
    isbn = ISBN("bar")
    as_isbn10 = isbn.as_isbn10
    mock_isbn13_to_isbn.assert_called_once_with("BAR")
    assert as_isbn10 is None


def test_hyphenated():
    isbn = ISBN("9789607073013")
    assert isbn.hyphenated == "978-960-7073-01-3"


def test_as_dict_isbn13_978():
    isbn = ISBN("9789607073013")
    assert isbn.as_dict == {
        "source": "9789607073013",
        "prefix": "978",
        "group": "960",
        "group_name": "Greece",
        "publisher": "7073",
        "article": "01",
        "check_digit": "3",
        "check_digit_10": "0",
        "check_digit_13": "3",
        "hyphenated": "978-960-7073-01-3",
        "is_isbn10": False,
        "is_isbn13": True,
        "as_isbn10": "9607073010",
        "as_isbn10_hyphenated": "960-7073-01-0",
        "as_isbn13": "9789607073013",
        "as_isbn13_hyphenated": "978-960-7073-01-3",
        "is_valid": True,
    }


def test_as_dict_isbn13_979():
    isbn = ISBN("9798531132178")
    assert isbn.as_dict == {
        "source": "9798531132178",
        "prefix": "979",
        "group": "8",
        "group_name": "United States",
        "publisher": "5311",
        "article": "3217",
        "check_digit": "8",
        "check_digit_10": None,
        "check_digit_13": "8",
        "hyphenated": "979-8-5311-3217-8",
        "is_isbn10": False,
        "is_isbn13": True,
        "as_isbn10": None,
        "as_isbn10_hyphenated": None,
        "as_isbn13": "9798531132178",
        "as_isbn13_hyphenated": "979-8-5311-3217-8",
        "is_valid": True,
    }


def test_as_dict_isbn10():
    isbn = ISBN("9607073010")
    assert isbn.as_dict == {
        "source": "9607073010",
        "prefix": None,
        "group": "960",
        "group_name": "Greece",
        "publisher": "7073",
        "article": "01",
        "check_digit": "0",
        "check_digit_10": "0",
        "check_digit_13": "3",
        "hyphenated": "960-7073-01-0",
        "is_isbn10": True,
        "is_isbn13": False,
        "as_isbn10": "9607073010",
        "as_isbn10_hyphenated": "960-7073-01-0",
        "as_isbn13": "9789607073013",
        "as_isbn13_hyphenated": "978-960-7073-01-3",
        "is_valid": True,
    }


def test_as_isbn10_hyphenated():
    isbn = ISBN("9607073010")
    assert isbn.as_isbn10_hyphenated == "960-7073-01-0"


def test_as_isbn13_hyphenated():
    isbn = ISBN("9789607073013")
    assert isbn.as_isbn13_hyphenated == "978-960-7073-01-3"
