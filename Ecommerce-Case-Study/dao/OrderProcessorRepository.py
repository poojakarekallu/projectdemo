import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from abc import ABC, abstractmethod
from typing import List, Dict
from entity.customer import Customer 
from entity.product import Product

class OrderProcessorRepository(ABC):
    
    @abstractmethod
    def create_product(self, product: Product) -> bool:
        pass

    @abstractmethod
    def create_customer(self, customer: Customer) -> bool:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int) -> bool:
        pass

    @abstractmethod
    def add_to_cart(self, customer: Customer, product: Product, quantity: int) -> bool:
        pass

    @abstractmethod
    def remove_from_cart(self, customer: Customer, product: Product) -> bool:
        pass

    @abstractmethod
    def get_all_from_cart(self, customer: Customer) -> List[Product]:
        pass

    @abstractmethod
    def place_order(self, customer: Customer, product_quantity_map: List[Dict[Product, int]], shipping_address: str) -> bool:
        pass

    @abstractmethod
    def get_orders_by_customer(self, customer_id: int) -> List[Dict[Product, int]]:
        pass
