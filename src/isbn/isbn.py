from typing import Optional

from isbn.exceptions import ISBNInvalidOperation, ISBNValidationError
from isbn.mixins import DundersMixin, PartsMixin, PresentationMixin


class ISBN(DundersMixin, PresentationMixin, PartsMixin):
    def __init__(self, source: str):
        self._source: str = self.clean(source)
        self._is_valid: Optional[bool] = None

    @property
    def source(self) -> str:
        """
        Getter for the `_source` property.
        """
        return self._source

    @source.setter
    def source(self, value: str) -> None:
        """
        Setter for the `source` property. When we set the `source`, we need to invalidate some cached variables that may
        have been previously calculated.

        Set validity to `None` when changing the value of `source`. This is fairly shallow, because nothing stops the
        user from setting `_is_valid` to anything and bypassing this invalidation. But who does that anyway... right?
        """
        _value = self.clean(value)
        if _value != self._source:
            self._is_valid = None
        self._source = _value

    @property
    def is_valid(self) -> bool:
        if self._is_valid is None:
            try:
                self.validate()
            except ISBNValidationError:
                self._is_valid = False
            else:
                self._is_valid = True
        return self._is_valid

    @is_valid.setter
    def is_valid(self, _: bool) -> None:
        raise ISBNInvalidOperation("'is_valid' is a read-only property, it cannot be set")

    def clean(self, source: str) -> str:
        """Removes whitespace and dashes from the input, and converts it to uppercase."""
        _source = [character for character in source if not character.isspace()]  # remove spaces and tabs
        _source = [character for character in _source if not character == "-"]  # remove hyphenation
        return "".join(_source).upper()

    def validate(self) -> None:
        """
        TODO: Wire the "calculate_isbn" method here.
        """
        if len(self.source) not in [10, 13]:
            raise ISBNValidationError(
                f"The length of {self.source} is neither 10 nor 13, got length {len(self.source)}."
            )
