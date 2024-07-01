import json
import os
import uuid

from constant import IVA


class Sale:
    DISCOUNTS = {
        "perfect": 15.0,
    }

    def __init__(self, ticket):
        self.ticket = ticket
        self.type = ticket.type
        if self.type.lower() != "vip":
            raise ValueError("Sale can only be made with VIP tickets.")
        self.customer = ticket.customer
        self.sale_info = []
        self.products = []
        self.customer = self.ticket.customer
        self.code = str(uuid.uuid4()).upper()
        self.sold = False

    def add_product(self, product, amount):
        if self.sold:
            raise ValueError("La venta ya se a pagado.")
        if not product.can_be_sold(amount):
            raise ValueError("No hay esa cantidad en el stock.")
        if not self.age_is_ok(product):
            raise ValueError("El cliente no puede comprar bebidas alcohólicas")
        product_info = {
            "code": self.code,
            "product": product.name,
            "amount": amount,
            "price": self.product_price(product, amount),
            "discounts": self.discount(product, amount),
            "tax": self.tax(product, amount),
            "final_price": self.final_price(product, amount),
            "is_alcoholic": product.is_alcoholic(),
            "product_type": product.type,
            "ident": self.customer.ident,
            "ticket_code": self.ticket.code,
        }
        self.sale_info.append(product_info)
        self.products.append({"product": product, "amount": amount})

    def age_is_ok(self, product):
        if product.is_alcoholic() and not self.customer.is_adult():
            return False
        return True

    def product_price(self, product, amount):
        return round(product.price * amount, 2)

    def discount(self, product, amount):
        if not self.customer.is_perfect():
            return 0.0
        price = self.product_price(product, amount)
        discount_amount = round(price * self.DISCOUNTS["perfect"] / 100, 2)
        return discount_amount

    def tax(self, product, amount):
        price = self.product_price(product, amount)
        discount = self.discount(product, amount)
        sub_total = price - discount
        tax = round(sub_total * IVA / 100)
        return tax

    def final_price(self, product, amount):
        price = self.product_price(product, amount)
        discount = self.discount(product, amount)
        tax = self.tax(product, amount)
        return round(price - discount + tax, 2)

    def get_total_price_info(self):
        total_price = 0
        total_discount = 0
        total_tax = 0
        total_final_price = 0
        for product_info in self.sale_info:
            total_price += product_info["price"]
            total_discount += product_info["discounts"]
            total_tax += product_info["tax"]
            total_final_price += product_info["final_price"]
        return {
            "total_price": float(total_price),
            "total_discount": float(total_discount),
            "total_tax": float(total_tax),
            "total_final_price": float(total_final_price),
        }

    def sell(self):
        self.sold = True
        for item in self.products:
            product = item["product"]
            amount = item["amount"]
            product.sold(amount)
        return self.sale_info


class SaleManager:
    DATA_FILENAME = "sales.json"

    def __init__(self):
        self.sales = []
        self.sales_history = []

    def add_sale(self, ticket):
        sale = Sale(ticket)
        self.sales.append(sale)
        return sale

    def remove_sale(self, sale):
        if sale in self.sales:
            self.sales.remove(sale)

    def get_sale_by_code(self, sale_code):
        for sale in self.sales:
            if sale.code == sale_code:
                return sale
        return None

    def add_product_to_sale(self, sale, product, amount):
        sale.add_product(product, amount)

    def sold(self, sale):
        sale_info = sale.sell()
        self.sales_history.extend(sale_info)

    def load_sales_data(self):
        if not os.path.exists(self.DATA_FILENAME):
            return
        self.sales_history = []
        with open(self.DATA_FILENAME, "r", encoding="utf-8") as fh:
            sales_data = json.load(fh)
        for item in sales_data:
            self.sales_history.append(item)

    def save_sales_data(self):
        with open(self.DATA_FILENAME, "w", encoding="utf-8") as fh:
            json.dump(self.sales_history, fh, indent=4)

    def del_data_file(self):
        if os.path.exists(self.DATA_FILENAME):
            os.remove(self.DATA_FILENAME)
