# Changelog #

## v0.0.3 ##

The generic `ISBNValidationError` exception was replaced with three more informative exceptions:
`ISBNInvalidCheckDigit`, `ISBNInvalidLength`, and `ISBNInvalidPrefix`. Also, a properties for Publisher Prefix and
Publisher Name.

## v0.0.2 ##

Renamed package to make PyPI happy. Added equality check with `__eq__`.

## v0.0.1 ##

First release with basic functionality.
