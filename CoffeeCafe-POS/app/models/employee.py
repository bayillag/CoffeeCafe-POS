# app/models/employee.py

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Employee:
    id: str
    name: str
    email: str
    role: str  # 'admin', 'manager', 'staff'
    is_active: bool = True
    pin_code: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            role=data.get('role'),
            is_active=data.get('is_active', True),
            pin_code=data.get('pin_code')
        )