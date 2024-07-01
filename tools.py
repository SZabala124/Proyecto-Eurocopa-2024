import hashlib

from rich import print
from rich.text import Text


def center_text(text, max_num_characters, left_pad_char=" ", right_pad_char=" "):
    """Return a text with padding spaces left and right so the
    given text is centered.

    Args:
        text (str): the text ot be centered.
        max_num_characters (int): the max number of characters
        left_pad_char (str, optional): the character to pad the text. Defaults to " ".
        right_pad_char (str, optional): the character to pad the text. Defaults to " ".

    Raises:
        TypeError: if max_num_characters is not a int.
        TypeError: if text is not a str.
        ValueError: if the len of text couldn't be larger than max_num_characters.
        TypeError: if left_pad_char is not a str.
        TypeError: if right_pad_char is not a str.
        ValueError: if len(left_pad_char)!= 1.
        ValueError: if len(right_pad_char)!= 1.
    Returns:
        str: a str with the text in the center and left and right padding.
    """
    if not isinstance(max_num_characters, int):
        raise TypeError("max_num_characters must be an int")
    if not isinstance(text, (str, Text)):
        raise TypeError("text must be a str or rich.text.Text")
    if len(text) > max_num_characters:
        raise ValueError("The len of text couldn't be larger than max_num_characters")
    if not isinstance(left_pad_char, str):
        raise TypeError("left_pad_char must be a str")
    if not isinstance(right_pad_char, str):
        raise TypeError("right_pad_char must be a str")
    if len(left_pad_char) != 1:
        raise ValueError("left_pad_char must be a single character")
    if len(right_pad_char) != 1:
        raise ValueError("right_pad_char must be a single character")

    total_pad_size = max_num_characters - len(text)
    left_spaces = total_pad_size // 2
    if total_pad_size % 2 == 0:
        right_spaces = left_spaces
    else:
        right_spaces = left_spaces + 1

    if isinstance(text, Text):
        text.pad_left(left_spaces, left_pad_char)
        text.pad_right(right_spaces, right_pad_char)
        return text

    left = f"{left_pad_char * left_spaces}"
    right = f"{right_pad_char * right_spaces}"
    return f"{left}{text}{right}"


def generate_hash(texto):
    """Generate a hash for the given text.

    Args:
        texto (str): the text.

    Returns:
        str: the generated hash
    """
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def prompt(
    text="",
    choices=None,
    default=None,
    show_choices=True,
    show_default=True,
    question_mark=False,
    empty_answer=True,
    case_sensitive=False,
    warning_style="red",
):
    """Returns a str with the answer of the question.

    Args:
        text (str|Text, optional): the text for the prompt. Defaults to "".
        choices (list, optional): a list of choices, they could be str or rich.text.Text. Defaults to None.
        show_choices (bool, optional): if True the prompt will show the choices. Defaults to True.
        show_default (bool, optional): if True the prompt will show the default. Defaults to True.
        default (str|Text, optional): a default value. Defaults to None.
        question_mark (bool, optional): if True a question mark will be appended to the text. Defaults to False.
        empty_answer (bool, optional): if True the answer could be an empty str. Defaults to True.
        case_sensitive (bool, optional): if True the choices are case sensitive. Defaults to False.
        warning_style (str, optional): the style for the warning messages. Defaults to "red".

    Raises:
        TypeError: if text is not a str or a rich.text.Text instance.
        TypeError: if choices is not a list.
        TypeError: if any of the choices is not a str or a rich.text.Text instance.
        TypeError: if default is not a str, Text or None.

    Returns:
        str: the answer.
    """
    if not isinstance(text, (str, Text)):
        raise TypeError("text must be a str or rich.text.Text.")
    if not text:
        text = Text()
    if isinstance(text, str):
        text = Text(text)
    if choices:
        if not isinstance(choices, list):
            raise TypeError("choices must be a list.")
        for choice in choices:
            if not isinstance(choice, (str, Text)):
                raise TypeError("choices must be a list of str or rich.text.Text.")
    if default and not isinstance(default, (str, Text)):
        raise TypeError("default must be a str or rich.text.Text.")
    if choices and show_choices:
        text.append(" ")
        text.append("(")
        for i, choice in enumerate(choices):
            text.append(choice)
            if i < len(choices) - 1:
                text.append("|")
        text.append(")")
    if default and show_default:
        text.append(" [")
        text.append(default)
        text.append("]")
    if question_mark:
        text.append("? ")
    else:
        text.append(": ")
    print(text, end="")
    while True:
        input_text = input()
        if not input_text:
            if default:
                return default
            elif not choices:
                if empty_answer:
                    return input_text
                print(Text("Se requiere su respuesta...", style=warning_style), end="")
                continue
        if not case_sensitive:
            if choices and input_text.lower() not in [str(choice).lower() for choice in choices]:
                print(Text("Seleccione de las opciones disponibles: ", style=warning_style), end="")
                continue
        else:
            if choices and input_text not in [str(choice) for choice in choices]:
                print(Text("Seleccione de las opciones disponibles: ", style=warning_style), end="")
                continue
        return input_text


def prompt_int(
    text="",
    choices=None,
    default=None,
    show_choices=True,
    show_default=True,
    question_mark=False,
    warning_style="red",
):
    """Returns a str with the answer of the question.

    Args:
        text (str|Text, optional): the text for the prompt. Defaults to "".
        choices (list, optional): a list of choices, they could be a int, str or rich.text.Text. Defaults to None.
        default (int|str|Text, optional): a default value. Defaults to None.
        show_choices (bool, optional): if True the prompt will show the choices. Defaults to True.
        show_default (bool, optional): if True the prompt will show the default. Defaults to True.
        question_mark (bool, optional): if True a question mark will be appended to the text. Defaults to False.
        warning_style (str, optional): the style for the warning messages. Defaults to "red".

    Raises:
        TypeError: if text is not a str or a rich.text.Text instance.
        TypeError: if choices is not a list.
        TypeError: if any of the choices is not an int, str or a rich.text.Text instance.
        TypeError: if default is not an int, str, Text or None.

    Returns:
        int: the int to be return.
    """
    if not isinstance(text, (str, Text)):
        raise TypeError("text must be a str or rich.text.Text.")
    if not text:
        text = Text()
    if isinstance(text, str):
        text = Text(text)
    if choices:
        if not isinstance(choices, list):
            raise TypeError("choices must be a list.")
        for choice in choices:
            if not isinstance(choice, (int, str, Text)):
                raise TypeError("choices must be a list of integer of type int, str or rich.text.Text.")
            if not str(choice).isdigit():
                raise ValueError("choices must be just digits.")
    if default and not isinstance(default, (int, str, Text)):
        raise TypeError("default must be a int, str or Text.")
    if choices and show_choices:
        text.append(" ")
        text.append("(")
        for i, choice in enumerate(choices):
            if isinstance(choice, int):
                text.append(str(choice))
            else:
                text.append(choice)
            if i < len(choices) - 1:
                text.append("|")
        text.append(")")
    if default and show_default:
        text.append(" [")
        if isinstance(default, int):
            text.append(str(default))
        else:
            text.append(default)
        text.append("]")
    if question_mark:
        text.append("? ")
    else:
        text.append(": ")
    print(text, end="")
    while True:
        input_text = input()
        if not input_text:
            if default:
                return default
            elif not choices:
                print(Text("Se requiere su respuesta...", style=warning_style), end="")
                continue
        if choices and input_text not in [str(choice) for choice in choices]:
            print(Text("Seleccione de las opciones disponibles: ", style=warning_style), end="")
            continue
        if not input_text.isdigit():
            print(Text("Solo se aceptan números. Dame tu respuesta: ", style=warning_style), end="")
            continue
        return int(input_text)


def prompt_float(
    text="",
    choices=None,
    default=None,
    show_choices=True,
    show_default=True,
    question_mark=False,
    warning_style="red",
):
    """Returns a str with the answer of the question.

    Args:
        text (str|Text, optional): the text for the prompt. Defaults to "".
        choices (list, optional): a list of choices, they could be float, int, str or rich.text.Text. Defaults to None.
        default (str|int|float|Text, optional): a default value. Defaults to None.
        show_choices (bool, optional): if True the prompt will show the choices. Defaults to True.
        show_default (bool, optional): if True the prompt will show the default. Defaults to True.
        question_mark (bool, optional): if True a question mark will be appended to the text. Defaults to False.
        warning_style (str, optional): the style for the warning messages. Defaults to "red".

    Raises:
        TypeError: if text is not a str or a rich.text.Text instance.
        TypeError: if choices is not a list.
        TypeError: if any of the choices is not a float, int, str or a rich.text.Text instance.
        TypeError: if default is not a float, int, str, Text or None.

    Returns:
        float: the float to be return.
    """
    if not isinstance(text, (str, Text)):
        raise TypeError("text must be a str or rich.text.Text.")
    if not text:
        text = Text()
    if isinstance(text, str):
        text = Text(text)
    if choices:
        if not isinstance(choices, list):
            raise TypeError("choices must be a list.")
        for choice in choices:
            if not isinstance(choice, (float, int, str, Text)):
                raise TypeError("choices must be a list of integer of type float, int, str or rich.text.Text.")
            try:
                float(choice)
            except Exception:
                raise ValueError("if choices are str or Text should be a float representation.")
    if default and not isinstance(default, (float, int, str, Text)):
        raise TypeError("default must be a float, int, str or Text.")
    if choices and show_choices:
        text.append(" ")
        text.append("(")
        for i, choice in enumerate(choices):
            if isinstance(choice, int):
                text.append(str(choice))
            else:
                text.append(choice)
            if i < len(choices) - 1:
                text.append("|")
        text.append(")")
    if default and show_default:
        text.append(" [")
        if isinstance(default, (int, float)):
            text.append(str(default))
        else:
            text.append(default)
        text.append("]")
    if question_mark:
        text.append("? ")
    else:
        text.append(": ")
    print(text, end="")
    while True:
        input_text = input()
        if not input_text:
            if default:
                return default
            elif not choices:
                print(Text("Se requiere su respuesta...", style=warning_style), end="")
                continue
        if choices and input_text not in [str(choice) for choice in choices]:
            print(Text("Seleccione de las opciones disponibles: ", style=warning_style), end="")
            continue
        try:
            result = float(input_text)
        except Exception:
            print(Text("Solo se aceptan números. Dame tu respuesta: ", style=warning_style), end="")
            continue
        return result


if __name__ == "__main__":
    respuesta = prompt("Dame tu tipo", ["hombre", "mujer", "niño"], question_mark=True, default="hombre")
    print(f"La respuesta es: {respuesta}")
