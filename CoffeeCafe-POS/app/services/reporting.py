# Reporting System (app/services/reporting.py)

from datetime import datetime, timedelta
from app.services.database import DatabaseService
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ReportingService:
    def __init__(self):
        self.db = DatabaseService()
    
    def get_sales_report(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        try:
            response = self.db.client.table('orders').select('*, order_items(*, products(*))').gte('created_at', start_date.isoformat()).lte('created_at', end_date.isoformat()).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error generating sales report: {e}")
            return []
    
    def get_daily_sales(self, days: int = 7) -> List[Dict[str, Any]]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return self.get_sales_report(start_date, end_date)
    
    def get_top_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            response = self.db.client.rpc('get_top_products', {'limit': limit}).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching top products: {e}")
            return []