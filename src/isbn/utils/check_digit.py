from isbn.exceptions import ISBNInvalidOperation


def calculate_isbn10_check_digit(source: str) -> str:
    """
    The check digit in an ISBN10 is whatever number needs to be added to the sum of the products of the first 9 digits
    by their weight, so that the total is a multiple of 11. The weight of digits starts from 10 and decrements by 1 for
    each subsequent digit. The letter "X" is used if the calculated check digit is 10.
    """
    if len(source) != 10:
        raise ISBNInvalidOperation(f"Cannot calculate check digit for ISBN10 because {source} is not 10 digits long.")
    sum_of_weighted_digits = sum([int(digit) * (10 - index) for index, digit in enumerate(source[:-1])])
    check_digit = (11 - sum_of_weighted_digits % 11) % 11
    return str(check_digit) if check_digit != 10 else "X"


def calculate_isbn13_check_digit(source: str) -> str:
    """
    The check digit in an ISBN13 is whatever number needs to be added to the sum of the products of the first 12 digits
    by their weight, so that the total is a multiple of 10. The weight of digits is swaps between 1 and 3, i.e. 1 for
    digits in odd positions in the ISBN and 3 for digits in even positions in the ISBN.
    """
    if len(source) != 13:
        raise ISBNInvalidOperation(f"Cannot calculate check digit for ISBN13 because {source} is not 13 digits long.")
    sum_of_weighted_digits = sum([int(digit) for digit in source[:-1:2]]) + sum(
        [int(digit) * 3 for digit in source[1:-1:2]]
    )
    return str((10 - sum_of_weighted_digits % 10) % 10)
