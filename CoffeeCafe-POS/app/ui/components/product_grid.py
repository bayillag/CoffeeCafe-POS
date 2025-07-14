# app/ui/components/product_grid.py

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional
from app.models.product import Product
from app.services.database import DatabaseService

class ProductGrid(ttk.Frame):
    def __init__(self, parent, db: DatabaseService):
        super().__init__(parent)
        self.db = db
        self.selected_product: Optional[Product] = None
        self._setup_ui()
        self._load_categories()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Category selector
        self.category_var = tk.StringVar()
        self.category_menu = ttk.OptionMenu(self, self.category_var, "")
        self.category_menu.grid(row=0, column=0, sticky="ew", pady=5)
        
        # Product buttons frame
        self.products_frame = ttk.Frame(self)
        self.products_frame.grid(row=1, column=0, sticky="nsew")
    
    def _load_categories(self):
        categories = self._get_categories()
        self.category_menu['menu'].delete(0, 'end')
        
        for cat in categories:
            self.category_menu['menu'].add_command(
                label=cat,
                command=lambda c=cat: self._load_products(c)
            )
        
        if categories:
            self.category_var.set(categories[0])
            self._load_products(categories[0])
    
    def _get_categories(self) -> List[str]:
        try:
            response = self.db.client.table('products').select('category').execute()
            categories = list(set(item['category'] for item in response.data))
            return sorted(categories)
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []
    
    def _load_products(self, category: str):
        # Clear existing products
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        # Load products from database
        products_data = self.db.get_products_by_category(category)
        products = [Product.from_dict(p) for p in products_data]
        
        # Create product buttons
        for i, product in enumerate(products):
            btn = ttk.Button(
                self.products_frame,
                text=f"{product.name}\n${product.price:.2f}",
                command=lambda p=product: self._select_product(p),
                width=15
            )
            btn.grid(
                row=i // 4,
                column=i % 4,
                padx=5,
                pady=5,
                sticky="nsew"
            )
    
    def _select_product(self, product: Product):
        self.selected_product = product
        self.event_generate("<<ProductSelected>>")
