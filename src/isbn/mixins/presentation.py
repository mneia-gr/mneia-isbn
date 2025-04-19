from isbn import ISBNInvalidOperation
from isbn.utils.check_digit import calculate_isbn10_check_digit, calculate_isbn13_check_digit


class PresentationMixin:
    """
    Mix-in functionality, presents ISBN10 as ISBN13, or ISBN13 as ISBN10, or ISBN in hyphenated format.
    """

    source: str
    prefix: str
    group: str
    publisher: str
    article: str
    check_digit: str

    @property
    def as_isbn13(self) -> str:
        """
        Any ISBN10 can be converted to ISBN13 by prefixing it with "978" and recalculating the check digit."
        """
        if len(self.source) == 13:
            return self.source
        _as_isbn13 = f"978{self.source}"
        _as_isbn13 = _as_isbn13[:-1] + calculate_isbn13_check_digit(_as_isbn13)
        return _as_isbn13

    @property
    def as_isbn10(self) -> str:
        """
        Any ISBN13 that starts with "978" can be converted to ISBN10 by removing the "978" prefix and recalculating the
        check digit. ISBN13s that start with "979" cannot be converted to ISBN10.
        """
        if len(self.source) == 10:
            return self.source
        if self.source.startswith("979"):
            raise ISBNInvalidOperation("Cannot convert ISBN13 that starts with 979 to ISBN10.")
        _as_isbn10 = self.source[3:]
        _as_isbn10 = _as_isbn10[:-1] + calculate_isbn10_check_digit(_as_isbn10)
        return _as_isbn10

    @property
    def hyphenated(self) -> str:
        _hyphenated = f"{self.group}-{self.publisher}-{self.article}-{self.check_digit}"
        return _hyphenated if len(self.source) == 10 else f"{self.prefix}-{_hyphenated}"
