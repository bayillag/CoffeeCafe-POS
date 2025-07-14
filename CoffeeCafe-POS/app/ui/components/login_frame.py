# Login Frame (app/ui/components/login_frame.py)

import tkinter as tk
from tkinter import ttk, messagebox
from app.services.auth import AuthService

class LoginFrame(ttk.Frame):
    def __init__(self, parent, auth_service: AuthService, on_success):
        super().__init__(parent)
        self.auth = auth_service
        self.on_success = on_success
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        ttk.Label(self, text="Employee Login", font=('Helvetica', 14)).grid(row=0, column=0, pady=10)
        
        ttk.Label(self, text="Email:").grid(row=1, column=0, sticky="w", padx=20)
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=2, column=0, padx=20, sticky="ew")
        
        ttk.Label(self, text="Password:").grid(row=3, column=0, sticky="w", padx=20)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=4, column=0, padx=20, sticky="ew")
        
        self.error_msg = ttk.Label(self, text="", foreground="red")
        self.error_msg.grid(row=5, column=0, pady=5)
        
        ttk.Button(self, text="Login", command=self._login).grid(row=6, column=0, pady=10)
    
    def _login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            self.error_msg.config(text="Email and password are required")
            return
            
        result = self.auth.authenticate_employee(email, password)
        if result:
            self.on_success(result)
        else:
            self.error_msg.config(text="Invalid email or password")

