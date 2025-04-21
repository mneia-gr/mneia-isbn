# ISBN #

**isbn** is a collection of tools for working with International Standard Book Numbers in Python. It can validate,
hyphenate, and convert ISBNs between formats.

This library is inspired by, and partially ported from, the [isbn3](https://github.com/inventaire/isbn3) Javascript
library. This library has no runtime dependencies outside of the Python standard library. It has dependencies for
building, testing, and parsing XML, but none of those are needed for runtime, nor are they installed with the library.

## Usage ##

Import and create an ISBN instance:

```python
from isbn import ISBN

isbn = ISBN("9789605031114")
```

### Properties ###

#### Validation ####

The `is_valid` property returns either `True` or `False`. You can get similar results with the `validate()` utility,
documented later in this document.

```python
isbn.is_valid  # returns True or False
```

#### Prefix, Group, Publisher, Article, and Check Digit ####

An ISBN10 can be divided in a Group, a Publisher, an Article and a Check Digit. An ISBN13 additionally has a Prefix.

```python
isbn = ISBN("9789605031114")
isbn.prefix  # returns '978'
isbn.group  # returns '960'
isbn.publisher  # returns '503'
isbn.article  # returns '111'
isbn.check_digit  # returns '4'
```

You can also get the Group name, as defined by ISBN International:

```python
isbn.group_name  # returns 'Greece'
```

The Check Digit is available for both the ISBN10 and ISBN13 formats of an ISBN:

```python
isbn = ISBN("9789605031114")
isbn.check_digit_10  # returns '6'
isbn.check_digit_13  # returns '4'
```

#### Conversions ####

All ISBN10s can be converted to ISBN13s. All ISBN13 that start with "978" can be converted to ISBN10s:

```python
isbn = ISBN("9789605031114")
isbn.as_isbn10  # returns '9605031116'

isbn = ISBN("960236727X")
isbn.as_isbn13  # returns '9789602367278'

isbn = ISBN("9798531132178")
isbn.as_isbn10  # returns None, conversion is not possible
```

#### Hyphenation ####

You can get hyphenated representations of an ISBN:

```python
isbn = ISBN("9789605031114")
isbn.hyphenated  # returns '978-960-503-111-4'
isbn.as_isbn10_hyphenated  # returns '960-503-111-6'
isbn.as_isbn13_hyphenated  # returns '978-960-503-111-4'
```

#### Dictionary Representation ####

There is a dictionary representation that includes all the properties:

```python
isbn = ISBN("9789605031114")
isbn.as_dict
```

Returns:

```python
{
    'group': '960',
    'group_name': 'Greece',
    'publisher': '503',
    'article': '111',
    'check_digit': '4',
    'check_digit_10': '6',
    'check_digit_13': '4',
    'source': '9789605031114',
    'prefix': '978',
    'hyphenated': '978-960-503-111-4',
    'is_isbn10': False,
    'is_isbn13': True,
    'as_isbn10': '9605031116',
    'as_isbn13': '9789605031114',
    'as_isbn10_hyphenated': '960-503-111-6',
    'as_isbn13_hyphenated': '978-960-503-111-4',
    'is_valid': True
}
```

### Utilities ###

There are few utility functions that you can use. You can convert ISBN10 to ISBN13 and back:

```python
from isbn.utils import isbn10_to_isbn13, isbn13_to_isbn10

isbn10_to_isbn13("960236727X")  # returns: '9789602367278'

isbn13_to_isbn10("9789602367278")  # returns: '960236727X'

isbn13_to_isbn10("9798531132178")  # raises: ISBNInvalidOperation: Cannot convert ISBN13 that starts with 979 to ISBN10.
```

You can calculate check digits:

```python
from isbn.utils import calculate_check_digit, calculate_isbn10_check_digit, calculate_isbn13_check_digit

calculate_check_digit("979853113217?")  # returns '8'

calculate_isbn10_check_digit("960236727?")  # returns 'X'

calculate_isbn13_check_digit("979853113217?")  # returns '8'

calculate_isbn10_check_digit("123456789")  # raises ISBNInvalidOperation: Cannot calculate check digit for ISBN10 because 123456789 is not 10 digits long.

calculate_isbn13_check_digit("123456789012")  # raises ISBNInvalidOperation: Cannot calculate check digit for ISBN13 because 123456789012 is not 13 digits long.
```

Finally, you can validate an ISBN. This checks the length of the input, and the check digit:

```python
from isbn.utils import validate

validate("960236727X")  # returns None, which means there is no validation issue

validate("9789602367278")  # returns None, which means there is no validation issue

validate("123456789012")  # raises ISBNValidationError: The length of 123456789012 is neither 10 nor 13, got length 12.

validate("9602367270")  # raises ISBNValidationError: The check digit of 9602367270 is not valid, expected check digit X.
```