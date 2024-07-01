import json
import os

from perfect_number import is_perfect_number
from vampire_number import vampire_number


class Customer:
    """Definition for a customer."""

    def __init__(self, full_name, ident, age):
        """Initialize a customer.

        Args:
            full_name (str): the customer's name.
            ident (str|int): the customer's identification.
            age (int): the age of the customer.

        Raises:
            TypeError: if full_name is not a str.
            TypeError: if ident is not a int or a str.
            ValueError: if ident has not digits characters.
        """
        if not isinstance(full_name, str):
            raise TypeError("Full name must be a str.")
        self.full_name = full_name
        if not isinstance(ident, (str, int)):
            raise TypeError("Invalid ident")
        if isinstance(ident, str):
            if not ident.isdigit():
                raise ValueError("Invalid ident")
        self.ident = str(ident).strip()
        if not isinstance(age, int):
            raise TypeError("Age must be an int.")
        self.age = age
        self.vampire = None
        self.perfect = None

    def is_vampire(self):
        """Returns True if the customer's identification is a vampire number."""
        if self.vampire is None:
            self.vampire = vampire_number(self.ident)
        if self.vampire:
            return True
        return False

    def is_perfect(self):
        """Returns True if the customer's age is a perfect number."""
        if self.perfect is None:
            self.perfect = is_perfect_number(self.age)
        if self.perfect:
            return True
        return False

    def is_adult(self):
        """Returns True if the customer is an adult."""
        return self.age >= 18


class CustomerManager:
    """Manager for customers."""

    DATA_FILENAME = "customers.json"

    def __init__(self, customers=None):
        """Initialize the manager."""
        if not customers:
            customers = []
        if not isinstance(customers, list):
            raise TypeError("Customers must be a list.")
        self.customers = customers

    def add_customer(self, customer):
        """Add a customer to the manager."""
        if not isinstance(customer, Customer):
            raise TypeError("Customer must be an instance of Customer.")
        for item in self.customers:
            if item.ident.lower() == customer.ident.lower():
                return
        self.customers.append(customer)

    def remove_customer(self, customer):
        """Remove a customer from the manager."""
        if not isinstance(customer, Customer):
            raise TypeError("Customer must be an instance of Customer.")
        if customer in self.customers:
            self.customers.remove(customer)

    def get_customer_by_ident(self, ident):
        """Get a customer by their identification."""
        for customer in self.customers:
            if customer.ident.lower() == ident.lower():
                return customer
        return None

    def get_customer_by_name(self, name):
        """Get a customer by their full name."""
        for customer in self.customers:
            if customer.full_name.lower() == name.lower():
                return customer
        return None

    def get_customer_by_name_start_with(self, name):
        """Get customers whose full name starts with a given name."""
        return [customer for customer in self.customers if customer.full_name.lower().startswith(name.lower())]

    def load_customers_data(self):
        if not os.path.exists(self.DATA_FILENAME):
            return
        with open(self.DATA_FILENAME, "r", encoding="utf-8") as fh:
            customers_data = json.load(fh)
        self.customers = []
        for item in customers_data:
            customer = Customer(item["full_name"], item["ident"], item["age"])
            self.add_customer(customer)

    def save_customers_data(self):
        customers_data = []
        for customer in self.customers:
            customer_data = {
                "full_name": customer.full_name,
                "ident": customer.ident,
                "age": customer.age,
            }
            customers_data.append(customer_data)
        with open(self.DATA_FILENAME, "w", encoding="utf-8") as fh:
            json.dump(customers_data, fh, indent=4)

    def del_data_file(self):
        if os.path.exists(self.DATA_FILENAME):
            os.remove(self.DATA_FILENAME)
