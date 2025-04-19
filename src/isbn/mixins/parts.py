from typing import Optional

from isbn import ISBNError
from isbn.constants.ranges import RANGES


class PartsMixin:
    _prefix: Optional[str]
    source: str

    @property
    def prefix(self) -> str:
        if self._prefix is None:
            self._prefix = "978" if len(self.source) == 10 else self.source[:3]
        return self._prefix

    @property
    def group(self) -> str:
        rest_after_prefix = self.source if len(self.source) == 10 else self.source[3:]
        for group in RANGES[self.prefix]:
            if rest_after_prefix.startswith(group):
                return group
        raise ISBNError(f"Could not find the Group of ISBN {self.source}.")

    @property
    def publisher(self) -> str:
        length_before_publisher = len(self.group) if len(self.source) == 10 else len(self.group) + 3
        rest_after_group = self.source[length_before_publisher:]
        publisher_ranges = RANGES[self.prefix][self.group]["ranges"]
        for publisher_range in publisher_ranges:
            publisher_min, publisher_max = publisher_range
            publisher = rest_after_group[: len(publisher_min)]
            if int(publisher) in range(int(publisher_min), int(publisher_max) + 1):
                return publisher
        raise ISBNError(f"Could not find the Publisher of ISBN {self.source}.")

    @property
    def article(self) -> str:
        length_before_article = len(self.group) + len(self.publisher)
        length_before_article = length_before_article if len(self.source) == 10 else length_before_article + 3
        return self.source[length_before_article:-1]
