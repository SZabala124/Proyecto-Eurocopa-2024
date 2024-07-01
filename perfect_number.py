def dividers(number):
    """Return a list of dividers for the given number.

    Args:
        number (int|str): the number to get the dividers.

    Raises:
        TypeError: if the number is not a str or int.
        ValueError: if the str is not a number.

    Returns:
        list: the list of dividers
    """
    if not isinstance(number, (int, str)):
        raise TypeError("Invalid number")
    if isinstance(number, str):
        if not number.isdigit():
            raise ValueError("Invalid number")
        number = int(number)
    divider_list = []
    for i in range(1, number):
        if number % i == 0:
            divider_list.append(i)
    return divider_list


def is_perfect_number(number):
    """Return True if the number is a perfect number.

    Args:
        number (int|str): the number to check.

    Raises:
        TypeError: if the number is not a str or int.
        ValueError: if the str is not a number.

    Returns:
        bool: True if the number is a perfect number.
    """
    if not isinstance(number, (int, str)):
        raise TypeError("Invalid number")
    if isinstance(number, str):
        if not number.isdigit():
            raise ValueError("Invalid number")
        number = int(number)
    if number <= 0:
        return False
    divider_list = dividers(number)
    if sum(divider_list) == number:
        return True
    return False


if __name__ == "__main__":

    def main():
        import os

        os.system("cls")

        perfect_numbers = [6, 28, 496, 8128]
        number_list = [i for i in range(10000)]
        perfect_number_list = []
        for number in number_list:
            if is_perfect_number(number):
                perfect_number_list.append(number)
        print("Perfect numbers!!")
        print(perfect_number_list)
        if perfect_number_list == perfect_numbers:
            print("Perfecto!")

        number = 33550336
        print(f"The number {number} is perfect? {is_perfect_number(number)}")
        number = 33550338
        print(f"The number {number} is perfect? {is_perfect_number(number)}")

    main()
