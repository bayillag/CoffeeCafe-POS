# app/models/product.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: str
    name: str
    category: str
    price: float
    cost: float
    description: Optional[str] = None
    is_active: bool = True
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            category=data.get('category'),
            price=data.get('price'),
            cost=data.get('cost'),
            description=data.get('description'),
            is_active=data.get('is_active', True)
        )