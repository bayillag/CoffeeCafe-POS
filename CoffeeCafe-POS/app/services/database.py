# app/services/database.py

from supabase import create_client, Client
from app.config import Config
import logging
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)

class DatabaseService:
    _instance: Optional['DatabaseService'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        Config.validate()
        self.client: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        logger.info("Database service initialized")
    
    # Product Operations
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.client.table('products').select('*').eq('id', product_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching product: {e}")
            return None
    
    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        try:
            response = self.client.table('products').select('*').eq('category', category).eq('is_active', True).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []
    
    # Order Operations
    def create_order(self, order_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = self.client.table('orders').insert(order_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return None
    
    def add_order_items(self, order_id: str, items: List[Dict[str, Any]]) -> bool:
        try:
            self.client.table('order_items').insert(items).execute()
            return True
        except Exception as e:
            logger.error(f"Error adding order items: {e}")
            return False
    
    # Customer Operations
    def get_customer_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.client.table('customers').select('*').eq('phone', phone).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching customer: {e}")
            return None