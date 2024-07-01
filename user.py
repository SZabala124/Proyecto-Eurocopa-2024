import json
import os


class User:
    USER_TYPES = ["admin", "seller", "security"]

    def __init__(self, fullname, user_id, password, type):
        if not isinstance(fullname, str):
            raise TypeError("Full name must be a str.")
        if not fullname:
            raise ValueError("Full name cannot be empty.")
        self.fullname = fullname
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a str.")
        if not user_id:
            raise ValueError("User ID cannot be empty.")
        self.user_id = user_id.lower()
        if not isinstance(password, str):
            raise TypeError("Password must be a str.")
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password = password
        if not isinstance(type, str):
            raise TypeError("Type must be a str.")
        if type.lower() not in self.USER_TYPES:
            raise ValueError("Invalid user type.")
        self.type = type.lower()

    def __str__(self):
        return f"{self.fullname.title()}:{self.user_id}:{self.type.title()}"

    def __repr__(self):
        return f"User('{self.fullname}', '{self.user_id}', '{self.password}', '{self.type}')"


class UserManager:
    """Class that create a users manager."""

    DATA_FILENAME = "users.json"
    FIRST_ADMIN = {
        "fullname": "Admin User",
        "user_id": "admin123",
        "password": "password123",
        "type": "admin",
    }

    def __init__(self):
        """Constructor"""
        self.users = []
        first_admin_user = User(**self.FIRST_ADMIN)
        self.users.append(first_admin_user)

    def add_user(self, user):
        """Add a user to the user manager list of users.

        Args:
            user (User): the user to be added.

        Raises:
            TypeError: if the user is not a User obj.
            ValueError: if the user ID already exists.
        """
        if not isinstance(user, User):
            raise TypeError("User must be an instance of User.")
        found = False
        for item in self.users:
            if item.user_id.lower() == user.user_id.lower():
                found = True
                break
        if found:
            raise ValueError("User ID already exists.")
        self.users.append(user)

    def remove_user(self, user):
        """Removes a user from the user manager list.

        Args:
            user (user): the user to remove.

        Raises:
            TypeError: if user is not a User obj.
        """
        if not isinstance(user, User):
            raise TypeError("User must be an instance of User.")
        if user in self.users:
            self.users.remove(user)

    def get_user_by_id(self, user_id):
        """Returns the user associated with the given user_id.

        Args:
            user_id (str): the id of the user to retrieve.

        Raises:
            TypeError: if the user_id is not a str.

        Returns:
            User: the user associated with the given user_id or None if
                the user is not in the list of users.
        """
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a str.")
        for user in self.users:
            if user.user_id.lower() == user_id.lower():
                return user
        return None

    def authenticate(self, user_id, password):
        """Returns True if the user is authenticated.

        Args:
            user_id (str): the ID of the user to be authenticated.
            password (str): the password to be used.

        Raises:
            TypeError: if the user_id or the password are not strs.

        Returns:
            bool: True if the user is authenticated or False otherwise.
        """
        if not isinstance(user_id, str) or not isinstance(password, str):
            raise TypeError("User ID and Password must be str.")
        user = self.get_user_by_id(user_id)
        if user and user.password == password:
            return True
        return False

    def load_users_data(self):
        if not os.path.exists(self.DATA_FILENAME):
            return
        with open(self.DATA_FILENAME, "r", encoding="utf-8") as fh:
            users_data = json.load(fh)
        self.users = []
        for item in users_data:
            full_name = item["full_name"]
            user_id = item["user_id"]
            password = item["password"]
            type = item["type"]
            user = User(full_name, user_id, password, type)
            self.add_user(user)

    def save_users_data(self):
        users_data = []
        for user in self.users:
            users_data.append(
                {
                    "full_name": user.fullname,
                    "user_id": user.user_id,
                    "password": user.password,
                    "type": user.type,
                }
            )
        with open(self.DATA_FILENAME, "w", encoding="utf-8") as fh:
            json.dump(users_data, fh, indent=4)

    def del_data_file(self):
        if os.path.exists(self.DATA_FILENAME):
            os.remove(self.DATA_FILENAME)
