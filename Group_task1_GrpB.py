from collections import defaultdict
from datetime import datetime
import pandas as pd
import pyarrow.feather as feather
import random

class Product:
    __slots__ = ['_product_id', 'name', 'category', 'price', '_stock', '_sales']

    def __init__(self, product_id, name, category, price, stock):
        self._product_id, self.name, self.category, self.price, self._stock = product_id, name, category, price, stock
        self._sales = 0

    def is_in_stock(self, quantity):
        return self._stock >= quantity

    def purchase(self, quantity):
        if self.is_in_stock(quantity):
            self._stock -= quantity
            self._sales += quantity
            return True
        return False

    def restock(self, quantity):
        self._stock += quantity

    def get_details(self):
        return f"{self.name} - Category: {self.category}, Price: ${self.price:.2f}, Stock: {self._stock}"

    def to_dict(self):
        return {
            'product_id': self._product_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'stock': self._stock,
            'sales': self._sales
        }

    @staticmethod
    def from_dict(data):
        product = Product(
            data['product_id'],
            data['name'],
            data['category'],
            data['price'],
            data['stock']
        )
        product._sales = data['sales']
        return product

    def __repr__(self):
        return f"Product({self._product_id}, {self.name}, {self.category}, {self.price}, {self._stock})"


# Sub-category class inheriting from Product
class Electronics(Product):
    __slots__ = ['warranty']

    def __init__(self, product_id, name, price, stock, warranty):
        super().__init__(product_id, name, 'Electronics', price, stock)
        self.warranty = warranty  # Public variable for electronics-specific warranty period

    def to_dict(self):
        data = super().to_dict()
        data['warranty'] = self.warranty
        return data

    @staticmethod
    def from_dict(data):
        return Electronics(
            data['product_id'],
            data['name'],
            data['price'],
            data['stock'],
            data['warranty']
        )

    def get_details(self):
        base_details = super().get_details()
        return f"{base_details}, Warranty: {self.warranty} months"

    def __repr__(self):
        return f"Electronics({self._product_id}, {self.name}, {self.price}, {self._stock}, {self.warranty})"


# Sub-category class inheriting from Product
class Kitchen(Product):
    __slots__ = ['energy_rating']

    def __init__(self, product_id, name, price, stock, energy_rating):
        super().__init__(product_id, name, 'Kitchen', price, stock)
        self.energy_rating = energy_rating  # Public variable for kitchen appliances' energy rating

    def to_dict(self):
        data = super().to_dict()
        data['energy_rating'] = self.energy_rating
        return data

    @staticmethod
    def from_dict(data):
        return Kitchen(
            data['product_id'],
            data['name'],
            data['price'],
            data['stock'],
            data['energy_rating']
        )

    def get_details(self):
        base_details = super().get_details()
        return f"{base_details}, Energy Rating: {self.energy_rating}"

    def __repr__(self):
        return f"Kitchen({self._product_id}, {self.name}, {self.price}, {self._stock}, {self.energy_rating})"


class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
        self.orders = defaultdict(list)

    def place_order(self, order):
        self.orders[order.order_id] = order

    def list_orders(self):
        return list(self.orders.keys())

    def to_dict(self):
        return {'customer_id': self.customer_id, 'name': self.name}

    @staticmethod
    def from_dict(data):
        return Customer(data['customer_id'], data['name'])

    def __repr__(self):
        return f"Customer({self.customer_id}, {self.name})"


class Order:
    def __init__(self, order_id, customer, products):
        self.order_id = order_id
        self.customer = customer
        self.products = products
        self.timestamp = datetime.now()

    def get_summary(self):
        total = sum(p['product'].price * p['quantity'] for p in self.products)
        product_list = ", ".join([f"{p['product'].name} (x{p['quantity']})" for p in self.products])
        return f"Order {self.order_id}: {product_list}, Total: ${total:.2f}, Timestamp: {self.timestamp}"

    def __repr__(self):
        return f"Order({self.order_id}, {self.customer}, {self.products})"


class Store:
    def __init__(self):
        self.products, self.customers, self.orders = {}, {}, defaultdict(list)
        self.next_order_id = 1

    def add_product(self, product):
        if product._product_id not in self.products:
            self.products[product._product_id] = product
            print(f"Product '{product.name}' added to the store.")
        else:
            print(f"Product '{product.name}' is already in the store.")

    def add_customer(self, customer_id, name):
        if customer_id not in self.customers:
            self.customers[customer_id] = Customer(customer_id, name)
            print(f"Customer '{name}' registered.")
        else:
            print(f"Customer '{name}' is already registered.")

    def save_and_load_customers(self, filepath='customers.feather'):
        """Save and then load customers to/from a Feather file for persistent storage."""
        data = pd.DataFrame([c.to_dict() for c in self.customers.values()])
        feather.write_feather(data, filepath)
        loaded_data = pd.read_feather(filepath)
        for _, row in loaded_data.iterrows():
            self.customers[row['customer_id']] = Customer.from_dict(row)

    def save_and_load_products(self, filepath='products.feather'):
        """Save and then load products to/from a Feather file for persistent storage."""
        data = pd.DataFrame([p.to_dict() for p in self.products.values()])
        feather.write_feather(data, filepath)
        loaded_data = pd.read_feather(filepath)
        for _, row in loaded_data.iterrows():
            category = row['category']
            if category == 'Electronics':
                product = Electronics.from_dict(row)
            else:
                product = Product.from_dict(row)
            self.products[row['product_id']] = product

    def emulate_random_orders(self, num_orders):
            for _ in range(num_orders):
                customer_id = random.choice(list(self.customers.keys()))
                order_quantities = {}
                for product_id in self.products.keys():
                    if random.random() > 0.3:  # 70% chance of including this product in the order
                        quantity = random.randint(1, 3)
                        order_quantities[product_id] = quantity

                if order_quantities:
                    self.place_order(customer_id, order_quantities)
                
    def place_order(self, customer_id, product_quantities):
        """Place an order for a given customer and their desired product quantities."""
        if customer_id not in self.customers:
            raise ValueError(f"No customer with ID '{customer_id}' found.")

        customer = self.customers[customer_id]
        order_products = []
        for product_id, quantity in product_quantities.items():
            if product_id in self.products:
                product = self.products[product_id]
                if product.purchase(quantity):
                    order_products.append({'product': product, 'quantity': quantity})
                else:
                    print(f"Not enough stock for '{product.name}' (Requested: {quantity}, Available: {product._stock})")
            else:
                print(f"No product with ID '{product_id}' found.")

        if order_products:
            order = Order(self.next_order_id, customer_id, order_products)
            self.orders[self.next_order_id] = order
            customer.place_order(order)
            self.next_order_id += 1
            print(order.get_summary())
        else:
            print("No valid products available to place an order.")

    def list_products(self):
        if self.products:
            for product in self.products.values():
                print(product.get_details())
        else:
            print("No products available in the store.")

    def list_orders(self):
        if self.orders:
            for order in self.orders.values():
                print(order.get_summary())
        else:
            print("No orders placed yet.")

    def list_customers(self):
        if self.customers:
            for customer in self.customers.values():
                print(f"Customer {customer.customer_id}: {customer.name}, Orders: {customer.list_orders()}")
        else:
            print("No customers registered.")
            
    def check_category_overlap(self):
        # Example to check overlapping categories using set operations
        electronic_ids = {prod._product_id for prod in self.products.values() if prod.category == 'Electronics'}
        kitchen_ids = {prod._product_id for prod in self.products.values() if prod.category == 'Kitchen'}
        overlap = electronic_ids.intersection(kitchen_ids)
        print("Overlap in product IDs between Electronics and Kitchen:", overlap)
            

# Initialize store and add products/customers as usual
store = Store()

# Add electronics products
store.add_product(Electronics(101, "Laptop", 999.99, 50, 24))
store.add_product(Electronics(102, "Smartphone", 599.99, 150, 12))

# Add kitchen products
store.add_product(Kitchen(201, "Blender", 99.99, 30, "A++"))
store.add_product(Kitchen(202, "Toaster", 49.99, 50, "A+"))

# Add customers manually
store.add_customer(1, "Alice")
store.add_customer(2, "Bob")

# Save and load customers AND products to/from a Feather file
store.save_and_load_customers()
store.save_and_load_products()

# List loaded products and customers to confirm persistence
print("\nLoaded Products:")
store.list_products()

print("\nLoaded Customers:")
store.list_customers()

# Emulate random orders
print("\nEmulating Random Orders:")
store.emulate_random_orders(50)
print("\nListing Orders:")
store.list_orders()

store.check_category_overlap() 
gc.collect()