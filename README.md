# ISBN #

**isbn** is a collection of tools for working with International Standard Book Numbers in Python. It can validate,
hyphenate, and convert ISBNs between formats.

## Usage ##

Import and create an ISBN instance:

```python
from isbn import ISBN

isbn = ISBN("9789605031114")
```

### Validation ###

You can check the validity of an ISBN using either the `is_valid` property, or the `validate()` method. The `is_valid`
property returns either `True` or `False`, whereas the `validate()` method raises an exception if the ISBN is not valid.
Examples:

```python
isbn = ISBN("9789605031114")
isbn.is_valid  # returns True

isbn = ISBN("ABC")
isbn.is_valid  # returns False
```
