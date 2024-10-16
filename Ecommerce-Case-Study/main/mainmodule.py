import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entity.customer import Customer
from entity.product import Product
from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from exception.customernotfound import CustomerNotFound
from exception.productnotfound import ProductNotFound

class EcomApp:
    def __init__(self):
        self.repository = OrderProcessorRepositoryImpl()

    def display_menu(self):
        print("\nE-commerce Application")
        print("1. Register Customer")
        print("2. Create Product")
        print("3. Delete Product")
        print("4. Add to Cart")
        print("5. View Cart")
        print("6. Place Order")
        print("7. View Customer Order")
        print("8. Exit")

    def register_customer(self):
        customerid=int(input("Enter customer Id:"))
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        password = input("Enter customer password: ")
        customer = Customer(customer_id=customerid, name=name, email=email, password=password)
        if self.repository.create_customer(customer):
            print("Customer registered successfully.")
        else:
            print("Failed to register customer.")

    def create_product(self):
        productid = int(input("Enter product Id:"))
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        description = input("Enter product description: ")
        stock_quantity = int(input("Enter stock quantity: "))
        product = Product(product_id=productid, name=name, price=price, description=description, stockQuantity=stock_quantity)
        if self.repository.create_product(product):
            print("Product created successfully.")
        else:
            print("Failed to create product.")

    def delete_product(self):
        product_id = int(input("Enter product ID to delete: "))
        if self.repository.delete_product(product_id):
            print("Product deleted successfully.")
        else:
            print("Failed to delete product.")

    def add_to_cart(self):
        customer_id = int(input("Enter customer ID: "))
        product_id = int(input("Enter product ID: "))
        quantity = int(input("Enter quantity: "))
        customer = self.repository.get_customer_by_id(customer_id)
        if not customer:
            print("Customer not found. Please register first.")
            return 
        product_row = self.repository.get_product_by_id(product_id)
        if not product_row:
            print("Product not found.")
            return

        # Create product object with all required attributes
        product = Product(
            product_id=product_row[0],
            name=product_row[1],
            price=product_row[2],
            description=product_row[3],
            stockQuantity=product_row[4]
        )
        
        if self.repository.add_to_cart(customer, product, quantity):
            print("Product added to cart successfully.")
        else:
            print("Failed to add product to cart.")

    def view_cart(self):
        customer_id = int(input("Enter customer ID: "))
        # Fetch the customer from the repository to get all details
        customer = self.repository.get_customer_by_id(customer_id)
        if customer:
            cart_items = self.repository.get_all_from_cart(customer)
            if cart_items:
                print("Cart items:")
                for item in cart_items:
                    product = item['product']
                    quantity = item['quantity']
                    print(f"- {product.get_name()}, Price: {product.get_price()}, Quantity: {quantity}")
            else:
                print("Cart is empty.")
        else:
            print("Cart is empty or Customer not found.")

    def place_order(self):
        customer_id = int(input("Enter customer ID: "))
        shipping_address = input("Enter shipping address: ")
        product_quantity_map = []  # List of tuples (product, quantity)
        # Fetch the customer from the repository
        customer = self.repository.get_customer_by_id(customer_id)
        if not customer:
            print("Customer not found. Please register first.")
            return
        while True:
            product_id = int(input("Enter product ID to order (0 to finish): "))
            if product_id == 0:
                break
            quantity = int(input("Enter quantity: "))
            product_row = self.repository.get_product_by_id(product_id)
            if not product_row:
                print(f"Product with ID {product_id} not found.")
                continue
            # Create product object with all required attributes
            product = Product(
                product_id=product_row[0],
                name=product_row[1],
                price=product_row[2],
                description=product_row[3],
                stockQuantity=product_row[4]
            )
            if product.get_stockQuantity()< quantity:
                print(f"Not enough stock for {product.get_name()}. Available: {product.get_stockQuantity()}")
                continue
            product_quantity_map.append((product, quantity))
        if not product_quantity_map:
            print("No products were selected for the order.")
            return 

        if self.repository.place_order(customer, product_quantity_map, shipping_address):
            print("Order placed successfully.")
        else:
            print("Failed to place order.")

    def view_customer_order(self):
        customer_id = int(input("Enter customer ID to view orders: "))
        orders = self.repository.get_orders_by_customer(customer_id)
        if orders:
            print("Orders for Customer ID:", customer_id)
            for product, quantity in orders.items():
                print(f"- Product ID: {product.get_product_id()}, Quantity: {quantity}")
        else:
            print("No orders found for this customer.")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Choose an operation (1-8): ")
            if choice == '1':
                self.register_customer()
            elif choice == '2':
                self.create_product()
            elif choice == '3':
                self.delete_product()
            elif choice == '4':
                self.add_to_cart()
            elif choice == '5':
                self.view_cart()
            elif choice == '6':
                self.place_order()
            elif choice == '7':
                self.view_customer_order()
            elif choice == '8':
                print("Thank you for visiting...We hope to see you again soon!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = EcomApp()
    app.run()
