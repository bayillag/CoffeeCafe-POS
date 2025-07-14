# Root __init__.py (CoffeeCafe-POS/app/init.py)

"""
CoffeeCafe-POS Application Package

This is the main package for the Coffee Shop Point of Sale system.
"""

from .version import __version__

# Import key components to make them available at package level
from .main import CoffeeCafePOS
from .config import Config

__all__ = [
    'CoffeeCafePOS',
    'Config',
    '__version__'
]