import json
import os

from rich import box
from rich.table import Table
from rich.text import Text

from euro_2024_api_handler import Euro2024ApiHandler
from tools import center_text


class Seat:
    """Class that represents a seat in a row of a section in the stadium.

    Raises:
        TypeError: if the type is not a str.
        ValueError: if the type is invalid.
        TypeError: if the sold is not a bool.

    Returns:
        Seat: a seat object.
    """

    SEAT_TYPES = ["general", "vip"]
    SEAT_COLORS = {
        "general": "bold dark_green",
        "vip": "bold gold3",
        "sold": "bold red",
    }
    NUM_SEAT_CODE_CHARACTERS = 8

    def __init__(self, floor, section, row, number, type, sold_in_matches=None):
        """The constructor

        Args:
            floor (int): the floor number.
            section (str): the section letter.
            row (int): the row number.
            number (int): the seat number.
            type (str): the seat type.
            sold_in_matches (list): Matches

        Raises:
            TypeError: if floor is not an int.
            TypeError: if section is not a str.
            TypeError: if row is not an int.
            TypeError: if number is not an int.
            TypeError: if type is not a str.
            ValueError: if type is invalid.
            TypeError: if sold is not a list.
        """
        if not isinstance(floor, int):
            raise TypeError("piso must be a int.")
        self.floor = floor
        if not isinstance(section, str):
            raise TypeError("section must be a str.")
        self.section = section.lower()
        if not isinstance(row, int):
            raise TypeError("row must be an int.")
        self.row = row
        if not isinstance(number, int):
            raise TypeError("number must be an int.")
        self.number = number
        if not isinstance(type, (str)):
            raise TypeError("type must be a str.")
        type = type.lower()
        if type not in self.SEAT_TYPES:
            raise ValueError("Invalid seat type.")
        self.type = type
        if not sold_in_matches:
            sold_in_matches = []
        if not isinstance(sold_in_matches, list):
            raise TypeError("sold_in_matches must be a list.")
        self.sold_in_matches = sold_in_matches

    def color(self, match=None):
        """Returns the color of the seat.

        Args:
            match (Match, optional): The match to look if the seat is sold. Defaults to None.

        Returns:
            str: The color of the seat.
        """
        if match and self.sold_in_matches and match in self.sold_in_matches:
            return self.SEAT_COLORS["sold"]
        return self.SEAT_COLORS[self.type]

    def text(self, match=None):
        """Returns the actual text of the seat.

        Returns:
            rich.text.Text: The actual text of the seat.
        """
        color = self.color(match)
        if self.number < 10:
            return Text(f"[0{self.number}]", style=color)
        return Text(f"[{self.number}]", style=color)

    def set_vip(self):
        """Change the seat to vip type."""
        self.type = "vip"

    def set_general(self):
        """Change the seat to general type."""
        self.type = "general"

    def sold(self, match):
        """The seat has been sold for the match, so the match should be append
        to the sold_in_matches list.

        Args:
            match (Match): the match where the seat has been sold.
        """
        if match not in self.sold_in_matches:
            self.sold_in_matches.append(match)

    def del_sold(self, match):
        """Remove the match from the sold_in_matches list.

        Args:
            match (Match): The match to be deleted.
        """
        if match in self.sold_in_matches:
            self.sold_in_matches.remove(match)

    def is_sold(self, match):
        """Check if the seat has been sold for the match.

        Args:
            match (Match): the match to look if the seat is sold.

        Returns:
            bool: True if the seat has been sold for the match and False otherwise.
        """
        if match in self.sold_in_matches:
            return True
        return False

    def code(self):
        """Returns the code or name of the seat.

        Returns:
            str: the code or name of the seat.
        """
        text = "P"
        if self.floor < 10:
            text += f"0{self.floor}"
        else:
            text += f"{self.floor}"
        text += self.section.upper()
        if self.row < 10:
            text += f"0{self.row}"
        else:
            text += f"{self.row}"
        if self.number < 10:
            text += f"0{self.number}"
        else:
            text += f"{self.number}"

        return text

    def is_vip(self):
        """Returns True if the seat is vip.

        Returns:
            bool: True if the seat is vip, False otherwise.
        """
        if self.type == "vip":
            return True
        return False


class Row:
    """Define a row of seats for a section of a stadium."""

    MAX_SEATS = 10

    def __init__(self, floor, section, number, num_seats):
        """The constructor

        Args:
            floor (int) the floor of the section.
            section (str): the letter of the section.
            number (int): the number of the row.
            seats (list): the list of seats of the row.

        Raises:
            TypeError: if floor is not a int.
            TypeError: if section is not a str.
            TypeError: if number is not a int.
            TypeError: if num_seats is not a int.
            ValueError: if num_seats > self.MAX_SEATS
        """
        if not isinstance(floor, int):
            raise TypeError("floor must be an int.")
        self.floor = floor
        if not isinstance(section, str):
            raise TypeError("section must be a str.")
        self.section = section.lower()
        if not isinstance(number, int):
            raise TypeError("number must be an int.")
        self.number = number
        if not isinstance(num_seats, int):
            raise TypeError("num_seats must be an int.")
        if num_seats > self.MAX_SEATS:
            raise ValueError(f"The row can't have more than {self.MAX_SEATS} seats.")
        self.num_seats = num_seats
        self.seats = []
        self.create_seats()

    def create_seats(self):
        """Generates the list of seats for the given amount for the row.

        Raises:
            TypeError: if the amount is not a int.
            ValueError: if the amount is greater than self.MAX_SEATS
        """
        for i in range(1, self.num_seats + 1):
            self.seats.append(Seat(self.floor, self.section, self.number, i, "general"))

    def seat(self, seat_number):
        """Returns the seat for the given number.

        Args:
            seat_number (int): the seat number.

        Raises:
            TypeError: if seat_number is not a int.
            ValueError: if the number is greater than self.MAX_SEATS or less than 1.

        Returns:
            Seat: the requested seat.
        """
        if not isinstance(seat_number, int):
            raise TypeError("The seat_number must be an int.")
        if seat_number < 1 or seat_number > self.num_seats:
            raise ValueError(f"The seat_number must be between 1 and {self.num_seats}.")
        return self.seats[seat_number - 1]

    def code(self):
        """Returns the code of the row.

        Returns:
            str: the code of the row.
        """
        text = ""
        if self.floor < 10:
            text += f"P0{self.floor}"
        else:
            text += f"P{self.floor}"
        text += f"{self.section.upper()}"
        if self.number < 10:
            text += f"0{self.number}"
        else:
            text += f"{self.number}"
        return text

    def text(self):
        """Returns the text of the row.

        Returns:
            rich.text.Text: the text of the row.
        """
        return Text(f"{self.code()}")

    def get_row_text(self, match=None, centered_seats_text=True):
        """Returns the text of the row with all the text of the seats.

        Args:
            match (Match, optional): The match to look at rows text. Defaults to None.
            centered_seats_text (bool, optional): if True, the seats text will be centered. Defaults to True.

        Returns:
            rich.text.Text: the text of the row with all the text of the seats.
        """
        text = Text()
        text.append(self.text())
        if centered_seats_text:
            text.append(":")
        else:
            text.append(": ")
        seats_text = Text()
        last_seat = len(self.seats)
        for seat in self.seats:
            seats_text.append(seat.text(match))
            if seat.number < last_seat:
                seats_text.append(" ")
        if centered_seats_text:
            if self.num_seats < self.MAX_SEATS:
                seats_text = center_text(seats_text, Section.MAX_NUM_CHARACTERS - 8)
            else:
                text.append(" ")
        text.append(seats_text)
        return text


class Section:
    """The class that represents a section of the stadium"""

    MAX_ROWS = 20
    MAX_CAPACITY = MAX_ROWS * Row.MAX_SEATS
    MAX_NUM_CHARACTERS = 58

    def __init__(self, floor, letter, location, capacity):
        """Constructor for Section.

        Args:
            floor (int): The floor of the section.
            letter (str): The letter of the section.
            location (str): The location of the section.
            capacity (int): The number of seats of the section.

        Raises:
            TypeError: if letter is not a str.
            TypeError: if location is not a str.
            TypeError: if capacity is not a int.
            ValueError: if capacity is greater than MAX_CAPACITY.
        """
        if not isinstance(floor, int):
            raise TypeError("floor must be a int.")
        self.floor = floor
        if not isinstance(letter, str):
            raise TypeError("letter must be a str.")
        self.letter = letter.lower()
        if not isinstance(location, str):
            raise TypeError("location must be a str.")
        location = location.lower()
        self.location = location
        if not isinstance(capacity, int):
            raise TypeError("capacity must be an int.")
        if capacity > self.MAX_CAPACITY:
            raise ValueError(f"The section can't have more than {self.MAX_CAPACITY} seats.")
        self.capacity = capacity
        self.num_rows = 0
        self.rows = []
        self.create_rows()

    def create_rows(self):
        """Generates a list of rows for the section."""
        num_rows = self.capacity // Row.MAX_SEATS
        if self.capacity % Row.MAX_SEATS > 0:
            num_rows += 1
        self.num_rows = num_rows
        missing_seats = self.capacity
        for i in range(1, num_rows):
            self.rows.append(Row(self.floor, self.letter, i, Row.MAX_SEATS))
            missing_seats -= Row.MAX_SEATS
        self.rows.append(Row(self.floor, self.letter, num_rows, missing_seats))

    def text(self):
        """Returns the text of the section"""
        return Text(self.code())

    def code(self):
        """The code of the section.

        Returns:
            str: The code of the section
        """
        text = ""
        if self.floor < 10:
            text += f"P0{self.floor}"
        else:
            text += f"P{self.floor}"
        text += f"{self.letter.upper()}"
        return text

    def row(self, row_number):
        """Returns the row for the given row number.

        Args:
            row_number (int): the row number.

        Raises:
            TypeError: if row_number is not a int.
            ValueError: if row_number is invalid.

        Returns:
            _type_: _description_
        """
        if not isinstance(row_number, int):
            raise TypeError("row_number must be an int.")
        if row_number > len(self.rows) or row_number < 1:
            raise ValueError(f"The row_number must be between 1 and {len(self.rows)}.")
        return self.rows[row_number - 1]

    def seat(self, row_number, seat_number):
        """Returns the seat of the given row_number and seat_number.

        Args:
            row_number (int): the row number.
            seat_number (int): the seat number.

        Raises:
            TypeError: if row_number is not an int.
            TypeError: if seat_number is not an int.
            ValueError: if row_number is < 1 or bigger than the number of rows of the section.
            ValueError: if seat_number is < 1 or bigger than the number of seats of row.

        Returns:
            Seat: the seat of the given row_number and seat_number.
        """
        if not isinstance(row_number, int):
            raise TypeError("row_number must be an int.")
        if not isinstance(seat_number, int):
            raise TypeError("seat_number must be an int.")
        if row_number > len(self.rows) or row_number < 1:
            raise ValueError(f"The row number must be between 1 and {len(self.rows)}.")
        if seat_number > self.rows[row_number - 1].num_seats or seat_number < 1:
            raise ValueError(f"The seat number must be between 1 and {self.rows[row_number - 1].num_seats}.")
        row = self.row(row_number)
        if not row:
            return None
        return row.seat(seat_number)

    def get_rows_text(self, match=None, centered_seats_text=True):
        """Return the text of the section rows and their seats.

        Args:
            match (Match, optional): The match for getting the seats info. Defaults to None.
            centered_seats_text (bool, optional): if True, the seats text will be centered.

        Returns:
            list: a list of rich.text.Text with the text of every row or the section.
        """
        rows = []
        for row in self.rows:
            text = center_text(row.get_row_text(match, centered_seats_text), Section.MAX_NUM_CHARACTERS)
            rows.append(text)
        return rows

    def get_titles(self):
        """Get the section title

        Returns:
            list: the section title texts
        """
        section_text = []

        text = Text()
        tmp_text = f"Sección {self.letter.upper()}"
        tmp_centered_text = center_text(tmp_text, self.MAX_NUM_CHARACTERS)
        text.append(tmp_centered_text)
        section_text.append(text)

        text = Text()
        tmp_text = f"Ubicación: {Stadium.LOCATION_DICT[self.location].title()}"
        tmp_centered_text = center_text(tmp_text, self.MAX_NUM_CHARACTERS)
        text.append(tmp_centered_text)
        section_text.append(text)

        text = Text()
        tmp_text = f"Piso: {self.floor}"
        tmp_centered_text = center_text(tmp_text, self.MAX_NUM_CHARACTERS)
        text.append(tmp_centered_text)
        section_text.append(text)

        text = Text()
        tmp_text = f"Capacidad: {self.capacity}"
        tmp_centered_text = center_text(tmp_text, self.MAX_NUM_CHARACTERS)
        text.append(tmp_centered_text)
        section_text.append(text)

        text = Text()
        tmp_text = "Asientos VIP"
        tmp_centered_text = center_text(tmp_text, self.MAX_NUM_CHARACTERS)
        text.append(tmp_centered_text, style=Seat.SEAT_COLORS["vip"])
        section_text.append(text)

        text = Text()
        tmp_text = "Asientos Generales"
        tmp_centered_text = center_text(tmp_text, self.MAX_NUM_CHARACTERS)
        text.append(tmp_centered_text, style=Seat.SEAT_COLORS["general"])
        section_text.append(text)

        text = Text()
        tmp_text = "Asientos Vendidos"
        tmp_centered_text = center_text(tmp_text, self.MAX_NUM_CHARACTERS)
        text.append(tmp_centered_text, style=Seat.SEAT_COLORS["sold"])
        section_text.append(text)

        return section_text

    def get_titles_and_rows_text(self, match=None, centered_seats_text=True, sep_lines=1):
        """Return a list with the titles and rows texts.

        Args:
            match (Match, optional): The match for getting the seats info. Defaults to None.
            centered_seats_text (bool, optional): if True, the seats text will be centered. Defaults to True.
            sep_lines (int, optional): the number of sep lines between the titles and rows texts. Defaults to 1.

        Returns:
            list: the list of titles and rows texts
        """
        titles = self.get_titles()
        rows = self.get_rows_text(match, centered_seats_text)
        all_info = []
        all_info += titles
        sep_text = Text(center_text("", self.MAX_NUM_CHARACTERS))
        for i in range(sep_lines):
            all_info += [sep_text]
        all_info += rows
        return all_info


class Stadium:
    """Class that represents a stadium

    Returns:
        Stadium: a stadium object
    """

    MAX_NUM_SECTIONS_PER_FLOOR = 8
    LOCATIONS = ["front", "back", "left", "right"]
    SECTIONS_LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h"]
    NUM_SEP_SPACES = 2
    LOCATION_DICT = {"front": "frontal", "back": "trasera", "right": "derecha", "left": "izquierda"}

    def __init__(self, id, name, city, num_general_seats, num_vip_seats):
        """The constructor

        Args:
            id (str): the id of the stadium.
            name (str): the name of the stadium.
            city (str): the city of the stadium.
            num_general_seats (int): the number of seats of type general.
            num_vip_seats (int): the number of seats of type vip.

        Raises:
            TypeError: if the id is not a str.
            TypeError: if the name is not a str.
            TypeError: if the city is not a str.
            TypeError: if general_seats is not a int.
            TypeError: if vip_seats is not a int.

        """
        if not isinstance(id, str):
            raise TypeError("id must be a str.")
        self.id = id
        if not isinstance(name, str):
            raise TypeError("name must be a str.")
        self.name = name
        if not isinstance(city, str):
            raise TypeError("city must be a str.")
        self.city = city
        if not isinstance(num_general_seats, int):
            raise TypeError("num_general_seats must be an int.")
        self.general_seats = num_general_seats
        if not isinstance(num_vip_seats, int):
            raise TypeError("num_vip_seats must be an int.")
        self.vip_seats = num_vip_seats
        self.capacity = num_general_seats + num_vip_seats
        self.sections = []
        self.num_floors = 0
        self.num_sections = 0
        self.create_sections()
        self.set_vip_seats()

    def __str__(self):
        """The string representation of a stadium

        Returns:
            str: the string representation of a stadium
        """
        return f"{self.name}: city: {self.city} - vip: {self.vip_seats} - general: {self.general_seats}"

    def __repr__(self):
        return f"<Stadium {self.name}>"

    def create_sections(self):
        """Create the sections of the stadium."""
        num_floors = self.capacity // (self.MAX_NUM_SECTIONS_PER_FLOOR * Section.MAX_CAPACITY)
        if self.capacity % (self.MAX_NUM_SECTIONS_PER_FLOOR * Section.MAX_CAPACITY) > 0:
            num_floors += 1
        self.num_floors = num_floors
        num_sections = self.capacity // Section.MAX_CAPACITY
        if self.capacity % Section.MAX_CAPACITY > 0:
            num_sections += 1
        self.num_sections = num_sections
        needed_capacity = self.capacity
        for i in range(1, num_floors + 1):
            section_capacity = Section.MAX_CAPACITY
            for section_number in range(self.MAX_NUM_SECTIONS_PER_FLOOR):
                if section_number in {0, 1, 2}:
                    location = self.LOCATIONS[0]
                elif section_number in {3, 4, 5}:
                    location = self.LOCATIONS[1]
                elif section_number in {6}:
                    location = self.LOCATIONS[2]
                elif section_number in {7}:
                    location = self.LOCATIONS[3]
                letter = self.SECTIONS_LETTERS[section_number]
                if needed_capacity >= section_capacity:
                    self.sections.append(Section(i, letter, location, section_capacity))
                else:
                    self.sections.append(Section(i, letter, location, needed_capacity))
                needed_capacity -= section_capacity
                if needed_capacity <= 0:
                    return

    def section(self, floor, letter):
        """Returns the section object for the given floor and Letter.

        Args:
            floor (int): the floor.
            letter (str): the letter of the section

        Raises:
            TypeError: if floor is not a int.
            ValueError: if floor < 1 or floor > self._num_floors.
            TypeError: if letter is not a str.
            ValueError: if letter has more that one character.
            ValueError: if letter is not in self.SECTIONS_LETTERS.

        Returns:
            Section: the section object for the given floor and Letter.
        """
        if not isinstance(floor, int):
            raise TypeError("floor must be an int.")
        if floor < 1 or floor > self.num_floors:
            raise ValueError(f"floor must be between 1 and {self.num_floors}.")
        if not isinstance(letter, str):
            raise TypeError("letter must be a str.")
        if len(letter) != 1:
            raise ValueError("letter must be a single character.")
        if letter.lower() not in self.SECTIONS_LETTERS:
            raise ValueError(f"letter must be one of {self.SECTIONS_LETTERS}.")
        for section in self.sections:
            if section.floor == floor and section.letter == letter:
                return section

    def seat(self, floor, letter, row_number, seat_number):
        """Returns the seat for the given floor, letter, row_number and seat_number.

        Args:
            floor (int): the floor number.
            letter (str): the section letter.
            row_number (int): the row number.
            seat_number (int): the seat number.

        Returns:
            Seat: the requested seat.
        """
        section = self.section(floor, letter)
        if not section:
            return None
        seat = section.seat(row_number, seat_number)
        return seat

    def seat_by_code(self, seat_code):
        """Returns a seat by its code.

        Args:
            seat_code (str): the seat code.

        Raises:
            TypeError: if the seat code is not a str.
            ValueError: if the seat code doesn't have the correct size.
            ValueError: if the floor number is invalid.
            ValueError: if the section letter is invalid.
            ValueError: if the row number is invalid.
            ValueError: if the seat number is invalid.

        Returns:
            Seat: the Seat object of the seat_code given.
        """
        if not isinstance(seat_code, str):
            raise TypeError("seat_code must be a str.")
        if len(seat_code) != Seat.NUM_SEAT_CODE_CHARACTERS:
            raise ValueError(f"seat_code must be {Seat.NUM_SEAT_CODE_CHARACTERS} characters long.")
        floor_number = seat_code[1:3]
        if not floor_number.isdigit():
            raise ValueError("The seat_code has a invalid floor number.")
        floor_number = int(floor_number)
        section_letter = seat_code[3].lower()
        if section_letter not in self.SECTIONS_LETTERS:
            raise ValueError(f"section_letter must be one of {self.SECTIONS_LETTERS}.")
        row_number = seat_code[4:6]
        if not row_number.isdigit():
            raise ValueError("The seat_code has a invalid row number.")
        row_number = int(row_number)
        seat_number = seat_code[6:]
        if not seat_number.isdigit():
            raise ValueError("The seat_code has a invalid seat number.")
        seat_number = int(seat_number)
        return self.seat(floor_number, section_letter, row_number, seat_number)

    def set_vip_seats(self):
        """Set the vip seats for the stadium."""
        vip_seats = self.vip_seats
        for row_number in range(1, Section.MAX_ROWS + 1):
            for floor in range(1, self.num_floors + 1):
                floor_sections = self.sections_by_floor(floor)
                for section in floor_sections:
                    if row_number > section.num_rows:
                        continue
                    row = section.row(row_number)
                    if not row:
                        continue
                    for seat_number in range(1, row.num_seats + 1):
                        seat = section.seat(row_number, seat_number)
                        if not seat:
                            break
                        seat.set_vip()
                        vip_seats -= 1
                        if vip_seats == 0:
                            return

    def get_section_titles_and_rows_text(self, floor, letter, match=None, centered_seats_text=True, sep_lines=1):
        """Returns the text of the section with the given floor and letter.

        Args:
            floor (int): the section floor number.
            letter (str): the section letter.
            match (Match, optional): The Match. Defaults to None.
            centered_seats_text (bool, optional): if True, the seats text will be centered. Defaults to True.
            sep_lines (int, optional): the number of sep lines between the titles and rows texts. Defaults to 1.

        Returns:
            list: a list of rich.text.Text objects.
        """
        section = self.section(floor, letter)
        if not section:
            return None
        return section.get_titles_and_rows_text(match, centered_seats_text, sep_lines)

    def sections_by_floor(self, floor):
        """Returns a list of sections for the given floor.

        Args:
            floor (int): the floor number.

        Raises:
            TypeError: if the given floor is not an int.
            ValueError: if the given floor is invalid.

        Returns:
            list: a list of sections for the given floor.
        """
        if not isinstance(floor, int):
            raise TypeError("floor must be an int.")
        if floor < 1 or floor > self.num_floors:
            raise ValueError(f"floor must be between 1 and {self.num_floors}.")
        sections = []
        for section in self.sections:
            if section.floor == floor:
                sections.append(section)
        return sections

    def sections_by_location(self, floor, location):
        """Return a list of sections for the given floor and location.

        Args:
            floor (int): the floor of the section.
            location (str): the location of the section.

        Returns:
            list: a list of sections for the given floor and location.
        """
        sections = self.sections_by_floor(floor)
        location_sections = []
        for section in sections:
            if section.location == location:
                location_sections.append(section)
        return location_sections

    def get_sections_titles_and_rows_text_by_location(
        self, floor, location, match=None, centered_seats_text=True, sep_lines=1
    ):
        """The text of the sections for the given floor and location.

        Args:
            floor (int): the floor of the section.
            location (str): the location of the section.
            match (Match, optional): the match. Defaults to None.
            centered_seats_text (bool, optional): if True, the seats text will be centered. Defaults to True.
            sep_lines (int, optional): the number of sep lines between the titles and rows texts. Defaults to 1.

        Returns:
            list: a list of rich.text.Text objects with the texto of the sections.
        """
        sections = self.sections_by_location(floor, location)
        if not sections:
            return None
        sections_text = []
        for section in sections:
            sections_text.append(
                self.get_section_titles_and_rows_text(
                    section.floor, section.letter, match, centered_seats_text, sep_lines
                )
            )
        sections_merged_text = self.merge_sections_text_lines(sections_text, self.NUM_SEP_SPACES)
        return sections_merged_text

    def merge_sections_text_lines(self, sections_lines, num_sep_spaces):
        """Returns a merge of the text lines.

        Args:
            sections_lines (list): The list of rich.text.Text objects or str to be merged.
            num_sep_spaces (int): The spaces between the text lines to be merged.

        Returns:
            list: a list of rich.text.Text objects of the merged lines.
        """
        merged_lines = []
        num_sections = len(sections_lines)
        if num_sections <= 1:
            return sections_lines[0]
        max_section_lines = len(sections_lines[0])
        for i in range(1, num_sections):
            max_section_lines = max([max_section_lines, len(sections_lines[i])])
        for i in range(max_section_lines):
            text = Text()
            for j in range(num_sections):
                if i < len(sections_lines[j]):
                    tmp = sections_lines[j][i]
                else:
                    tmp = " " * Section.MAX_NUM_CHARACTERS
                if j < 2:
                    tmp += " " * num_sep_spaces
                text.append(tmp)
            merged_lines.append(text)
        return merged_lines

    def get_titles(self, floor=None, location=None, centered=True):
        """The stadium title lines for sections

        Args:
            location (str): The location.
            centered (bool): if True, the text will be centered using a pad character.
        Returns:
            list: a list of rich.text.Text objects with the stadium titles.
        """
        if floor and location:
            sections = self.sections_by_location(floor, location)
            num_sections = len(sections)
            total_spaces = Section.MAX_NUM_CHARACTERS * num_sections + self.NUM_SEP_SPACES * (num_sections - 1)
        else:
            total_spaces = Section.MAX_NUM_CHARACTERS

        stadium_titles = []
        text = Text()
        tmp_text = f"Estadio: {self.name}"
        if centered:
            tmp_centered_text = center_text(tmp_text, total_spaces)
            text.append(tmp_centered_text)
        else:
            text.append(tmp_text)
        stadium_titles.append(text)

        text = Text()
        tmp_text = f"Ciudad: {self.city}"
        if centered:
            tmp_centered_text = center_text(tmp_text, total_spaces)
            text.append(tmp_centered_text)
        else:
            text.append(tmp_text)
        stadium_titles.append(text)

        text = Text()
        tmp_text = f"Capacidad: {self.capacity}"
        if centered:
            tmp_centered_text = center_text(tmp_text, total_spaces)
            text.append(tmp_centered_text)
        else:
            text.append(tmp_text)
        stadium_titles.append(text)

        text = Text()
        tmp_text = f"VIP: {self.vip_seats}"
        if centered:
            tmp_centered_text = center_text(tmp_text, total_spaces)
            text.append(tmp_centered_text)
        else:
            text.append(tmp_text)
        stadium_titles.append(text)

        text = Text()
        tmp_text = f"Generales: {self.general_seats}"
        if centered:
            tmp_centered_text = center_text(tmp_text, total_spaces)
            text.append(tmp_centered_text)
        else:
            text.append(tmp_text)
        stadium_titles.append(text)

        return stadium_titles

    def get_stadium_location_section_titles_and_info_table_format(
        self, floor, location, match=None, centered_seats_text=True
    ):
        """The text of the sections for the given floor and location, return using rich.table.Table.

        Args:
            floor (int): the floor of the section.
            location (str): the location of the section.
            match (Match, optional): the match. Defaults to None.
            centered_seats_text (bool, optional): if True, the seats text will be centered. Defaults to True.

        Returns:
            rich.table.Table: a table with the info.
        """
        stadium_titles = self.get_titles(floor, location, centered=False)
        len_stadium_titles = len(stadium_titles)
        stadium_titles_text = Text()
        for i, line in enumerate(stadium_titles):
            stadium_titles_text.append(line)
            if i < len_stadium_titles - 1:
                stadium_titles_text.append("\n")

        sections = self.sections_by_location(floor, location)
        if not sections:
            return None
        sections_text = []
        for section in sections:
            section_titles = section.get_titles()
            len_section_titles = len(section_titles)
            section_titles_text = Text()
            for i, line in enumerate(section_titles):
                section_titles_text.append(line)
                if i < len_section_titles - 1:
                    section_titles_text.append("\n")
            rows_info = section.get_rows_text(match, centered_seats_text)
            len_rows_info = len(rows_info)
            rows_info_text = Text()
            for i, line in enumerate(rows_info):
                rows_info_text.append(line)
                if i < len_rows_info - 1:
                    rows_info_text.append("\n")
            sections_text.append([section_titles_text, rows_info_text])
        table = Table(title=stadium_titles_text)
        for i in range(len(sections_text)):
            table.add_column(sections_text[i][0])
        rows_text_list = []
        for i in range(len(sections_text)):
            rows_text_list.append(sections_text[i][1])
        table.add_row(*rows_text_list)
        return table

    def get_stadium_locations_and_sections_info(self, floor=1):
        """Return the info of the Stadium for the floor, locations and sections.

        Returns:
            list: a list of rich.text.Text objects.
        """
        if not isinstance(floor, int):
            raise TypeError("floor must be an int.")
        if floor < 1 or floor > self.num_floors:
            raise ValueError(f"floor must be between 1 and {self.num_floors}.")

        num_sections_front = len(self.sections_by_location(floor, "front"))
        num_sections_back = len(self.sections_by_location(floor, "back"))
        num_sections_left = len(self.sections_by_location(floor, "left"))
        num_sections_right = len(self.sections_by_location(floor, "right"))

        text_lines = []

        estadio_text = f"Estadio: {self.name}"
        city_text = f"Ciudad: {self.city}"
        sections_Locations_text = f"Secciones y Localidades del Piso: {floor}"

        if len(estadio_text) >= len(city_text):
            box_spaces = len(estadio_text)
        else:
            box_spaces = len(city_text)

        if len(sections_Locations_text) > box_spaces:
            box_spaces = len(sections_Locations_text)

        if num_sections_left:
            left_spaces = box_spaces
        else:
            left_spaces = 0

        text = Text()

        tmp_text = estadio_text
        tmp_centered_text = center_text(tmp_text, box_spaces)
        tmp_centered_text = " " * left_spaces + tmp_centered_text
        text.append(tmp_centered_text)
        text_lines.append(text)

        text = Text()

        tmp_text = city_text
        tmp_centered_text = center_text(tmp_text, box_spaces)
        tmp_centered_text = " " * left_spaces + tmp_centered_text
        text.append(tmp_centered_text)
        text_lines.append(text)

        text = Text()
        tmp_text = f"Capacidad: {self.capacity}"
        tmp_centered_text = center_text(tmp_text, box_spaces)
        tmp_centered_text = " " * left_spaces + tmp_centered_text
        text.append(tmp_centered_text)
        text_lines.append(text)

        text = Text()
        tmp_text = f"Pisos: {self.num_floors}"
        tmp_centered_text = center_text(tmp_text, box_spaces)
        tmp_centered_text = " " * left_spaces + tmp_centered_text
        text.append(tmp_centered_text)
        text_lines.append(text)

        text = Text()
        tmp_text = f"VIP: {self.vip_seats}"
        tmp_centered_text = center_text(tmp_text, box_spaces)
        tmp_centered_text = " " * left_spaces + tmp_centered_text
        text.append(tmp_centered_text)
        text_lines.append(text)

        text = Text()
        tmp_text = f"Generales: {self.general_seats}"
        tmp_centered_text = center_text(tmp_text, box_spaces)
        tmp_centered_text = " " * left_spaces + tmp_centered_text
        text.append(tmp_centered_text)
        text_lines.append(text)

        text = Text()
        text_lines.append(text)

        text = Text()

        tmp_text = sections_Locations_text
        tmp_centered_text = center_text(tmp_text, box_spaces)
        tmp_centered_text = " " * left_spaces + tmp_centered_text
        text.append(tmp_centered_text)
        text_lines.append(text)

        text = Text()
        text_lines.append(text)

        text = Text()
        tmp_text = "Ubicación: Frontal"
        tmp_centered_text = center_text(tmp_text, box_spaces)
        tmp_centered_text = " " * left_spaces + tmp_centered_text
        text.append(tmp_centered_text)
        text_lines.append(text)

        text = Text()
        sections = ["A", "B", "C"]
        tmp_text = f"Secciones: {sections[0:num_sections_front]}"
        tmp_centered_text = center_text(tmp_text, box_spaces)
        tmp_centered_text = " " * left_spaces + tmp_centered_text
        text.append(tmp_centered_text)
        text_lines.append(text)

        text = Text()
        text_lines.append(text)

        text = Text()
        text_lines.append(text)

        if num_sections_left:
            text = Text()
            tmp_text = "Ubicación: Izquierda"
            tmp_centered_text = center_text(tmp_text, box_spaces)
            text.append(tmp_centered_text)
            tmp_text = " " * box_spaces
            text.append(tmp_text)
            if num_sections_right:
                tmp_text = "Ubicación: Derecha"
                tmp_centered_text = center_text(tmp_text, box_spaces)
                text.append(tmp_centered_text)
            text_lines.append(text)

            text = Text()
            tmp_text = "Sección: ['G']"
            tmp_centered_text = center_text(tmp_text, box_spaces)
            text.append(tmp_centered_text)
            tmp_text = " " * box_spaces
            text.append(tmp_text)
            if num_sections_right:
                tmp_text = "Sección: ['H']"
                tmp_centered_text = center_text(tmp_text, box_spaces)
                text.append(tmp_centered_text)
            text_lines.append(text)

        text = Text()
        text_lines.append(text)

        if num_sections_back:
            text = Text()
            tmp_text = "Ubicación: Trasera"
            tmp_centered_text = center_text(tmp_text, box_spaces)
            tmp_centered_text = " " * left_spaces + tmp_centered_text
            text.append(tmp_centered_text)
            text_lines.append(text)

            text = Text()
            sections = ["D", "E", "F"]
            tmp_text = f"Secciones: {sections[0:num_sections_back]}"
            tmp_centered_text = center_text(tmp_text, box_spaces)
            tmp_centered_text = " " * left_spaces + tmp_centered_text
            text.append(tmp_centered_text)
            text_lines.append(text)

        return text_lines

    def get_stadium_locations_and_sections_info_table_format(self, floor=1):
        """Return the info of the Stadium for the floor, locations and sections using
        rich.table.Table.

        Returns:
            rich.table.Table : The table with the info.
        """
        if not isinstance(floor, int):
            raise TypeError("floor must be an int.")
        if floor < 1 or floor > self.num_floors:
            raise ValueError(f"floor must be between 1 and {self.num_floors}.")

        num_sections_front = len(self.sections_by_location(floor, "front"))
        num_sections_back = len(self.sections_by_location(floor, "back"))
        num_sections_left = len(self.sections_by_location(floor, "left"))
        num_sections_right = len(self.sections_by_location(floor, "right"))

        estadio_text = f"Estadio: {self.name}"
        city_text = f"Ciudad: {self.city}"
        capacity_text = f"Capacidad: {self.capacity}"
        pisos_text = f"Pisos: {self.num_floors}"
        vip_text = f"VIP: {self.vip_seats}"
        generales_text = f"Generales: {self.general_seats}"
        sections_locations_text = f"Secciones y Localidades del Piso: {floor}"

        stadium_titles_text = Text()
        stadium_titles_text.append(estadio_text)
        stadium_titles_text.append("\n")
        stadium_titles_text.append(city_text)
        stadium_titles_text.append("\n")
        stadium_titles_text.append(capacity_text)
        stadium_titles_text.append("\n")
        stadium_titles_text.append(pisos_text)
        stadium_titles_text.append("\n")
        stadium_titles_text.append(vip_text)
        stadium_titles_text.append("\n")
        stadium_titles_text.append(generales_text)
        stadium_titles_text.append("\n")
        stadium_titles_text.append(sections_locations_text)

        front_sections_text = Text()
        front_sections_text.append("Ubicación: Frontal")
        front_sections_text.append("\n")
        sections = ["A", "B", "C"]
        front_sections_text.append(f"Secciones: {sections[0:num_sections_front]}")

        table = Table(title=stadium_titles_text, box=box.MINIMAL, min_width=70, show_lines=True)
        if num_sections_left:
            table.add_column(justify="center")
        table.add_column(front_sections_text, justify="center")
        if num_sections_right:
            table.add_column(justify="center")

        if num_sections_left:
            left_section_text = Text()
            left_section_text.append("Ubicación: Izquierda", style="bold")
            left_section_text.append("\n")
            left_section_text.append("Sección: ['G']", style="bold")
            if num_sections_right:
                right_section_text = Text()
                right_section_text.append("Ubicación: Derecha", style="bold")
                right_section_text.append("\n")
                right_section_text.append("Sección: ['H']", style="bold")
                table.add_row(left_section_text, None, right_section_text)
            else:
                table.add_row(left_section_text, None)

        if num_sections_back:
            back_sections_text = Text()
            back_sections_text.append("Ubicación: Trasera", style="bold")
            back_sections_text.append("\n")
            sections = ["D", "E", "F"]
            back_sections_text.append(f"Secciones: {sections[0:num_sections_back]}", style="bold")
            if num_sections_left:
                if num_sections_right:
                    table.add_row(None, back_sections_text, None)
                else:
                    table.add_row(None, back_sections_text)
            else:
                table.add_row(back_sections_text)
        return table


class StadiumManager:
    DATA_FILENAME = "stadiums.json"

    def __init__(self, stadiums=None):
        if not stadiums:
            stadiums = []
        if not isinstance(stadiums, list):
            raise TypeError("stadiums must be a list.")
        self.stadiums = []
        self.api_handler = Euro2024ApiHandler()

    def add_stadium(self, stadium):
        if not isinstance(stadium, Stadium):
            raise TypeError("stadium must be an instance of Stadium.")
        if stadium not in self.stadiums:
            self.stadiums.append(stadium)

    def remove_stadium(self, stadium):
        if not isinstance(stadium, Stadium):
            raise TypeError("stadium must be an instance of Stadium.")
        if stadium in self.stadiums:
            self.stadiums.remove(stadium)

    def get_stadium_by_name(self, name):
        for stadium in self.stadiums:
            if stadium.name == name:
                return stadium
        return None

    def get_stadium_by_id(self, id):
        for stadium in self.stadiums:
            if stadium.id == id:
                return stadium
        return None

    def load_stadiums_data(self, restaurant_manager):
        if not os.path.exists(self.DATA_FILENAME):
            stadiums_data = self.api_handler.get_stadiums()
        else:
            with open(self.DATA_FILENAME, "r", encoding="utf-8") as fh:
                stadiums_data = json.load(fh)
        self.stadiums = []
        restaurant_manager.restaurants = []
        for item in stadiums_data:
            stadium = Stadium(
                id=item["id"],
                name=item["name"],
                city=item["city"],
                num_general_seats=item["capacity"][0],
                num_vip_seats=item["capacity"][1],
            )
            self.add_stadium(stadium)
            restaurants = item["restaurants"]
            restaurant_manager.load_restaurants_data(stadium, restaurants)

    def save_stadiums_data(self, restaurant_manager):
        stadiums_data = []
        for stadium in self.stadiums:
            stadium_data = {}
            stadium_data["id"] = stadium.id
            stadium_data["name"] = stadium.name
            stadium_data["city"] = stadium.city
            stadium_data["capacity"] = [stadium.general_seats, stadium.vip_seats]
            restaurants_data = restaurant_manager.save_restaurants_data(stadium)
            stadium_data["restaurants"] = restaurants_data
            stadiums_data.append(stadium_data)
        with open(self.DATA_FILENAME, "w", encoding="utf-8") as fh:
            json.dump(stadiums_data, fh)

    def del_data_file(self):
        if os.path.exists(self.DATA_FILENAME):
            os.remove(self.DATA_FILENAME)


if __name__ == "__main__":
    pass
