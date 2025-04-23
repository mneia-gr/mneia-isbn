from typing import Any, Dict, Optional

from mneia_isbn.constants import PUBLISHERS, RANGES
from mneia_isbn.exceptions import (
    ISBNError,
    ISBNInvalidCheckDigit,
    ISBNInvalidLength,
    ISBNInvalidOperation,
    ISBNInvalidPrefix,
)
from mneia_isbn.utils import calculate_check_digit, clean, isbn10_to_isbn13, isbn13_to_isbn10, validate


class ISBN:
    def __init__(self, source: str):
        self.source: str = clean(source)

    def __str__(self) -> str:
        return self.source

    def __repr__(self) -> str:
        return f"<ISBN: {self.source}>"

    def __len__(self) -> int:
        return len(self.source)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ISBN):
            return False
        return self.as_isbn13 == other.as_isbn13

    @property
    def is_valid(self) -> bool:
        try:
            validate(self.source)
        except (ISBNInvalidCheckDigit, ISBNInvalidLength, ISBNInvalidPrefix):
            return False
        return True

    @property
    def prefix(self) -> Optional[str]:
        """
        Returns the ISBN prefix. In ISBN13s, the prefix are the first 3 digits. ISBN10s don't have a prefix.
        """
        return self.source[:3] if len(self) == 13 else None

    @property
    def group(self) -> str:
        prefix = self.prefix or "978"  # use 978 as default for ISBN10
        rest_after_prefix = self.source if len(self) == 10 else self.source[3:]
        for group in RANGES[prefix]:
            if rest_after_prefix.startswith(group):
                return group
        raise ISBNError(f"Could not find the Group of ISBN {self.source}.")

    @property
    def group_name(self) -> str:
        prefix = self.prefix or "978"
        return str(RANGES[prefix][self.group]["name"])

    @property
    def publisher(self) -> str:
        prefix = self.prefix or "978"  # use 978 as default for ISBN10
        length_before_publisher = len(self.group) if self.prefix is None else len(self.group) + len(self.prefix)
        rest_after_group = self.source[length_before_publisher:]
        publisher_ranges = RANGES[prefix][self.group]["ranges"]
        for publisher_range in publisher_ranges:
            publisher_min, publisher_max = publisher_range
            publisher = rest_after_group[: len(publisher_min)]
            if int(publisher) in range(int(publisher_min), int(publisher_max) + 1):
                return publisher
        raise ISBNError(f"Could not find the Publisher of ISBN {self.source}.")

    @property
    def publisher_prefix(self) -> str:
        """
        Use this prefix to search for the publisher in the Global Registry of Publishers:

        https://grp.isbn-international.org/
        """
        return f"{self.prefix or '978'}-{self.group}-{self.publisher}"

    @property
    def publisher_name(self) -> str:
        return PUBLISHERS[self.publisher_prefix]

    @property
    def article(self) -> str:
        length_before_article = len(self.group) + len(self.publisher)
        length_before_article = length_before_article if len(self) == 10 else length_before_article + 3
        return self.source[length_before_article:-1]

    @property
    def check_digit(self) -> str:
        return calculate_check_digit(self.source)

    @property
    def is_isbn10(self) -> bool:
        return len(self) == 10

    @property
    def is_isbn13(self) -> bool:
        return len(self) == 13

    @property
    def as_isbn10(self) -> Optional[str]:
        try:
            return isbn13_to_isbn10(self.source)
        except ISBNInvalidOperation:
            return None

    @property
    def as_isbn13(self) -> str:
        return isbn10_to_isbn13(self.source)

    @property
    def as_isbn10_hyphenated(self) -> Optional[str]:
        return None if self.as_isbn10 is None else f"{self.group}-{self.publisher}-{self.article}-{self.as_isbn10[-1]}"

    @property
    def as_isbn13_hyphenated(self) -> str:
        return f"{self.prefix or '978'}-{self.group}-{self.publisher}-{self.article}-{self.as_isbn13[-1]}"

    @property
    def hyphenated(self) -> Optional[str]:
        return self.as_isbn10_hyphenated if self.is_isbn10 else self.as_isbn13_hyphenated

    @property
    def check_digit_10(self) -> Optional[str]:
        return None if self.as_isbn10 is None else self.as_isbn10[-1]

    @property
    def check_digit_13(self) -> str:
        return self.as_isbn13[-1]

    @property
    def as_dict(self) -> Dict[str, Optional[str | bool]]:
        return {
            "group": self.group,
            "group_name": self.group_name,
            "publisher": self.publisher,
            "article": self.article,
            "check_digit": self.check_digit,
            "check_digit_10": self.check_digit_10,
            "check_digit_13": self.check_digit_13,
            "source": self.source,
            "prefix": self.prefix,
            "hyphenated": self.hyphenated,
            "is_isbn10": self.is_isbn10,
            "is_isbn13": self.is_isbn13,
            "as_isbn10": self.as_isbn10,
            "as_isbn13": self.as_isbn13,
            "as_isbn10_hyphenated": self.as_isbn10_hyphenated,
            "as_isbn13_hyphenated": self.as_isbn13_hyphenated,
            "is_valid": self.is_valid,
        }
