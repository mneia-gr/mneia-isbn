from typing import Optional

from isbn.exceptions import ISBNInvalidOperation, ISBNValidationError
from isbn.mixins import DundersMixin


class ISBN(DundersMixin):
    def __init__(self, source: str):
        self._source: str = self.clean(source)
        self._is_valid: Optional[bool] = None
        self._prefix: Optional[str] = None

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
            self._prefix = None
        self._source = _value

    @property
    def prefix(self) -> str:
        if self._prefix is None:
            self._prefix = "978" if len(self) == 10 else self.source[:3]
        return self._prefix

    # @property
    # def as_isbn13(self) -> str:
    #     """
    #     TODO: Commented out for now, this needs to recalculate the check digit if "978" is prefixed to an ISBN10.
    #     """
    #     return self.source if len(self) == 13 else f"978{self.source}"

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

    def calculate_check_digit(self) -> str:
        if len(self) == 10:
            return self.calculate_isbn10_check_digit()
        if len(self) == 13:
            return self.calculate_isbn13_check_digit()
        raise ISBNInvalidOperation(f"The length of {self.source} is neither 10 nor 13, got length {len(self)}.")

    def calculate_isbn10_check_digit(self) -> str:
        """
        The check digit in an ISBN10 is whatever number needs to be added to the sum of the products of the first 9
        digits by their weight, so that the total is a multiple of 11. The weight of digits starts from 10 and declines
        by 1 for each subsequent digit. The letter "X" is used if the calculated check digit is 10.
        """
        if len(self) != 10:
            raise ISBNInvalidOperation(
                f"Cannot calculate check digit for ISBN10 because {self.source} is not 10 digits long."
            )
        sum_of_weighted_digits = sum([int(digit) * (10 - index) for index, digit in enumerate(self.source[:-1])])
        check_digit = (11 - sum_of_weighted_digits % 11) % 11
        return str(check_digit) if check_digit != 10 else "X"

    def calculate_isbn13_check_digit(self) -> str:
        """
        The check digit in an ISBN13 is whatever number needs to be added to the sum of the products of the first 12
        digits by their weight, so that the total is a multiple of 10. The weight of digits is swaps between 1 and 3,
        i.e. 1 for digits in odd positions in the ISBN and 3 for digits in even positions in the ISBN.
        """
        if len(self) != 13:
            raise ISBNInvalidOperation(
                f"Cannot calculate check digit for ISBN13 because {self.source} is not 13 digits long."
            )
        sum_of_weighted_digits = sum([int(digit) for digit in self.source[:-1:2]]) + sum(
            [int(digit) * 3 for digit in self.source[1:-1:2]]
        )
        return str((10 - sum_of_weighted_digits % 10) % 10)
