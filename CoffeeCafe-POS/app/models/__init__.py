# Models Package __init__.py (CoffeeCafe-POS/app/models/init.py)

"""
Data Models Package

Contains all data models for the CoffeeCafe-POS system.
"""

# Import all models to make them available from the models package
from .product import Product
from .order import Order, OrderItem
from .employee import Employee
from .customer import Customer

__all__ = [
    'Product',
    'Order',
    'OrderItem',
    'Employee',
    'Customer'
]