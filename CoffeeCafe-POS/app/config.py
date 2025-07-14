# app config.py
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PRINTER_VENDOR_ID = int(os.getenv("PRINTER_VENDOR_ID", "0x04b8"))
    PRINTER_PRODUCT_ID = int(os.getenv("PRINTER_PRODUCT_ID", "0x0e15"))
    
    @classmethod
    def validate(cls):
        required = [cls.SUPABASE_URL, cls.SUPABASE_KEY]
        if not all(required):
            raise ValueError("Missing required configuration. Check .env file")