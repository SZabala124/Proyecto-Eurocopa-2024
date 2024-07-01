from stadium import Stadium


class Product:
    """Represents a product."""

    FOOD_TYPES = ["package", "plate"]
    BEVERAGE_TYPES = ["alcoholic", "non-alcoholic"]
    PRODUCT_TYPES = FOOD_TYPES + BEVERAGE_TYPES

    def __init__(self, name, quantity, price, type, stock):
        """Constructor for Product.

        Args:
            name (str): the name of the product.
            quantity (int): the quantity already sold of the product.
            price (float): the price of the product.
            type (str): the type of the product.
            stock (int): the stock of the product.

        Raises:
            TypeError: if name is not a str.
            TypeError: if quantity is not an int.
            ValueError: if quantity < 0.
            TypeError: if price is not a float.
            ValueError: if price < 0.
            TypeError: if type is not a str.
            ValueError: if type is not valid.
            TypeError: if stock is not an int.
            ValueError: fi stock < 0.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a str.")
        self.name = name.lower()
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an int.")
        if quantity < 0:
            raise ValueError("Quantity must be a positive integer.")
        self.quantity = quantity
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")
        if price <= 0:
            raise ValueError("Price must be a positive number.")
        self.price = round(float(price), 2)
        if not isinstance(type, str):
            raise TypeError("Type must be a str.")
        if type.lower() not in self.PRODUCT_TYPES:
            raise ValueError("Invalid product type.")
        self.type = type.lower()
        if not isinstance(stock, int):
            raise TypeError("Stock must be an int.")
        if stock < 0:
            raise ValueError("Stock must be a non-negative integer.")
        self.stock = stock

    def __repr__(self):
        """Return a string representation of the product."""
        return f"Product({self.name}, {self.quantity}, {self.price}, {self.type}, {self.stock})"

    def is_beverage(self):
        """Returns True if the product is a Beverage."""
        if self.type in self.BEVERAGE_TYPES:
            return True
        return False

    def is_alcoholic(self):
        """Returns True if the product is Alcoholic."""
        if self.type == "alcoholic":
            return True
        return False

    def is_food(self):
        """Returns True if the product is a Food."""
        if self.type in self.FOOD_TYPES:
            return True
        return False

    def is_package(self):
        """Returns True if the product is a Package."""
        if self.type == "package":
            return True
        return False

    def is_plate(self):
        """Returns True if the product is a Plate."""
        if self.type == "plate":
            return True
        return False

    def can_be_sold(self, amount):
        """Returns True if the product can be sold.

        Args:
            amount (int): the amount of product to be sold.

        Raises:
            TypeError: if amount is not an int.
            ValueError: if amount <= 0

        Returns:
            bool: True if there is enough stock to sell the product.
        """
        if not isinstance(amount, int):
            raise TypeError("Amount must be a int.")
        if amount <= 0:
            raise ValueError("Amount must be a positive integer.")
        if self.stock >= amount:
            return True
        return False

    def sold(self, amount):
        """Update the stock and quantity due to a sell of the product.

        Args:
            amount (int): The amount of the product that was sold.

        Raises:
            TypeError: if amount is not a int.
            ValueError: if amount <= 0.
            ValueError: if amount > stock.
        """
        if not isinstance(amount, int):
            raise TypeError("Amount must be a int.")
        if amount <= 0:
            raise ValueError("Amount must be a positive integer.")
        if self.stock < amount:
            raise ValueError("Not enough stock to sell the product.")
        self.stock -= amount
        self.quantity += amount


class Restaurant:
    """Represents a restaurant."""

    def __init__(self, name, stadium, products=None):
        """Constructor

        Args:
            name (str): The name of the restaurant.
            products (Product, optional): a list of Products. Defaults to None.

        Raises:
            TypeError: if name is not a str.
            TypeError: if product is not a list.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a str.")
        self.name = name.lower()
        if not isinstance(stadium, Stadium):
            raise TypeError("Stadium must be an instance of Stadium.")
        self.stadium = stadium
        if not products:
            products = []
        if not isinstance(products, list):
            raise TypeError("Products must be a list.")
        self.products = products

    def __repr__(self):
        """Return a string representation of the restaurant."""
        return f"Restaurant({self.name}, {self.stadium})"

    def add_product(self, product):
        """Adds a product to the list.

        Args:
            product (Product): the product to be added.

        Raises:
            TypeError: if the product is not a Product obj.
        """
        if not isinstance(product, Product):
            raise TypeError("Product must be an instance of Product.")
        if product not in self.products:
            self.products.append(product)

    def remove_product(self, product):
        """Removes a product from the list.

        Args:
            product (Product): if the product

        Raises:
            TypeError: if product is not a Product obj.
        """
        if not isinstance(product, Product):
            raise TypeError("Product must be an instance of Product.")
        if product in self.products:
            self.products.remove(product)

    def get_product_by_name(self, name):
        """Returns the product of the given product's name.

        Args:
            name (str): the product's name to look for.

        Raises:
            TypeError: if name if not a str.

        Returns:
            Product: the product of the given name
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a str.")
        for product in self.products:
            if product.name == name.lower():
                return product

    def get_products_starts_with(self, name):
        """Returns all products that start with the given name.

        Args:
            name (str): the product's name to look for.

        Raises:
            TypeError: if name is not a str.
            ValueError: if name is an empty str.

        Returns:
            list: a list of products that start with the given name
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a str.")
        if not name:
            raise ValueError("Name cannot be an empty string.")
        return [product for product in self.products if product.name.lower().startswith(name.lower())]

    def get_product_by_price_range(self, max_price, min_price=0.0):
        """Returns all products within the given price range.

        Args:
            max_price (float): the maximum price to look for.
            min_price (float, optional): the minimum price to look for. Defaults to 0.0.

        Raises:
            TypeError: if max_price is not a int or float.
            ValueError: if max_price < 0.
            TypeError: if min_price is not a int or float.
            ValueError if min_price < 0.

        Returns:
            list: a list of products within the given price range.
        """
        if not isinstance(max_price, (int, float)):
            raise TypeError("Max price must be a number.")
        if max_price < 0:
            raise ValueError("Max price must be a positive number.")
        if not isinstance(min_price, (int, float)):
            raise TypeError("Min price must be a number.")
        if min_price < 0:
            raise ValueError("Min price must be a positive number.")
        return [product for product in self.products if min_price <= product.price <= max_price]

    def get_products_by_type(self, type):
        """Returns all products of the given type.

        Args:
            type (str): the type to look for.

        Raises:
            TypeError: if type is not a str.
            ValueError: if type is not valid.

        Returns:
            list: a list of products of the given type.
        """
        if not isinstance(type, str):
            raise TypeError("Type must be a str.")
        if type.lower() not in Product.PRODUCT_TYPES:
            raise ValueError("Invalid product type.")
        return [product for product in self.products if product.type.lower() == type.lower()]


class RestaurantManager:
    def __init__(self):
        self.restaurants = []

    def add_restaurant(self, restaurant):
        if not isinstance(restaurant, Restaurant):
            raise TypeError("Restaurant must be an instance of Restaurant.")
        if restaurant not in self.restaurants:
            self.restaurants.append(restaurant)

    def remove_restaurant(self, restaurant):
        if not isinstance(restaurant, Restaurant):
            raise TypeError("Restaurant must be an instance of Restaurant.")
        if restaurant in self.restaurants:
            self.restaurants.remove(restaurant)

    def get_restaurant_by_name(self, name):
        for restaurant in self.restaurants:
            if restaurant.name == name.lower():
                return restaurant
        return None

    def get_restaurants_starts_with(self, name):
        return [restaurant for restaurant in self.restaurants if restaurant.name.lower().startswith(name.lower())]

    def get_restaurants_by_stadium(self, stadium):
        if not isinstance(stadium, Stadium):
            raise TypeError("Stadium must be an instance of Stadium.")
        return [restaurant for restaurant in self.restaurants if restaurant.stadium == stadium]

    def load_restaurants_data(self, stadium, data):
        for restaurant in data:
            products = restaurant["products"]
            product_list = []
            for product_item in products:
                product = Product(
                    name=product_item["name"],
                    quantity=int(product_item["quantity"]),
                    price=float(product_item["price"]),
                    type=product_item["adicional"],
                    stock=int(product_item["stock"]),
                )
                product_list.append(product)
            restaurant = Restaurant(name=restaurant["name"], stadium=stadium, products=product_list)
            self.add_restaurant(restaurant)

    def save_restaurants_data(self, stadium):
        restaurants_data = []
        for restaurant in self.get_restaurants_by_stadium(stadium):
            restaurant_data = {}
            restaurant_data["name"] = restaurant.name
            products_data = []
            for product in restaurant.products:
                product_data = {}
                product_data["name"] = product.name
                product_data["quantity"] = product.quantity
                product_data["price"] = str(product.price)
                product_data["adicional"] = product.type
                product_data["stock"] = product.stock
                products_data.append(product_data)
            restaurant_data["products"] = products_data
            restaurants_data.append(restaurant_data)
        return restaurants_data
