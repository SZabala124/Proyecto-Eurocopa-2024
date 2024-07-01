import os
from datetime import datetime
from math import ceil

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from constant import PANEL_OPTIONS, USER_ACCESS_BY_TYPE
from customer import Customer, CustomerManager
from match_and_team import MatchManager, TeamManager
from restaurant import Product, RestaurantManager
from sale import SaleManager
from stadium import Stadium, StadiumManager
from ticket import Ticket, TicketManager
from tools import prompt, prompt_float, prompt_int
from user import User, UserManager


class InterfaceManager:
    """Class that manage the user menu."""

    def __init__(self):
        self.console = Console()
        self.user_manager = UserManager()
        self.restaurant_manager = RestaurantManager()
        self.match_manager = MatchManager()
        self.customer_manager = CustomerManager()
        self.ticket_manager = TicketManager()
        self.products_sold = []
        self.team_manager = TeamManager()
        self.stadium_manager = StadiumManager()
        self.sale_manager = SaleManager()

        # self.user = None
        self.user = self.user_manager.get_user_by_id("admin123")  # QUITAR

        self.selected_customer = None
        self.selected_match = None
        self.selected_seat = None
        self.current_sale = None
        self.panel_options = PANEL_OPTIONS
        self.users_access = USER_ACCESS_BY_TYPE
        self.initializate_system()

        ############
        # QUITAR
        ############
        customer = Customer("santigo zabala", "31460195", 18)  # QUITAR
        self.customer_manager.customers.append(customer)  # QUITAR
        self.selected_customer = customer  # QUITAR
        code = "B63C44C9-014F-40D5-8F95-46F3A5139A12"
        match = self.match_manager.matches[0]
        match2 = self.match_manager.matches[1]
        stadium = match.stadium
        stadium2 = match2.stadium
        seat = stadium.seat_by_code("P01A0101")
        seat2 = stadium2.seat_by_code("P01A0101")
        code2 = "8CF9C9F8-0780-4372-ACEA-6FE6F87F8FC6"
        ticket = Ticket(customer, match, seat, code)
        ticket2 = Ticket(customer, match2, seat2, code2)
        self.ticket_manager.add_ticket(ticket)  # QUITAR
        self.ticket_manager.add_ticket(ticket2)  # QUITAR

        ############
        # Fin de QUITAR
        ############

    def initializate_system(self, reset=False):
        if reset:
            self.team_manager.del_data_file()
            self.stadium_manager.del_data_file()
            self.match_manager.del_data_file()
            self.user_manager.del_data_file()
            self.customer_manager.del_data_file()
            self.ticket_manager.del_data_file()
            self.sale_manager.del_data_file()
        self.team_manager.load_teams_data()
        self.stadium_manager.load_stadiums_data(self.restaurant_manager)
        self.match_manager.load_matches_data(self.team_manager, self.stadium_manager)
        self.user_manager.load_users_data()
        self.customer_manager.load_customers_data()
        self.ticket_manager.load_tickets_data(self.customer_manager, self.match_manager, self.stadium_manager)
        self.sale_manager.load_sales_data()

    def get_panel(self, text="", title="", panel_option_key=None, no_width=False, no_height=False):
        """Return a panel with the given text at the bottom of the panel and the
        salutation_text at the top of the panel.

        Args:
            text (str|Text, optional): the text to be at the bottom of the panel. Defaults to "".
            salutation_text (str|Text, optional): the text to be at the top of the panel. Defaults to "".
            title (str|Text, optional): the title of the panel. Defaults to "".
            panel_option_key (str, optional): the key to get the panel options. Defaults to None.

        Returns:
            Panel: the panel.
        """
        if panel_option_key and panel_option_key in self.panel_options:
            panel_options = self.panel_options[panel_option_key]["panel"].copy()
            min_lines = self.panel_options[panel_option_key]["min_lines"]
            max_lines = self.panel_options[panel_option_key]["max_lines"]
        else:
            panel_options = self.panel_options["default"]["panel"].copy()
            min_lines = self.panel_options["default"]["min_lines"]
            max_lines = self.panel_options["default"]["max_lines"]
        if no_width:
            panel_options["width"] = None
        if no_height:
            panel_options["height"] = None

        if self.user:
            salutation_text = Text()
            salutation_text.append(Text.from_markup(f"Bienvenido, [blue]{self.user.fullname}[/blue]\n"))
        else:
            salutation_text = Text()
            salutation_text.append(Text.from_markup("Bienvenido!\n"))

        footer_text = None
        if self.selected_customer and panel_option_key in ["tickets", "matches", "stadiums"]:
            footer_text = Text()
            name = self.selected_customer.full_name
            footer_text.append(Text.from_markup(f"Cliente: [green]{name.title()}[/green] "))
            if self.selected_match:
                match_text = f"{self.selected_match.code()} "
                footer_text.append(Text.from_markup(f"- [cyan]{match_text}[/cyan] "))
            if self.selected_seat:
                seat_text = f"{self.selected_seat.code()}"
                footer_text.append(Text.from_markup(f"- [green]{seat_text}[/green]\n"))

        elif self.selected_customer and panel_option_key in ["products"]:
            footer_text = Text()
            name = self.selected_customer.full_name
            footer_text.append(Text.from_markup(f"Cliente: [green]{name.title()}[/green] "))

        new_text = Text()
        new_text.append(salutation_text)
        new_text.append("\n")
        if text:
            num_lines = len(str(text).split("\n"))
            if num_lines <= min_lines:
                new_text.append("\n" * (max_lines - num_lines - 2))
            new_text.append(text)
        else:
            new_text.append("\n" * min_lines)
            panel_options["height"] = max_lines
        if not footer_text:
            return Panel(new_text, title=title, **panel_options)
        return Panel(new_text, title=title, subtitle=footer_text, subtitle_align="right", **panel_options)

    def main_menu(self):
        while True:
            os.system("cls")
            title = "Menú Principal"
            menu_text = Text()
            menu_options = {
                "1": "Iniciar Session",
                "2": "Administrar Usuarios",
                "3": "Inicializar Sistema",
                "4": "Administrar Clientes",
                "5": "Venta de Tickets",
                "6": "Validar Tickets",
                "7": "Venta de Productos",
                "8": "Generar Reportes",
                "9": "Guardar/Cargar",
                "10": "Cerrar Sesión",
                "s": "Salir",
            }
            if not self.user:
                type = None
            else:
                type = self.user.type
            user_allowed_choices = self.users_access[type]["main_menu"]
            for key, value in menu_options.items():
                if key in user_allowed_choices:
                    style = "green"
                else:
                    style = "red"
                menu_text.append(f"{key}: {value}", style=style)
                if key != "s":
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="users")
            self.console.print(panel)
            choice = prompt("Seleccione una opción", choices=[key for key in menu_options], show_choices=False)
            if choice not in user_allowed_choices:
                prompt(Text("No tienes acceso a esa opción. Pulse Enter para continuar...", style="red"))
                continue
            if choice == "1":
                self.login()
                continue
            elif choice == "2":
                self.user_management_menu()
                continue
            elif choice == "3":
                self.initializate_system(reset=True)
                continue
            elif choice == "4":
                self.customer_management_menu()
                continue
            elif choice == "5":
                self.ticket_sales_menu()
                continue
            elif choice == "6":
                self.validar_ticket()
                continue
            elif choice == "7":
                self.products_sales_menu()
                continue
            elif choice == "8":
                self.generar_reportes_menu()
                continue
            elif choice == "9":
                choice = prompt(
                    "Desea Guardar o Cargar la data del sistema. (c) para cancelar",
                    choices=(["guardar", "cargar", "c"]),
                )
                if choice.lower() == "cargar":
                    self.load_system_data()
                if choice.lower() == "guardar":
                    self.save_system_data()
                continue
            elif choice == "10":
                self.user = None
                continue
            elif choice == "s":
                self.console.print(Text("Hasta Luego...", style="blue"))
                prompt("Presione cualquier tecla para terminar...")
                break

    def login(self):
        title = "Iniciar Sesión"
        os.system("cls")
        if self.user:
            text = Text()
            text = Text.from_markup("[red]Ya tienes abierta la sesión!!!")
            self.console.print(text)
            return
        text = ""
        panel = self.get_panel(text, title=title, panel_option_key="users")
        self.console.print(panel)
        text = "Introduzca su user id"
        user_id = prompt(text)
        os.system("cls")
        text = Text.from_markup(f"User_id: [blue]{user_id}[/blue]")
        panel = self.get_panel(text, title=title, panel_option_key="users")
        self.console.print(panel)
        password = prompt("Introduzca su password")
        os.system("cls")
        text.append("\n")
        text.append(Text.from_markup(f"Password: [blue]{password}[/blue]"))
        panel = self.get_panel(text, title=title, panel_option_key="users")
        self.console.print(panel)
        if self.user_manager.authenticate(user_id, password):
            user = self.user_manager.get_user_by_id(user_id)
            if user:
                self.user = user
                text = "[yellow]Sesión abierta con éxito!!![/yellow]"
                self.console.print(Text.from_markup(text))
                text = "Presiona enter para continuar..."
                prompt(text)
                return
        text = "[red]User_id o Password incorrectos!!![/red]"
        self.console.print(Text.from_markup(text))
        text = "Presione enter para continuar..."
        prompt(text)
        self.user = None
        return

    def user_management_menu(self):
        while True:
            os.system("cls")
            title = "Administrar Usuarios"
            menu_text = Text()

            menu_options = {
                "1": "Agregar Usuario",
                "2": "Listar Usuarios",
                "3": "Modificar Password Usuario",
                "4": "Eliminar Usuario",
                "s": "Salir",
            }
            for key, value in menu_options.items():
                menu_text.append(f"{key}: {value}", style="green")
                if key != "s":
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="users")
            self.console.print(panel)
            choice = prompt("Seleccione una opción", choices=[key for key in menu_options], show_choices=False)
            if choice == "1":
                self.add_user()
                continue
            elif choice == "2":
                self.list_users()
                continue
            elif choice == "3":
                self.change_password()
                continue
            elif choice == "4":
                self.remove_user()
                continue
            elif choice == "s":
                break

    def add_user(self):
        title = "Crear Usuario"
        if self.user.type != "admin":
            text = "[red]No puedes crear un usuario ya que no eres Admin!!![/red]"
            self.console.print(Text.from_markup(text))
            text = "Presione enter para salir..."
            prompt(text)
            return
        os.system("cls")
        panel = self.get_panel(title=title, panel_option_key="users")
        self.console.print(panel)
        text = "Nombre completo del usuario"
        full_name = prompt(text).title()

        os.system("cls")
        text = f"Full Name: [blue]{full_name}[/blue]"
        panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="users")
        self.console.print(panel)
        text = "Introduzca el user id"
        user_id = prompt(text).lower()

        os.system("cls")
        text = f"Full Name: [blue]{full_name}[/blue]\n"
        text += f"User ID: [blue]{user_id}[/blue]"
        panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="users")
        self.console.print(panel)
        text = "Introduzca un password"
        password = prompt(text)

        os.system("cls")
        text = f"Full Name: [blue]{full_name}[/blue]\n"
        text += f"User ID: [blue]{user_id}[/blue]\n"
        text += f"Password: [blue]{password}[/blue]"
        panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="users")
        self.console.print(panel)
        text = "Seleccione el Tipo de Usuario"
        choices = [Text(choice, style="green") for choice in User.USER_TYPES]
        type_user = prompt(text, choices=choices)

        os.system("cls")
        text = f"Full Name: [blue]{full_name}[/blue]\n"
        text += f"User ID: [blue]{user_id}[/blue]\n"
        text += f"Password: [blue]{password}[/blue]\n"
        text += f"Tipo de Usuario: [blue]{type_user.title()}[/blue]"
        panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="users")
        self.console.print(panel)
        text = "¿Desea confirmar la creación del usuario?"
        if prompt(text, choices=["s", "n"]) == "s":
            try:
                user = User(full_name, user_id, password, type_user)
                self.user_manager.add_user(user)
                text = "[green]Usuario creado con éxito!!![/green]"
                self.console.print(Text.from_markup(text))
                text = "Presione enter para continuar..."
                prompt(text)
                return
            except ValueError:
                text = "[red]Ya existe un usuario con ese user_id!!![/red]"
                self.console.print(Text.from_markup(text))
                text = "Presione enter para continuar..."
                prompt(text)
                return
        else:
            text = "[red]No se a creado el usuario!!![/red]"
            self.console.print(Text.from_markup(text))
            text = "Presione enter para continuar..."
            prompt(text)
            return

    def list_users(self):
        os.system("cls")
        title = "Listado de Usuarios"
        text = Text()
        num_users = len(self.user_manager.users)
        for i, user in enumerate(self.user_manager.users):
            text.append(Text.from_markup(f"[blue]{user.fullname}[/blue] | "))
            text.append(Text.from_markup(f"[blue]{user.user_id}[/blue] | "))
            text.append(Text.from_markup(f"[blue]{user.password}[/blue] | "))
            text.append(Text.from_markup(f"[blue]{user.type}[/blue]"))
            if i < num_users - 1:
                text.append(Text("\n"))
        panel = self.get_panel(text, title=title, panel_option_key="users")
        self.console.print(panel)
        text = "Presione enter para continuar..."
        prompt(text)

    def remove_user(self):
        os.system("cls")
        title = "Eliminar Usuario"
        if self.user.type != "admin":
            text = "[red]No puedes eliminar un usuario ya que no eres Admin!!![/red]"
            self.console.print(Text.from_markup(text))
            text = "Presione enter para salir..."
            prompt(text)
            return
        panel = self.get_panel(title=title, panel_option_key="users")
        self.console.print(panel)
        text = "User ID"
        user_id = prompt(text).lower()
        user = self.user_manager.get_user_by_id(user_id)
        if user:
            os.system("cls")
            text = f"User ID: [blue]{user_id}[/blue]"
            panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="users")
            self.console.print(panel)
            text = "¿Desea confirmar la eliminación del usuario?"
            if prompt(text, choices=["s", "n"]) == "s":
                self.user_manager.remove_user(user)
                text = "[green]Usuario eliminado con éxito!!![/green]"
                self.console.print(Text.from_markup(text))
                text = "Presione enter para continuar..."
                prompt(text)
                return
            else:
                text = "[red]No se ha eliminado el usuario!!![/red]"
                self.console.print(Text.from_markup(text))
                text = "Presione enter para continuar..."
                prompt(text)
                return
        else:
            text = "[red]No existe un usuario con ese user_id!!![/red]"
            panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="users")
            self.console.print(panel)
            text = "Presione enter para continuar..."
            prompt(text)
            return

    def change_password(self):
        title = "Cambiar Password"
        if self.user.type != "admin":
            text = "[red]No puedes cambiar la contraseña de un usuario ya que no eres Admin!!![/red]"
            self.console.print(Text.from_markup(text))
            text = "Presione enter para continuar..."
            prompt(text)
            return
        os.system("cls")
        panel = self.get_panel(title=title, panel_option_key="users")
        self.console.print(panel)
        text = "User ID"
        user_id = prompt(text).lower()
        user = self.user_manager.get_user_by_id(user_id)
        if user:
            os.system("cls")
            text = f"User_id: [blue]{user_id}[/blue]"
            panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="users")
            self.console.print(panel)
            text = "Password"
            password = prompt(text)
            os.system("cls")
            text += f"User ID: [blue]{user_id}[/blue]\n"
            text += f"Password: [blue]{password}[/blue]\n"
            panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="users")
            self.console.print(panel)
            text = "¿Desea confirmar el cambio de password el usuario?"
            if prompt(text, choices=["s", "n"]) == "s":
                user.password = password
                text = "[green]Cambio de password exitoso!!![/green]"
                self.console.print(Text.from_markup(text))
                text = "Presione enter para continuar..."
                prompt(text)
                return
            text = "[red]No se a cambiado el password del usuario!!![/red]"
            self.console.print(Text.from_markup(text))
            text = "Presione enter para continuar..."
            prompt(text)
            return

    def customer_management_menu(self):
        while True:
            os.system("cls")
            title = "Administrar Clientes"
            menu_text = Text()

            menu_options = {
                "1": "Agregar Cliente",
                "2": "Listar Clientes",
                "3": "Eliminar Cliente",
                "s": "Salir",
            }
            for key, value in menu_options.items():
                menu_text.append(f"{key}: {value}", style="green")
                if key != "s":
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="customers")
            self.console.print(panel)
            choice = prompt("Seleccione una opción", choices=[key for key in menu_options], show_choices=False)
            if choice == "1":
                self.add_customer()
                continue
            elif choice == "2":
                self.list_customer()
                continue
            elif choice == "3":
                self.remove_customer()
                continue
            elif choice == "s":
                break

    def add_customer(self, ident=None):
        os.system("cls")
        title = "Agregar Cliente"
        panel_text = Text()
        panel = self.get_panel(title=title, panel_option_key="customers")
        self.console.print(panel)
        text = "Nombre completo del cliente"
        name = prompt(text).title()
        panel_text.append(Text.from_markup(f"Nombre: [blue]{name}[/blue]\n"))
        panel = self.get_panel(panel_text, title=title, panel_option_key="customers")
        os.system("cls")
        if not ident:
            self.console.print(panel)
            text = "Número de identidad"
            ident = prompt(text)
        panel_text.append(Text.from_markup(f"Ident: [blue]{ident}[/blue]\n"))
        panel = self.get_panel(panel_text, title=title, panel_option_key="customers")
        os.system("cls")
        self.console.print(panel)
        text = "Edad del Cliente"
        age = prompt_int(text)
        panel_text.append(Text.from_markup(f"Edad: [blue]{age}[/blue]\n"))
        panel = self.get_panel(panel_text, title=title, panel_option_key="customers")
        os.system("cls")
        self.console.print(panel)
        text = "¿Desea confirmar la creación del usuario?"
        if prompt(text, choices=["s", "n"]) == "s":
            customer = Customer(full_name=name, ident=ident, age=age)
            self.customer_manager.add_customer(customer)
            text = "[green]Cliente agregado con éxito!!![/green]"
            self.console.print(Text.from_markup(text))
            text = "Presione enter para continuar..."
            self.selected_customer = customer
            self.selected_match = None
            self.selected_seat = None
            prompt(text)
            return
        text = "[green]El cliente no fue agregado!!![/green]"
        self.console.print(Text.from_markup(text))
        text = "Presione enter para continuar..."
        prompt(text)

    def list_customer(self):
        os.system("cls")
        title = "Listar Clientes"
        customers = self.customer_manager.customers
        panel_text = Text()
        num_customers = len(customers)
        for index, customer in enumerate(customers, start=1):
            panel_text.append(
                Text.from_markup(
                    f"{index}. Nombre: [blue]{customer.full_name}[/blue], Ident: [blue]{customer.ident}[/blue], Edad: [blue]{customer.age}[/blue]"
                )
            )
            if index < num_customers:
                panel_text.append("\n")
        panel = self.get_panel(panel_text, title=title, panel_option_key="customers")
        self.console.print(panel)
        text = "Presione enter para continuar..."
        prompt(text)

    def remove_customer(self):
        os.system("cls")
        title = "Eliminar Cliente"
        panel_text = Text()
        panel = self.get_panel(panel_text, title=title, panel_option_key="customers")
        self.console.print(panel)
        text = "Número de identidad del cliente"
        ident = prompt(text)
        customer = self.customer_manager.get_customer_by_ident(ident)
        if customer:
            panel_text.append(
                Text.from_markup(f"Nombre: {customer.full_name}, Ident: {customer.ident}, Edad: {customer.age}")
            )
            os.system("cls")
            panel = self.get_panel(panel_text, title=title, panel_option_key="customers")
            self.console.print(panel)
            text = "¿Desea confirmar la eliminación del usuario?"
            if prompt(text, choices=["s", "n"]) == "s":
                self.customer_manager.remove_customer(customer)
                text = "[green]Cliente eliminado con éxito!!![/green]"
                if self.selected_customer.ident.lower() == customer.ident.lower():
                    self.selected_customer = None
                self.console.print(Text.from_markup(text))
                text = "Presione enter para continuar..."
                prompt(text)
                return
            text = "[green]El cliente no fue eliminado!!![/green]"
            self.console.print(Text.from_markup(text))
            text = "Presione enter para continuar..."
            prompt(text)
        else:
            text = "[red]No existe un cliente con el número de identidad dado."
            self.console.print(Text.from_markup(text))
            text = "Presione enter para continuar..."
            prompt(text)

    def ticket_sales_menu(self):
        while True:
            os.system("cls")
            title = "Ventas Tickets"
            menu_text = Text()
            menu_options = {
                "1": "Seleccionar Cliente",
                "2": "Seleccionar Partido",
                "3": "Seleccionar Asiento",
                "4": "Compra Ticket",
                "5": "Deseleccionar Cliente",
                "s": "Salir",
            }
            not_available_options = []
            if not self.selected_customer:
                not_available_options = ["2", "3", "4", "5"]
            elif not self.selected_match:
                not_available_options = ["3", "4"]
            elif not self.selected_seat:
                not_available_options = ["4"]
            for key, value in menu_options.items():
                if key not in not_available_options:
                    menu_text.append(f"{key}: {value}", style="green")
                else:
                    menu_text.append(f"{key}: {value}", style="red")
                if key != "s":
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="tickets")
            self.console.print(panel)
            choices = [key for key in menu_options.keys() if key not in not_available_options]
            choice = prompt("Seleccione una opción", choices=choices, show_choices=False)
            if choice == "1":
                self.select_customer()
                continue
            elif choice == "2":
                self.select_match_menu()
                continue
            elif choice == "3":
                self.select_piso()
                continue
            elif choice == "4":
                self.mostrar_ticket()
                continue
            elif choice == "5":
                self.selected_customer = None
                self.selected_match = None
                self.selected_seat = None
                text = "[green]Cliente deseleccionado con éxito!!![/green]"
                self.console.print(Text.from_markup(text))
                prompt("Presione cualquier tecla para continuar...")
                continue
            elif choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                break

    def select_customer(self):
        title = "Seleccionar Cliente"
        os.system("cls")
        panel = self.get_panel(title=title, panel_option_key="tickets")
        self.console.print(panel)
        text = "Número de identificación del cliente"
        ident = prompt(text)
        os.system("cls")
        panel_text = Text.from_markup(f"Ident: [blue]{ident}[/blue]")
        panel = self.get_panel(text, title=title, panel_option_key="users")
        self.console.print(panel)
        customer = self.customer_manager.get_customer_by_ident(ident)
        if customer:
            panel_text = f"Nombre: [blue]{customer.full_name}[/blue] "
            panel_text = f"Ident: [blue]{customer.ident}[/blue] "
            panel_text += f"Edad: [blue]{customer.age}[/blue]"
            panel = self.get_panel(Text.from_markup(panel_text), title=title, panel_option_key="tickets")
            os.system("cls")
            self.console.print(panel)
            text = "¿Deseas confirmar la selección del cliente?"
            if prompt(text, choices=["s", "n"]) == "s":
                self.selected_customer = customer
                self.selected_match = None
                self.selected_seat = None
                text = "[green]Cliente seleccionado con éxito!!![/green]"
                self.console.print(Text.from_markup(text))
                text = "Presione enter para continuar..."
                prompt(text)
                return
            text = "[red]El cliente no fue seleccionado!!![/red]"
            prompt(text)
            return
        text = "¿Deseas crear el cliente de es número de identidad?"
        if prompt(text, choices=["s", "n"]) == "s":
            self.add_customer(ident=ident)
            return
        text = "Presione enter para continuar..."
        prompt(text)
        self.selected_customer = None
        return

    def select_match_menu(self):
        while True:
            os.system("cls")
            title = "Seleccionar Partido"
            menu_text = Text()
            menu_options = {
                "1": "Partidos por País",
                "2": "Partidos por Estadio",
                "3": "Partidos por Fecha",
                "4": "Todos los Partidos",
                "s": "Salir",
            }
            for key, value in menu_options.items():
                menu_text.append(f"{key}: {value}", style="green")
                if key != "s":
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="matches")
            self.console.print(panel)
            choice = prompt("Seleccione una opción", choices=[key for key in menu_options], show_choices=False)
            if choice == "1":
                self.matches_by_country_menu()
                continue
            elif choice == "2":
                self.matches_by_stadium_menu()
                continue
            elif choice == "3":
                self.filter_matches_by_date()
                continue
            elif choice == "4":
                self.filter_matches_all()
                continue
            elif choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                break

    def matches_by_country_menu(self):
        while True:
            os.system("cls")
            title = "Países"
            countries = [team.name for team in self.team_manager.teams]
            menu_options = {str(index): value for index, value in enumerate(countries, start=1)}
            num_countries = len(countries)
            group_of = 12
            num_columns = ceil(num_countries / group_of)
            menu_text = Text()
            block = 50
            for i in range(group_of):
                for j in range(num_columns):
                    index = i + (group_of * j)
                    if index < num_countries:
                        menu_text.append(f"{index + 1}: {countries[index]}".ljust(block), style="green")
                if i < group_of - 1:
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="matches")
            self.console.print(panel)
            choices = [key for key in menu_options]
            choices.append("s")
            choice = prompt("Seleccione una opción o (s) para salir", choices=choices, show_choices=False)
            if choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                break
            else:
                self.filter_matches_by_country(country=menu_options[choice])
                continue

    def filter_matches_by_country(self, country):
        while True:
            os.system("cls")
            title = f"Partidos de {country}"
            panel = self.get_panel(title=title, panel_option_key="matches")
            self.console.print(panel)
            team = self.team_manager.get_team_by_name(country)
            if not team:
                text = f"No hay partidos en el equipo de {country}."
                self.console.print(Text.from_markup(text))
                prompt("Presione enter para continuar...")
                return
            matches = self.match_manager.get_matches_by_team(team)

            menu_options = {str(index): value for index, value in enumerate(matches, start=1)}
            num_matches = len(matches)
            group_of = 12
            num_columns = ceil(num_matches / group_of)
            menu_text = Text()
            block = 34
            for i in range(group_of):
                for j in range(num_columns):
                    index = i + (group_of * j)
                    if index < num_matches:
                        menu_text.append(f"{index + 1}: {matches[index].team_vs_team()}".ljust(block), style="green")
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="matches")
            os.system("cls")
            self.console.print(panel)
            choices = [key for key in menu_options]
            choices.append("s")
            choice = prompt("Seleccione una opción o (s) para salir", choices=choices, show_choices=False)
            if choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                break
            else:
                text = "¿Desea confirmar la selección del partido?"
                if prompt(text, choices=["s", "n"]) == "s":
                    self.selected_match = menu_options[choice]
                    text = "[green]Partido seleccionado con éxito!!![/green]"
                    self.console.print(Text.from_markup(text))
                    text = "Presione enter para continuar..."
                    prompt(text)
                    return
                text = "[red]El partido no fue seleccionado!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                return

    def matches_by_stadium_menu(self):
        while True:
            os.system("cls")
            title = "Stadiums"
            stadiums = [stadium.name for stadium in self.stadium_manager.stadiums]
            menu_options = {str(index): value for index, value in enumerate(stadiums, start=1)}
            num_stadiums = len(stadiums)
            group_of = 5
            num_columns = ceil(num_stadiums / group_of)
            menu_text = Text()
            block = 50
            for i in range(group_of):
                for j in range(num_columns):
                    index = i + (group_of * j)
                    if index < num_stadiums:
                        menu_text.append(f"{index + 1}: {stadiums[index]}".ljust(block), style="green")
                if i < group_of - 1:
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="matches")
            self.console.print(panel)
            choices = [key for key in menu_options]
            choices.append("s")
            choice = prompt("Seleccione una opción o (s) para salir", choices=choices, show_choices=False)
            if choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                break
            else:
                self.filter_matches_by_stadium(stadium_name=menu_options[choice])
                continue

    def filter_matches_by_stadium(self, stadium_name):
        while True:
            os.system("cls")
            title = f"Partidos en el Estadio: {stadium_name}"
            panel = self.get_panel(title=title, panel_option_key="matches")
            self.console.print(panel)

            stadium = self.stadium_manager.get_stadium_by_name(stadium_name)
            if not stadium:
                text = f"No hay partidos en el estadio {stadium_name}."
                self.console.print(Text.from_markup(text))
                prompt("Presione enter para continuar...")
                return
            matches = self.match_manager.get_matches_by_stadium(stadium)
            menu_options = {str(index): value for index, value in enumerate(matches, start=1)}
            num_matches = len(matches)
            group_of = 12
            num_columns = ceil(num_matches / group_of)
            menu_text = Text()
            block = 34
            for i in range(group_of):
                for j in range(num_columns):
                    index = i + (group_of * j)
                    if index < num_matches:
                        menu_text.append(f"{index + 1}: {matches[index].team_vs_team()}".ljust(block), style="green")
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="matches")
            os.system("cls")
            self.console.print(panel)
            choices = [key for key in menu_options]
            choices.append("s")
            choice = prompt("Seleccione una opción o (s) para salir", choices=choices, show_choices=False)
            if choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                break
            else:
                text = "¿Desea confirmar la selección del partido?"
                if prompt(text, choices=["s", "n"]) == "s":
                    self.selected_match = menu_options[choice]
                    text = "[green]Partido seleccionado con éxito!!![/green]"
                    self.console.print(Text.from_markup(text))
                    text = "Presione enter para continuar..."
                    prompt(text)
                    return
                text = "[red]El partido no fue seleccionado!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                return

    def filter_matches_by_date(self):
        while True:
            os.system("cls")
            title = "Partidos por fecha"

            match_dates = []
            for match in self.match_manager.matches:
                match_dates.append(match.date)
            min_date = min(match_dates)
            max_date = max(match_dates)
            min_date_str = min_date.strftime("%Y-%m-%d")
            max_date_str = max_date.strftime("%Y-%m-%d")
            text = f"Fechas entre: [blue]{min_date_str}[/blue] y [blue]{max_date_str}[/blue]"
            panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="matches")
            self.console.print(panel)
            match_date = prompt("Introduzca la fecha deseada (s) para Salir")
            if match_date.lower() == "s":
                prompt("Presione cualquier tecla para continuar...")
                return
            try:
                match_date = datetime.strptime(match_date, "%Y-%m-%d").date()
            except ValueError:
                text = "[red]Formato de fecha incorrecto. Debe ser YYYY-MM-DD!!![/red]"
                self.console.print(Text.from_markup(text))
                prompt("Presione enter para continuar...")
                continue
            matches = self.match_manager.get_matches_by_date(match_date)
            num_matches = len(matches)
            menu_options = {str(i): value for i, value in enumerate(matches, start=1)}
            menu_text = Text()
            for key, value in menu_options.items():
                menu_text.append(f"{key}: {value.team_vs_team()}", style="green")
                if int(key) < num_matches:
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="matches")
            os.system("cls")
            self.console.print(panel)
            choices = [key for key in menu_options.keys()]
            choices.append("s")
            choice = prompt("Seleccione una opción o (s) para salir", choices=choices, show_choices=False)
            if choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                break
            else:
                text = "¿Desea confirmar la selección del partido?"
                if prompt(text, choices=["s", "n"]) == "s":
                    self.selected_match = matches[int(choice) - 1]
                    text = "[green]Partido seleccionado con éxito!!![/green]"
                    self.console.print(Text.from_markup(text))
                    text = "Presione enter para continuar..."
                    prompt(text)
                    return
                text = "[red]El partido no fue seleccionado!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                return

    def filter_matches_all(self):
        while True:
            os.system("cls")
            title = "Todos los partidos"

            panel = self.get_panel(title=title, panel_option_key="matches")
            self.console.print(panel)
            matches = self.match_manager.matches
            menu_options = {str(index): value for index, value in enumerate(matches, start=1)}
            num_matches = len(matches)
            group_of = 12
            num_columns = ceil(num_matches / group_of)
            menu_text = Text()
            block = 34
            for i in range(group_of):
                for j in range(num_columns):
                    index = i + (group_of * j)
                    if index < num_matches:
                        menu_text.append(f"{index + 1}: {matches[index].team_vs_team()}".ljust(block), style="green")
                menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="matches")
            os.system("cls")
            self.console.print(panel)
            choices = [key for key in menu_options]
            choices.append("s")
            choice = prompt("Seleccione una opción o (s) para salir", choices=choices, show_choices=False)
            if choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                break
            else:
                text = "¿Desea confirmar la selección del partido?"
                if prompt(text, choices=["s", "n"]) == "s":
                    self.selected_match = menu_options[choice]
                    text = "[green]Partido seleccionado con éxito!!![/green]"
                    self.console.print(Text.from_markup(text))
                    text = "Presione enter para continuar..."
                    prompt(text)
                    return
                text = "[red]El partido no fue seleccionado!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                return

    def select_piso(self):
        while True:
            os.system("cls")
            stadium = self.selected_match.stadium
            title = "Estadio: {stadium.name}"
            num_floors = stadium.num_floors
            if num_floors == 1:
                self.select_locations(stadium, floor=1)
                return
            panel = self.get_panel(title=title, panel_option_key="stadiums")
            self.console.print(panel)
            floors = [str(floor) for floor in range(num_floors + 1, start=1)]
            floors.append("s")
            floor = prompt("(s) Salir o Seleccione el piso del estadio:", choices=floors, show_choices=True)
            if floor.lower() == "s":
                prompt("Presione cualquier tecla para continuar...")
                return
            text = "¿Desea confirmar la selección del piso?"
            if prompt(text, choices=["s", "n"]) == "s":
                self.select_location(stadium, floor=floor)
                return
            text = "[red]El piso no fue seleccionado!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            continue

    def select_locations(self, stadium, floor):
        while True:
            os.system("cls")
            title = f"Estadio: {stadium.name} piso: {floor}"
            table = stadium.get_stadium_locations_and_sections_info_table_format(floor=floor)
            name = self.selected_customer.full_name
            subtitle_text = f"Cliente:[green]{name.title()}[/green] "
            match_text = self.selected_match.code()
            subtitle_text += f"- [cyan]{match_text}[/cyan]"
            panel = Panel(table, title=title, subtitle=subtitle_text, subtitle_align="right", height=None, width=189)
            self.console.print(panel)
            floor_sections = stadium.sections_by_floor(floor=floor)
            sections_letters = {section.letter.lower() for section in floor_sections}
            locations = []
            if "a" in sections_letters:
                locations.append("frontal")
            if "d" in sections_letters:
                locations.append("trasera")
            if "g" in sections_letters:
                locations.append("izquierda")
            if "h" in sections_letters:
                locations.append("derecha")
            choices = locations
            choices.append("s")
            location = prompt("Seleccione una Ubicación o (s) para Salir", choices=choices, show_choices=True)
            if location.lower() == "s":
                prompt("Presione cualquier tecla para continuar...")
                return
            text = "¿Desea confirmar la selección de la sección?"
            if prompt(text, choices=["s", "n"]) == "s":
                self.select_section_row_seat(stadium=stadium, floor=floor, location=location.lower())
                return
            text = "[red]La sección no fue seleccionada!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            continue

    def select_section_row_seat(self, stadium, floor, location):
        for key, value in Stadium.LOCATION_DICT.items():
            if value.lower() == location.lower():
                location = key
        while True:
            os.system("cls")
            title = f"Estadio: {stadium.name.title()} - {floor} - {Stadium.LOCATION_DICT[location].title()} "
            table = stadium.get_stadium_location_section_titles_and_info_table_format(
                floor=floor, location=location, match=self.selected_match
            )
            name = self.selected_customer.full_name
            subtitle_text = f"Cliente:[green]{name.title()}[/green] "
            match_text = self.selected_match.code()
            subtitle_text += f"- [cyan]{match_text}[/cyan]"
            panel = Panel(table, title=title, subtitle=subtitle_text, subtitle_align="right", height=None, width=189)
            self.console.print(panel)
            floor_location_sections = stadium.sections_by_location(floor, location)
            if not floor_location_sections:
                text = "[red]No hay secciones disponibles en la ubicación seleccionada!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                return
            sections_letters = [section.letter.lower() for section in floor_location_sections]
            choices = sections_letters
            choices.append("s")
            letter = prompt("Seleccione una sección o (s) para Salir", choices=choices, show_choices=False).lower()
            if letter.lower() == "s":
                prompt("Presione cualquier tecla para continuar...")
                return
            os.system("cls")
            self.console.print(panel)
            text = f"[green]Section:[/green] [blue]{letter.upper()}[/blue]"
            self.console.print(text)
            text = f"¿Desea confirmar la selección de la sección: {letter.upper()}?"
            if prompt(text, choices=["s", "n"]) == "s":
                section = [section for section in floor_location_sections if section.letter.lower() == letter.lower()][
                    0
                ]
            else:
                text = "[red]La sección no fue seleccionada!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                continue
            os.system("cls")
            self.console.print(panel)
            text = f"[green]Section:[/green] [blue]{letter.upper()}[/blue]"
            self.console.print(Text.from_markup(text))

            rows = section.rows
            if not rows:
                text = "[red]No hay filas disponibles en la sección seleccionada!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                return
            choices = [str(row_num) for row_num in range(1, len(rows) + 1)]
            choices.append("s")
            text = f"Filas desde: [cyan]{choices[0]}[/cyan] hasta [cyan]{choices[-2]}[/cyan]"
            self.console.print(Text.from_markup(text))
            row_num = prompt("Seleccione una fila o (s) para Salir", choices=choices, show_choices=False)
            if row_num.lower() == "s":
                prompt("Presione cualquier tecla para continuar...")
                return
            os.system("cls")
            self.console.print(panel)
            text = f"[green]Section: [/green][blue]{letter.upper()}[/blue] "
            text += f"[green]Fila: [/green][blue]{row_num}[/blue]"
            self.console.print(text)
            text = f"¿Desea confirmar la selección de la fila: {row_num}?"
            if prompt(text, choices=["s", "n"]) == "n":
                text = "[red]La fila no fue seleccionada!!![/red]"
                self.console.print(Text.from_markup(text))
                prompt("Presione enter para continuar...")
                continue
            seats = [seat for seat in rows[int(row_num) - 1].seats]
            if not seats:
                text = "[red]No hay asientos disponibles en la fila seleccionada!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                return
            choices = [str(seat.number) for seat in seats]
            choices.append("s")
            text = f"Asientos desde: [cyan]{choices[0]}[/cyan] hasta [cyan]{choices[-2]}[/cyan]"
            self.console.print(Text.from_markup(text))
            seat_num = prompt("Seleccione un asiento o (s) para Salir", choices=choices, show_choices=False)
            if seat_num.lower() == "s":
                prompt("Presione cualquier tecla para continuar...")
                return
            os.system("cls")
            self.console.print(panel)
            text = f"[green]Section: [/green][blue]{letter.upper()}[/blue] "
            text += f"[green]Fila: [/green][blue]{row_num}[/blue] "
            text += f"[green]Asiento: [/green][blue]{seat_num}[/blue]"
            self.console.print(Text.from_markup(text))
            text = f"¿Desea confirmar la selección del asiento: {seat_num}?"
            if prompt(text, choices=["s", "n"]) == "n":
                text = "[red]El asiento no fue seleccionada!!![/red]"
                self.console.print(Text.from_markup(text))
                prompt("Presione enter para continuar...")
                continue
            self.selected_seat = seats[int(seat_num) - 1]
            if self.selected_seat.is_sold(self.selected_match):
                text = "[red]El asiento está vendido!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                self.selected_seat = None
                continue
            text = "Su reservación de asiento se ha realizado con éxito.\n"
            self.console.print(text)
            self.selected_seat = seats[int(seat_num) - 1]
            prompt("Presione enter para continuar...")
            return

    def mostrar_ticket(self):
        os.system("cls")
        title = f"Juego: {self.selected_match.code()} - {self.selected_seat.code()}"
        panel = self.get_panel(title=title, panel_option_key="tickets")
        self.console.print(panel)
        if self.selected_seat is None:
            text = "[red]No se ha seleccionado un asiento!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            return
        if self.selected_seat.is_sold(self.selected_match):
            text = "[red]El asiento está vendido!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            return
        title = Text()
        title.append(Text.from_markup(f"Bienvenido, [blue]{self.user.fullname}[/blue]\n"))
        subtitle_text = Text()
        name = self.selected_customer.full_name
        subtitle_text.append(Text.from_markup(f"Cliente: [green]{name.title()}[/green] "))
        match_text = f"{self.selected_match.code()} "
        subtitle_text.append(Text.from_markup(f"- [cyan]{match_text}[/cyan] "))
        seat_text = f"{self.selected_seat.code()}"
        subtitle_text.append(Text.from_markup(f"- [green]{seat_text}[/green]\n"))
        ticket = Ticket(self.selected_customer, self.selected_match, self.selected_seat)
        table = ticket.show_ticket_table_form()
        panel = Panel(table, title=title, subtitle=subtitle_text, subtitle_align="right", height=None, width=90)
        os.system("cls")
        self.console.print(panel)
        text = "¿Desea comprar la entrada?"
        if prompt(text, choices=["s", "n"]) == "n":
            text = "[red]La entrada no fue comprada!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            return
        self.selected_seat.sold(self.selected_match)
        self.ticket_manager.add_ticket(ticket)
        text = "La entrada se ha comprado con éxito.\n"
        self.console.print(text)
        prompt("Presione enter para continuar...")
        self.selected_seat = None
        return

    def validar_ticket(self):
        os.system("cls")
        title = "Validar Ticket"
        panel = self.get_panel(title=title, panel_option_key="security")
        self.console.print(panel)
        text = "Introduce el código del ticket"
        ticket_code = prompt(text)
        ticket = self.ticket_manager.get_ticket_by_code(ticket_code)
        if not ticket:
            text = "[red]El código del ticket no es válido!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            return
        if not ticket.validate(ticket_code):
            text = "[red]El ticket ya fue usado!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            return
        name = ticket.customer.full_name
        match_code = ticket.match.code()
        stadium = ticket.match.stadium.name
        seat_code = ticket.seat.code()
        text = "[green]Ticket válido![/green]\n"
        text += f"Bienvenido: [blue]{name.title()}[/blue] al estadio: [blue]{stadium}[/blue]\n"
        text += f"Partido: [cyan]{match_code}[/cyan] - Asiento: [green]{seat_code}[/green]\n"
        os.system("cls")
        panel = self.get_panel(Text.from_markup(text), title=title, panel_option_key="security")
        self.console.print(panel)
        prompt("Presione cualquier tecla para continuar...")

    def products_sales_menu(self):
        self.selected_match = None
        self.selected_seat = None
        self.selected_customer = None

        os.system("cls")
        title = "Ventas de Productos"
        panel = self.get_panel(title=title, panel_option_key="products")
        self.console.print(panel)
        text = "Introduce el código del ticket"
        ticket_code = prompt(text)
        ticket = self.ticket_manager.get_ticket_by_code(ticket_code)
        if not ticket:
            text = "[red]El código del ticket no es válido!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            return
        if ticket.type.lower() != "vip":
            text = "[red]El ticket no es VIP!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            return

        self.selected_customer = ticket.customer
        self.current_sale = self.sale_manager.add_sale(ticket)

        while True:
            menu_text = Text()
            menu_options = {
                "1": "Seleccionar Productos",
                "2": "Finalizar Compra",
                "s": "Salir",
            }
            not_available_options = []
            for key, value in menu_options.items():
                menu_text.append(f"{key}: {value}", style="green")
                if key != "s":
                    menu_text.append("\n")
            os.system("cls")
            panel = self.get_panel(menu_text, title=title, panel_option_key="products")
            self.console.print(panel)
            choices = [key for key in menu_options.keys() if key not in not_available_options]
            choice = prompt("Seleccione una opción", choices=choices, show_choices=False)
            if choice == "1":
                self.select_products_menu()
                continue
            elif choice == "2":
                self.end_sale()
                return
            elif choice == "s":
                self.sale_manager.remove_sale(self.current_sale)
                self.current_sale = None
                prompt("Presione cualquier tecla para continuar...")
                break

    def select_products_menu(self):
        while True:
            os.system("cls")
            title = "Seleccionar Filtro de Productos"
            menu_text = Text()
            menu_options = {
                "1": "Productos por Nombre",
                "2": "Productos por tipo",
                "3": "Partidos por Rango de Precios",
                "4": "Todos los Productos",
                "s": "Salir",
            }
            for key, value in menu_options.items():
                menu_text.append(f"{key}: {value}", style="green")
                if key != "s":
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="products")
            self.console.print(panel)
            choice = prompt("Seleccione una opción", choices=[key for key in menu_options], show_choices=False)
            if choice == "1":
                product_name = prompt("Introduzca el nombre comienzo del nombre")
                if not product_name:
                    text = "[red]Debe introducir un nombre!!![/red]"
                    self.console.print(text)
                    prompt("Presione enter para continuar...")
                    continue
                self.select_products(product_name=product_name)
                continue
            elif choice == "2":
                choices = Product.PRODUCT_TYPES
                type = prompt("Seleccione el tipo:", choices=choices)
                self.select_products(type=type)
                continue
            elif choice == "3":
                min_price = prompt_float("Introduzca el precio mínimo")
                max_price = prompt_float("Introduzca el precio máximo")
                self.select_products(min_price=min_price, max_price=max_price)
                continue
            elif choice == "4":
                self.select_products()
                continue
            elif choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                return

    def select_products(self, product_name=None, type=None, min_price=None, max_price=None):
        if product_name:
            filter = "name"
            filter_text = "[blue]Nombre[/blue]"
            title = f"Productos seleccionados por: {filter_text}: [blue]{product_name.title()}[/blue]"
        elif type:
            filter = "type"
            filter_text = "[blue]Tipo[/blue]"
            title = f"Productos seleccionados por: {filter_text}: [blue]{type.title()}[/blue]"
        elif min_price or max_price:
            if not min_price:
                min_price = 0.0
            if not max_price:
                max_price = 0.0
            min_price = float(min_price)
            max_price = float(max_price)
            filter = "price"
            filter_text = f"[blue]Precio[/blue]: [blue]{min_price:.2f} - {max_price:.2f}[/blue]"
            title = f"Productos seleccionados por: {filter_text}"
        else:
            filter = "Todos"
            filter_text = "[blue]Todos[/blue]"
            title = f"Productos seleccionados por: {filter_text}"
        while True:
            name = self.selected_customer.full_name
            subtitle_text = f"Cliente:[green]{name.title()}[/green] "
            ticket = self.current_sale.ticket
            match = ticket.match
            stadium = match.stadium
            restaurants = self.restaurant_manager.get_restaurants_by_stadium(stadium)
            if not restaurants:
                text = "[red]No hay restaurantes disponibles en este estadio!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                return
            products = []
            for restaurant in restaurants:
                products.extend(restaurant.products)
            if filter == "name":
                filtered_products = [product for product in products if product.name.lower().startswith(product_name)]
            elif filter == "type":
                filtered_products = [product for product in products if product.type.lower() == type.lower()]
            elif filter == "price":
                filtered_products = [product for product in products if min_price <= product.price <= max_price]
            else:
                filtered_products = products
            menu_options = ""
            num_options = len(filtered_products)
            for i in range(len(filtered_products)):
                product = filtered_products[i]
                name = product.name
                price = product.price
                type = product.type
                stock = product.stock
                menu_options += f"[green]{i+1}: {name.title()} ({type.title()}): {price} stock: {stock}[/green]\n"
            menu_options += "\n[blue]s: Salir[/blue]\n"
            menu_options = Text.from_markup(menu_options)
            panel = Panel(
                menu_options, title=title, subtitle=subtitle_text, subtitle_align="right", height=None, width=90
            )
            os.system("cls")
            self.console.print(panel)
            choices = [str(i) for i in range(1, num_options + 1)]
            choices.append("s")
            choice = prompt("Seleccione el número de producto", choices=choices, show_choices=False)
            if choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                return
            text = "¿Qué cantidad del producto?"
            amount = prompt(text)
            if not amount:
                text = "[red]Debe introducir una cantidad!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                continue
            amount = int(amount)
            if amount <= 0:
                text = "[red]Debe introducir una cantidad positiva!!![/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                continue
            product = filtered_products[int(choice) - 1]
            try:
                self.current_sale.add_product(product, amount)
                text = f"Se ha añadido {amount} unidades de {product.name.title()} al carrito"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                return
            except Exception as e:
                text = f"[red]{str(e)}[/red]"
                self.console.print(text)
                prompt("Presione enter para continuar...")
                continue

    def end_sale(self):
        os.system("cls")

        title = Text()
        title.append(Text.from_markup(f"Bienvenido, [blue]{self.user.fullname}[/blue]\n"))
        subtitle_text = Text()
        name = self.selected_customer.full_name
        subtitle_text.append(Text.from_markup(f"Cliente: [green]{name.title()}[/green] "))

        products = self.current_sale.sale_info
        if not products:
            os.system("cls")
            panel = self.get_panel(title=title, panel_option_key="products")
            self.console.print(panel)
            text = "[red]No hay productos en el carrito!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            return

        table = Table(title=f"Productos a comprar por el cliente: [green]{name.title()}")
        table.add_column("Cantidad", justify="left")
        table.add_column("Producto", justify="left")
        table.add_column("Precio", justify="right")
        for item in products:
            p_amount = Text.from_markup(f"[green]{item['amount']}[/green]")
            p_name = Text.from_markup(f"[green]{item['product'].title()}[/green]")
            p_price = Text.from_markup(f"[green]{item['price']}[/green]")
            table.add_row(
                p_amount,
                p_name,
                p_price,
            )

        total_info = self.current_sale.get_total_price_info()
        text = f"\n[green]Total Precios:[/green] [cyan]{total_info['total_price']}[/cyan]\n"
        text += f"[green]Total Descuentos:[/green] [yellow]{total_info['total_discount']}[/yellow]\n"
        text += f"[green]Total Impuestos:[/green] [red]{total_info['total_tax']}[/red]\n"
        text += f"[green]Total a Pagar:[/green] [cyan]{total_info['total_final_price']}[/cyan]\n"
        text = Text.from_markup(text)
        table.add_row("", "", text)

        panel = Panel(table, title=title, subtitle=subtitle_text, subtitle_align="right", height=None, width=90)
        os.system("cls")
        self.console.print(panel)
        text = "¿Desea pagar la compra?"
        if prompt(text, choices=["s", "n"]) == "n":
            text = "[red]La compra no fue efectuada!!![/red]"
            self.console.print(text)
            prompt("Presione enter para continuar...")
            return
        text = "[green]Gracias por su Compra[/green]"
        self.console.print(text)
        prompt("Presione enter para continuar...")
        self.sale_manager.sold(self.current_sale)
        self.sale_manager.remove_sale(self.current_sale)
        self.current_sale = None
        return

    def generar_reportes_menu(self):
        while True:
            os.system("cls")
            title = "Reportes"
            menu_text = Text()
            menu_options = {
                "1": "Promedio gasto de Cliente Vip por Partido (ticket + products)",
                "2": "Ranking Asistencia a los Partidos",
                "3": "Partido con mayor asistencia",
                "4": "Partido con mas boletos vendidos",
                "5": "Top 3 productos más vendidos en el restaurante",
                "6": "Top 3 clientes (boletos)",
                "s": "Salir",
            }
            for key, value in menu_options.items():
                menu_text.append(f"{key}: {value}", style="green")
                if key != "s":
                    menu_text.append("\n")
            panel = self.get_panel(menu_text, title=title, panel_option_key="matches")
            self.console.print(panel)
            choice = prompt("Seleccione una opción", choices=[key for key in menu_options], show_choices=False)
            if choice == "1":
                tickets = self.ticket_manager.tickets
                sales = self.sale_manager.sales_history
                tickets_vip = [ticket for ticket in tickets if ticket.type.lower() == "vip"]
                customers_idents = {ticket.customer.ident for ticket in tickets_vip}
                # sales_history = [item for item in sales]
                total_expenses_by_customer = {}
                for ticket in tickets:
                    customer_ident = ticket.customer.ident
                    if customer_ident not in total_expenses_by_customer:
                        total_expenses_by_customer[customer_ident] = 0.0
                    total_expenses_by_customer[customer_ident] += ticket.get_total_price()
                for customer_ident in customers_idents:
                    sales_by_customer = [item for item in sales if item["ident"] == customer_ident]
                    for sale in sales_by_customer:
                        total_expenses_by_customer[customer_ident] += sale["final_price"]
                total_expenses = sum([expenses for expenses in total_expenses_by_customer.values()])
                num_customers = len(total_expenses_by_customer)
                average_expenses = total_expenses / num_customers
                average_expenses = round(average_expenses, 2)
                text = "Promedio gasto de Clientes Vip por Partido (ticket + products):\n"
                text += f"Promedio: [cyan]{average_expenses}[/cyan]\n"
                text = Text.from_markup(text)
                os.system("cls")
                panel = self.get_panel(text, title=title, panel_option_key="matches")
                self.console.print(panel)
                prompt("Presione enter para continuar...")
                continue
            elif choice == "2":
                tickets = self.ticket_manager.tickets
                matches_info = {}
                for ticket in tickets:
                    if ticket.match not in matches_info:
                        matches_info[ticket.match] = {
                            "tickets_sold": 0,
                            "tickets_used": 0,
                        }
                        matches_info[ticket.match]["tickets_sold"] += 1
                        if ticket.is_used():
                            matches_info[ticket.match]["tickets_used"] += 1
                match_info_list = []
                for match, value in matches_info.items():
                    sold = value["tickets_sold"]
                    used = value["tickets_used"]
                    if not sold:
                        relation = 0.0
                    else:
                        relation = round(used / sold, 2)
                    item = [match.code(), match.stadium.name.title(), sold, used, relation]
                    match_info_list.append(item)
                match_info_list.sort(key=lambda x: x[4], reverse=True)
                table = Table(title="Ranking de asistencia")
                table.add_column("Partido")
                table.add_column("Estadio")
                table.add_column("Vendidos")
                table.add_column("Asistencia")
                table.add_column("Rel Asistencia")
                for item in match_info_list:
                    table.add_row(item[0], item[1], str(item[2]), str(item[3]), str(item[4]))
                os.system("cls")
                panel = Panel(table, title=title, height=None, width=100)
                self.console.print(panel)
                prompt("Presione enter para continuar...")
                continue
            elif choice == "3":
                tickets = self.ticket_manager.tickets
                matches_info = {}
                for ticket in tickets:
                    if ticket.match not in matches_info:
                        matches_info[ticket.match] = 0
                    matches_info[ticket.match] += 1
                match_info_list = []
                for match, value in matches_info.items():
                    item = [match.code(), match.stadium.name.title(), value]
                    match_info_list.append(item)
                match_info_list.sort(key=lambda x: x[2], reverse=True)
                if not match_info_list:
                    text = "No hay partidos registrados"
                    os.system("cls")
                    panel = self.get_panel(text, title=title, panel_option_key="matches")
                    self.console.print(panel)
                    prompt("Presione enter para continuar...")
                    continue
                text = "Partido con mayor asistencia:\n"
                match = match_info_list[0]
                text += f"Partido: {match[0]} - {match[1]} Asistencia: {match[2]}\n"
                os.system("cls")
                panel = self.get_panel(text, title=title, panel_option_key="matches")
                self.console.print(panel)
                prompt("Presione enter para continuar...")
                continue
            elif choice == "4":
                tickets = self.ticket_manager.tickets
                matches_info = {}
                for ticket in tickets:
                    if ticket.match not in matches_info:
                        matches_info[ticket.match] = 0
                    matches_info[ticket.match] += 1
                match_info_list = []
                for match, value in matches_info.items():
                    item = [match.code(), match.stadium.name.title(), value]
                    match_info_list.append(item)
                match_info_list.sort(key=lambda x: x[2], reverse=True)
                if not match_info_list:
                    text = "No hay partidos registrados"
                    os.system("cls")
                    panel = self.get_panel(text, title=title, panel_option_key="matches")
                    self.console.print(panel)
                    prompt("Presione enter para continuar...")
                    continue
                text = "Partido con mayor venta de boletos:\n"
                match = match_info_list[0]
                text += f"Partido: {match[0]} - {match[1]} Vendidos: {match[2]}\n"
                os.system("cls")
                panel = self.get_panel(text, title=title, panel_option_key="matches")
                self.console.print(panel)
                prompt("Presione enter para continuar...")
                continue
            elif choice == "5":
                sales = self.sale_manager.sales_history
                products_info = {}
                for sale in sales:
                    product = sale["product"]
                    if product not in products_info:
                        products_info[product] = 0
                    products_info[product] += sale["amount"]
                product_info_list = []
                for product, value in products_info.items():
                    item = [product, value]
                    product_info_list.append(item)
                product_info_list.sort(key=lambda x: x[1], reverse=True)
                if not product_info_list:
                    text = "No hay productos registrados"
                    os.system("cls")
                    panel = self.get_panel(text, title=title, panel_option_key="matches")
                    self.console.print(panel)
                    prompt("Presione enter para continuar...")
                    continue
                text = "Top de 3 productos mas vendidos\n"
                for i in range(3):
                    if i >= len(product_info_list):
                        break
                    product = product_info_list[i]
                    text += f"{i+1}. Producto: {product[0]} - Vendidos: {product[1]}\n"
                os.system("cls")
                panel = self.get_panel(text, title=title, panel_option_key="matches")
                self.console.print(panel)
                prompt("Presione enter para continuar...")
                continue
            elif choice == "6":
                tickets = self.ticket_manager.tickets
                tickets_by_customer = {}
                for ticket in tickets:
                    if ticket.customer not in tickets_by_customer:
                        tickets_by_customer[ticket.customer] = 0
                    tickets_by_customer[ticket.customer] += 1
                customers_info_list = []
                for customer, value in tickets_by_customer.items():
                    item = [customer, value]
                    customers_info_list.append(item)
                customers_info_list.sort(key=lambda x: x[1], reverse=True)
                if not customers_info_list:
                    text = "No hay clientes registrados"
                    os.system("cls")
                    panel = self.get_panel(text, title=title, panel_option_key="matches")
                    self.console.print(panel)
                    prompt("Presione enter para continuar...")

                text = "Top de 3 clientes con mayor cantidad de boletos:\n"
                for i in range(3):
                    if i >= len(customers_info_list):
                        break
                    customer = customers_info_list[i]
                    text += f"{i+1}. Cliente: {customer[0]} - Boletos: {customer[1]}\n"
                os.system("cls")
                panel = self.get_panel(text, title=title, panel_option_key="matches")
                self.console.print(panel)
                prompt("Presione enter para continuar...")
                continue
            elif choice == "s":
                prompt("Presione cualquier tecla para continuar...")
                return

    def save_system_data(self):
        self.team_manager.save_teams_data()
        self.stadium_manager.save_stadiums_data(self.restaurant_manager)
        self.match_manager.save_matches_data(self.team_manager, self.stadium_manager)
        self.user_manager.save_users_data()
        self.customer_manager.save_customers_data()
        self.ticket_manager.save_tickets_data()
        self.sale_manager.save_sales_data()

    def load_system_data(self):
        self.team_manager.load_teams_data()
        self.stadium_manager.load_stadiums_data(self.restaurant_manager)
        self.match_manager.load_matches_data(self.team_manager, self.stadium_manager)
        self.user_manager.load_users_data()
        self.customer_manager.load_customers_data()
        self.ticket_manager.load_tickets_data(self.customer_manager, self.match_manager, self.stadium_manager)
        self.sale_manager.load_sales_data()


if __name__ == "__main__":

    def prueba():
        uim = InterfaceManager()
        uim.main_menu()

    prueba()
