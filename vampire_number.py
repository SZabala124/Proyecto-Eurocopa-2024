def combination(elements, m, combination_temp=None, index=0, result=None):
    """
    Generate a combination list of m elements from a list of n elements.

    Args:
        elements (list): the list of elements.
        m (int): the number of elements in every combination.
        combination_temp (list): a temp combination.
        index(int): The actual index.
        result(list): one of the combination.

    Returns:
        list: the combination of m elements of element list.
    """
    if result is None:  # for the first call of the recursive function
        result = []
    if combination_temp is None:  # for the first call of the recursive function
        combination_temp = []
    if len(combination_temp) == m:
        result.append(combination_temp)
        return
    for i in range(index, len(elements)):
        combination_temp.append(elements[i])
        combination(elements, m, combination_temp[:], i + 1, result)
        combination_temp.pop()
    return result


def permutation(elements, temp_permutation=None, result=None):
    """Generates a permutation list from the given elements.

    Args:
        elements (list): the list of elements to make the permutation.
        temp_permutation (list): the temporary permutation.
        result (list): one of the permutation.

    Returns:
        list: the permutation of the elements in the list.
    """
    if result is None:
        result = []
    if temp_permutation is None:
        temp_permutation = []
    if not elements:
        result.append(temp_permutation.copy())
        return
    for i, element in enumerate(elements):
        temp_permutation.append(element)
        tmp_elements = elements.copy()
        tmp_elements.pop(i)
        permutation(tmp_elements, temp_permutation, result)
        temp_permutation.pop()
    return result


def remove_duplicates(elements):
    """Remove duplicates from a list of elements.

    Args:
        elements (list): The list of elements.

    Returns:
        list: a list of elements without duplicates.
    """
    new_list = []
    for item in elements:
        item_set = set(item)
        found = False
        for new_item in new_list:
            new_item_set = set(new_item)
            if item_set == new_item_set:
                found = True
                break
        if not found:
            new_list.append(item)
    return new_list


def get_fang_digits_pairs(digits):
    """Returns the pairs of possible digits for the fangs.

    Args:
        digits (list): a list of digits for be used to generate the fangs digits.

    Raises:
        ValueError: if the number of digits is not even.

    Returns:
        list: pairs of possible fangs digits.
    """
    if len(digits) % 2 != 0:
        raise ValueError("Invalid number of digits.")

    fang_size = len(digits) // 2  # get the fang_size
    fangs = combination(digits, fang_size)  # posible combination of digits of the fangs size
    fangs = remove_duplicates(fangs)  # remove duplicates, due to duplicates digits.
    fang_digits_pairs = []
    for fang in fangs:
        other_fang_digits = digits.copy()  # create a copy of the digits and then remove the digits of the found fang
        for digit in fang:
            other_fang_digits.remove(digit)
        fang_digits_pairs.append([fang, other_fang_digits])  # So the other fang should be made with this digits.
    return fang_digits_pairs


def vampire_number(number, all_fangs=False):
    """Return a pair of fangs, if the number is a vampire number, else return None.

    Args:
        number (int|str): The number to check if it is a vampire number.
        all_fangs (bool): if True, return all the possible fangs, else return only one.

    Returns:
        list|None: a list of two ints(fangs) if the number is a vampires number or None otherwise.
    """
    if not isinstance(number, (int, str)):
        raise TypeError("Invalid number")
    if isinstance(number, str):
        if not number.isdigit():
            raise ValueError("Invalid number")
        number = int(number)

    digits = [digit for digit in str(number)]  # getting all the digits of the number
    if len(digits) % 2 != 0:
        return None  # if the number of digits is not even, it couldn't be a vampire number

    fang_digits_pairs = get_fang_digits_pairs(digits)  # getting the digits for generate the fangs.

    if all_fangs:
        all_fangs_pairs = []

    for fangs_digits in fang_digits_pairs:  # the fangs will be made by permuting the digits
        fang1_permutations = permutation(fangs_digits[0])
        fang2_permutations = permutation(fangs_digits[1])
        for fang1 in fang1_permutations:
            if int(fang1[0]) == 0:  # the fang could not start with 0
                continue
            fang1 = "".join(fang1)  # joining to get a str of the fang
            for fang2 in fang2_permutations:
                if int(fang2[0]) == 0:  # the fang could not start with 0
                    continue
                if int(fang1[-1]) == 0 and int(fang2[-1]) == 0:  # both fangs couldn't ends with 0
                    continue
                fang2 = "".join(fang2)  # joining to get a str of the fang
                if int(fang1) * int(fang2) == number:  # if True, is a vampire number!!!
                    if not all_fangs:
                        return [int(fang1), int(fang2)]
                    all_fangs_pairs.append([int(fang1), int(fang2)])
    if all_fangs and all_fangs_pairs:
        all_fangs_pairs = remove_duplicates(all_fangs_pairs)
        return all_fangs_pairs
    return None


if __name__ == "__main__":

    def main():
        import os

        list_of_vampires_number = [
            1260,
            1395,
            1435,
            1530,
            1827,
            2187,
            6880,
            102510,
            104260,
            105210,
            105264,
            105750,
            108135,
            110758,
            115672,
            116725,
            117067,
            118440,
            120600,
            123354,
            124483,
            125248,
            125433,
            125460,
            125500,
        ]
        numbers = [i for i in range(0, 125501)]
        vampires = []

        os.system("cls")
        for number in numbers:
            answer = vampire_number(number)
            if answer:
                vampires.append([number, answer])

        print("Vampires returning just one pair of fangs...")
        print(vampires)
        vampire_numbers = [item[0] for item in vampires]
        if list_of_vampires_number != vampire_numbers:
            print("No nos dio!!!!")
        else:
            print("Exito total!!!")
        print(len(vampires))
        print("------------------------------------------------")

        vampires = []
        for number in numbers:
            answer = vampire_number(number, True)
            if answer:
                vampires.append([number, answer])

        print("Vampires returning all pairs of fangs...")
        print(vampires)
        vampire_numbers = [item[0] for item in vampires]
        if list_of_vampires_number != vampire_numbers:
            print("No nos dio!!!!")
        else:
            print("Exito total!!!")
        print(len(vampires))

    # tmp = combination([1, 2, 3, 4, 5, 6, 7, 8], 2)
    # print(tmp)
    # print(len(tmp))
    # tmp = permutation([1, 2, 3, 4, 5])
    # print(tmp)
    # print(len(tmp))
    main()
