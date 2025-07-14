# app/models/order.py

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: float

@dataclass
class Order:
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    items: List[OrderItem] = field(default_factory=list)
    total: float = 0.0
    payment_method: str = "cash"
    status: str = "pending"
    customer_id: Optional[str] = None
    
    def add_item(self, product_id: str, quantity: int, unit_price: float):
        self.items.append(OrderItem(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        ))
        self.total += unit_price * quantity
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_amount': self.total,
            'payment_method': self.payment_method,
            'status': self.status,
            'customer_id': self.customer_id,
            'items': [{
                'product_id': item.product_id,
                'quantity': item.quantity,
                'unit_price': item.unit_price
            } for item in self.items]
        }