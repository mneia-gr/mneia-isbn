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
