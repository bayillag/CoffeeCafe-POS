# app/ui/main_window.py

import tkinter as tk
from tkinter import ttk
from app.services.database import DatabaseService
from app.ui.components import ProductGrid, OrderPanel, InventoryView, ReportsView

class MainWindow(ttk.Frame):
    def __init__(self, parent, db: DatabaseService, employee: dict):
        super().__init__(parent)
        self.db = db
        self.employee = employee
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Notebook for multiple tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # POS Tab
        self.pos_tab = ttk.Frame(self.notebook)
        self._setup_pos_tab()
        self.notebook.add(self.pos_tab, text="Point of Sale")
        
        # Inventory Tab (only for managers/admins)
        if self.employee['role'] in ['admin', 'manager']:
            self.inventory_tab = ttk.Frame(self.notebook)
            self._setup_inventory_tab()
            self.notebook.add(self.inventory_tab, text="Inventory")
            
            # Reports Tab
            self.reports_tab = ttk.Frame(self.notebook)
            self._setup_reports_tab()
            self.notebook.add(self.reports_tab, text="Reports")
    
    def _setup_pos_tab(self):
        self.pos_tab.grid_columnconfigure(0, weight=3)
        self.pos_tab.grid_columnconfigure(1, weight=1)
        self.pos_tab.grid_rowconfigure(0, weight=1)
        
        self.product_grid = ProductGrid(self.pos_tab, self.db)
        self.product_grid.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.order_panel = OrderPanel(self.pos_tab, self.db)
        self.order_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    
    def _setup_inventory_tab(self):
        self.inventory_tab.grid_columnconfigure(0, weight=1)
        self.inventory_tab.grid_rowconfigure(0, weight=1)
        
        self.inventory_view = InventoryView(self.inventory_tab, self.db)
        self.inventory_view.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def _setup_reports_tab(self):
        self.reports_tab.grid_columnconfigure(0, weight=1)
        self.reports_tab.grid_rowconfigure(0, weight=1)
        
        self.reports_view = ReportsView(self.reports_tab, self.db)
        self.reports_view.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)