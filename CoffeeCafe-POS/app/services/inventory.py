# Inventory Management (app/services/inventory.py)

from typing import List, Dict, Optional
from app.services.database import DatabaseService
import logging

logger = logging.getLogger(__name__)

class InventoryService:
    def __init__(self):
        self.db = DatabaseService()
    
    def get_stock_level(self, product_id: str) -> int:
        try:
            response = self.db.client.table('inventory').select('quantity').eq('product_id', product_id).execute()
            return response.data[0]['quantity'] if response.data else 0
        except Exception as e:
            logger.error(f"Error checking stock: {e}")
            return 0
    
    def update_stock(self, product_id: str, quantity_change: int) -> bool:
        try:
            current = self.get_stock_level(product_id)
            if current + quantity_change < 0:
                return False
                
            self.db.client.table('inventory').upsert({
                'product_id': product_id,
                'quantity': current + quantity_change
            }).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating inventory: {e}")
            return False
    
    def get_low_stock_items(self, threshold: int = 5) -> List[Dict[str, Any]]:
        try:
            response = self.db.client.table('inventory').select('*, products(*)').lt('quantity', threshold).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching low stock items: {e}")
            return []