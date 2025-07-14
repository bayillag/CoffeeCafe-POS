# Loyalty Program (app/services/loyalty.py)

from app.services.database import DatabaseService
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class LoyaltyService:
    def __init__(self):
        self.db = DatabaseService()
        self.points_per_dollar = 1  # 1 point per $1 spent
        self.point_value = 0.05    # $0.05 value per point
    
    def get_customer_points(self, customer_id: str) -> int:
        try:
            response = self.db.client.table('customers').select('points').eq('id', customer_id).execute()
            return response.data[0]['points'] if response.data else 0
        except Exception as e:
            logger.error(f"Error getting customer points: {e}")
            return 0
    
    def add_points(self, customer_id: str, amount_spent: float) -> bool:
        points_to_add = int(amount_spent * self.points_per_dollar)
        try:
            self.db.client.rpc('increment_points', {
                'customer_id': customer_id,
                'points': points_to_add
            }).execute()
            return True
        except Exception as e:
            logger.error(f"Error adding loyalty points: {e}")
            return False
    
    def redeem_points(self, customer_id: str, points: int) -> Optional[float]:
        current_points = self.get_customer_points(customer_id)
        if current_points < points:
            return None
        
        discount = points * self.point_value
        try:
            self.db.client.rpc('decrement_points', {
                'customer_id': customer_id,
                'points': points
            }).execute()
            return discount
        except Exception as e:
            logger.error(f"Error redeeming points: {e}")
            return None