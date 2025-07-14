# app/models/customer.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Customer:
    id: str
    name: str
    phone: str
    email: Optional[str] = None
    points: int = 0
    last_visit: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email'),
            points=data.get('points', 0),
            last_visit=data.get('last_visit')
        )