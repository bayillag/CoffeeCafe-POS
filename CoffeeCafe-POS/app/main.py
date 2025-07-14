# Main Application (app/main.py)

import tkinter as tk
from app.config import Config
from app.services.auth import AuthService
from app.services.database import DatabaseService
from app.ui.main_window import MainWindow
from app.ui.components.login_frame import LoginFrame
import logging

class CoffeeCafePOS:
    def __init__(self):
        Config.validate()
        self.db = DatabaseService()
        self.auth = AuthService(self.db.client)
        
        self.root = tk.Tk()
        self.root.title("CoffeeCafe POS")
        self.root.geometry("1200x800")
        
        self._show_login()
    
    def _show_login(self):
        LoginFrame(
            self.root,
            self.auth,
            self._on_login_success
        ).pack(expand=True, fill="both")
    
    def _on_login_success(self, auth_result):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        MainWindow(
            self.root,
            self.db,
            auth_result['employee']
        ).pack(expand=True, fill="both")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = CoffeeCafePOS()
    app.root.mainloop()