# Inventory View (app/ui/components/inventory_view.py)

import tkinter as tk
from tkinter import ttk
from app.services.inventory import InventoryService

class InventoryView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.inventory = InventoryService()
        self._setup_ui()
        self._load_inventory()
    
    def _setup_ui(self):
        self.tree = ttk.Treeview(self, columns=("name", "category", "stock"), show="headings")
        self.tree.heading("name", text="Product")
        self.tree.heading("category", text="Category")
        self.tree.heading("stock", text="Stock")
        self.tree.pack(fill="both", expand=True)
        
        self.refresh_btn = ttk.Button(self, text="Refresh", command=self._load_inventory)
        self.refresh_btn.pack(pady=5)
    
    def _load_inventory(self):
        self.tree.delete(*self.tree.get_children())
        products = self.inventory.db.get_products()
        
        for product in products:
            stock = self.inventory.check_stock(product['id'])
            self.tree.insert("", "end", values=(
                product['name'],
                product['category'],
                stock
            ))