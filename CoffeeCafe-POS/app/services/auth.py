# CoffeeCafe POS - Authentication Service
# Employee Login System (app/services/auth.py)

import jwt
import datetime
from passlib.hash import pbkdf2_sha256
from app.config import Config
from app.services.database import DatabaseService
from typing import Optional, Dict

class AuthService:
    def __init__(self):
        self.db = DatabaseService()
    
    def authenticate_employee(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        try:
            employee = self.db.client.table('employees').select('*').eq('email', email).execute().data
            if not employee or not pbkdf2_sha256.verify(password, employee[0]['password_hash']):
                return None
            
            token = jwt.encode({
                'sub': employee[0]['id'],
                'name': employee[0]['name'],
                'role': employee[0]['role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            }, Config.SECRET_KEY, algorithm='HS256')
            
            return {
                'token': token,
                'employee': employee[0]
            }
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token")
            return None