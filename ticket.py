import json
import os
import uuid

from rich.table import Table
from rich.text import Text

from constant import IVA
from customer import Customer
from match_and_team import Match
from stadium import Seat


class Ticket:
    TICKET_TYPES_AND_PRICES = {
        "general": 35.0,
        "vip": 75.0,
    }
    DISCOUNT_TYPES_AND_PERCENTAGES = {"vampire_number": 50.0}

    def __init__(self, customer, match, seat, code=None, used=None):
        """Initialize a Ticket.

        Args:
            customer (Customer): the customer obj.
            match (Match): the match obj.

            seat (int): the seat number.

        Raises:
            ValueError: if type is not in TICKET_TYPES_AND_PRICES.keys().
        """
        if not isinstance(customer, Customer):
            raise ValueError("Customer must be a Customer obj.")
        self.customer = customer
        if not isinstance(match, Match):
            raise ValueError("Match must be a Match obj.")
        self.match = match
        if not isinstance(seat, Seat):
            raise TypeError("Seat must be a Seat obj.")
        self.seat = seat
        self.type = seat.type.lower()
        self.price = self.TICKET_TYPES_AND_PRICES[self.type]
        if code is None:
            self.code = str(uuid.uuid4()).upper()
        else:
            if not isinstance(code, str):
                raise TypeError("Code must be None or str.")
            self.code = code.upper()
        if used is None:
            self.used = False
        else:
            if not isinstance(used, bool):
                raise TypeError("Used must be None or bool.")
            self.used = used

    def __str__(self):
        """The ticket str representation.

        Returns:
            str: the ticket representation.
        """
        return (
            f"Ticket - Type: {self.type} - code: {self._code} - customer: {self.customer} - "
            + f"match: {self.match} - seat: {self.seat.code()} - "
            + f"Price: {self.price} - Tax: {self.get_tax_amount()} - Total: {self.get_total_price()}"
        )

    def get_tax_amount(self):
        """Returns the tax amount.

        Returns:
            float: the tax amount.
        """
        price = round(self.price - self.get_discount_amount())
        return round(price * IVA / 100, 2)

    def get_discount_amount(self):
        """Returns the discount amounts.

        Returns:
            Float: the discount amount.
        """
        if self.customer.is_vampire():
            discount = self.DISCOUNT_TYPES_AND_PERCENTAGES["vampire_number"]
            return round(self.price * discount / 100, 2)
        return 0.0

    def get_total_price(self):
        """Returns the total price.

        Returns:
            float: the total price.
        """
        price = round(self.price - self.get_discount_amount())
        return round(price + self.get_tax_amount(), 2)

    def is_valid(self, code):
        """Returns True if the code is valid.

        Args:
            code (str): the ticket's code.

        Returns:
            bool: True if the code is valid and False otherwise.
        """
        if self.code == code.upper():
            return True
        return False

    def use(self):
        """Mark the ticket as used."""
        self.used = True

    def is_used(self):
        """Returns True if the ticket is used.

        Returns:
            bool: True if the ticket is used, False otherwise.
        """
        return self.used

    def validate(self, code):
        """Validate the ticket, and mark as used if everything is ok returning True.
        Returns None if the ticket was previously used. Returns False if the ticket
        code is invalid (so is a False ticket).

        Args:
            code (str): The ticket's code to be validated.

        Returns:
            None|Boolean: True if the ticket is ok. None if the ticket was already used.
                False if the ticket's code is invalid.
        """
        if self.is_valid(code) and not self.is_used():
            self.use()
            return True
        elif self.is_used():
            return None
        return False

    def show_ticket(self):

        text = Text()
        text.append("Nombre: ")
        text.append(f"{self.customer.full_name.title()}", style="bold blue")
        text.append("\n")
        text.append("Juego: ")
        text.append(f"{self.match.home.name.title()}", style="bold blue")
        text.append(" vs ")
        text.append(f"{self.match.away.name.title()}", style="bold blue")
        text.append("\n")
        text.append("Grupo: ")
        text.append(f"{self.match.group}", style="bold blue")
        text.append("\n")
        text.append("Estadio:")
        text.append(f"{self.match.stadium.name.title()}", style="bold blue")
        text.append("Fecha: ")
        text.append(f"{self.match.date.strftime('%d/%m/%Y')}", style="bold blue")
        text.append("\n")
        text.append("Tipo: ")
        if self.type == "vip":
            text.append(f"{self.type.capitalize()}", style="bold gold3")
        else:
            text.append(f"{self.type.capitalize()}", style="bold blue")
        text.append("\n")
        text.append("Asiento: ")
        text.append(f"{self.seat.code()}", style="bold blue")
        text.append("\n")
        text.append("Código Seguridad: ")
        text.append(f"{self.code}", style="bold blue")
        text.append("\n")
        text.append("\n")
        text.append("Precio: ")
        text.append(f"{self.price}", style="bold green")
        text.append("\n")
        text.append("Descuento: ")
        if self.get_discount_amount() > 0:
            text.append(f"-{self.get_discount_amount()}", style="bold yellow")
        else:
            text.append(f"{self.get_discount_amount()}", style="bold green")
        text.append("\n")
        text.append("Subtotal: ")
        text.append(f"{self.price - self.get_discount_amount()}", style="bold green")
        text.append("\n")
        text.append("Impuesto: ")
        text.append(f"+{self.get_tax_amount()}", style="bold red")
        text.append("\n")
        text.append("Total: ")
        text.append(f"{self.get_total_price()}", style="bold green")

        return text

    def show_ticket_table_form(self):

        table = Table(title=Text("Ticket Virtual", style="bold red"), show_header=False)
        table.add_column()
        table.add_column(justify="right", vertical="bottom")
        text = Text()
        text.append("Nombre: ")
        text.append(f"{self.customer.full_name.title()}", style="bold blue")
        text.append("\n")
        text.append("Juego: ")
        text.append(f"{self.match.home.name.title()}", style="bold blue")
        text.append(" vs ")
        text.append(f"{self.match.away.name.title()}", style="bold blue")
        text.append("\n")
        text.append("Grupo: ")
        text.append(f"{self.match.group}", style="bold blue")
        text.append("\n")
        text.append("Estadio:")
        text.append(f"{self.match.stadium.name.title()}", style="bold blue")
        text.append("\n")
        text.append("Fecha: ")
        text.append(f"{self.match.date.strftime('%d/%m/%Y')}", style="bold blue")
        text.append("\n")
        text.append("Tipo: ")
        if self.type == "vip":
            text.append(f"{self.type.capitalize()}", style="bold gold3")
        else:
            text.append(f"{self.type.capitalize()}", style="bold blue")
        text.append("\n")
        text.append("Asiento: ")
        text.append(f"{self.seat.code()}", style="bold blue")
        text.append("\n")
        text.append("Código Seguridad: ")
        text.append(f"{self.code}", style="bold blue")
        text1 = text

        text = Text()
        text.append("Precio: ")
        text.append(f"{self.price}", style="bold green")
        text.append("\n")
        text.append("Descuento: ")
        if self.get_discount_amount() > 0:
            text.append(f"-{self.get_discount_amount()}", style="bold yellow")
        else:
            text.append(f"{self.get_discount_amount()}", style="bold green")
        text.append("\n")
        text.append("Subtotal: ")
        text.append(f"{self.price - self.get_discount_amount()}", style="bold green")
        text.append("\n")
        text.append("Impuesto: ")
        text.append(f"+{self.get_tax_amount()}", style="bold red")
        text.append("\n")
        text.append("Total: ")
        text.append(f"{self.get_total_price()}", style="bold green")
        text2 = text

        table.add_row(text1, text2)

        return table


class TicketManager:
    DATA_FILENAME = "tickets.json"

    def __init__(self, tickets=None):
        if tickets is None:
            self.tickets = []
        else:
            self.tickets = tickets

    def add_ticket(self, ticket):
        if ticket not in self.tickets:
            self.tickets.append(ticket)

    def remove_ticket(self, ticket):
        if ticket in self.tickets:
            self.tickets.remove(ticket)

    def get_tickets_by_match(self, match):
        return [ticket for ticket in self.tickets if ticket.match == match]

    def get_tickets_by_customer(self, customer):
        return [ticket for ticket in self.tickets if ticket.customer == customer]

    def get_tickets_by_type(self, ticket_type):
        return [ticket for ticket in self.tickets if ticket.type == ticket_type]

    def get_ticket_by_stadium(self, stadium):
        tickets_for_stadium = []
        for ticket in self.tickets:
            if ticket.match.stadium == stadium:
                tickets_for_stadium.append(ticket)
        return tickets_for_stadium

    def get_ticket_by_code(self, code):
        for ticket in self.tickets:
            if ticket.code.upper() == code.upper():
                return ticket

    def load_tickets_data(self, customer_manager, match_manager, stadium_manager):
        if not os.path.exists(self.DATA_FILENAME):
            return
        with open(self.DATA_FILENAME, "r", encoding="utf-8") as fh:
            tickets_data = json.load(fh)
        self.tickets = []
        for item in tickets_data:
            ident = item["ident"]
            customer = customer_manager.get_customer_by_ident(ident)
            match_id = item["match_id"]
            match = match_manager.get_match_by_id(match_id)
            seat_code = item["seat_code"]
            stadium = match.stadium
            seat = stadium.seat_by_code(seat_code)
            code = item["code"]
            used = item["used"]
            ticket = Ticket(customer, match, seat, code, used)
            self.add_ticket(ticket)

    def save_tickets_data(self):
        tickets_data = []
        for ticket in self.tickets:
            item = {
                "ident": ticket.customer.ident,
                "match_id": ticket.match.id,
                "seat_code": ticket.seat.code(),
                "code": ticket.code,
                "used": ticket.used,
            }
            tickets_data.append(item)
        with open(self.DATA_FILENAME, "w", encoding="utf-8") as fh:
            json.dump(tickets_data, fh, indent=4)

    def del_data_file(self):
        if os.path.exists(self.DATA_FILENAME):
            os.remove(self.DATA_FILENAME)
