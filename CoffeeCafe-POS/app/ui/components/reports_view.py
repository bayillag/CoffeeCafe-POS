
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.services.reporting import ReportingService
from app.services.database import DatabaseService
from app.utils.helpers import format_currency

class ReportsView(ttk.Frame):
    def __init__(self, parent, db: DatabaseService):
        super().__init__(parent)
        self.db = db
        self.reporting = ReportingService()
        self._setup_ui()
        self._setup_time_period()
        self._generate_default_report()

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Control Panel
        control_panel = ttk.Frame(self)
        control_panel.grid(row=0, column=0, sticky="ew", pady=5)
        
        ttk.Button(control_panel, text="Sales Report", 
                  command=self._generate_sales_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, text="Top Products", 
                  command=self._generate_top_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, text="Hourly Trends", 
                  command=self._generate_hourly_trends).pack(side=tk.LEFT, padx=5)
        
        # Time period controls
        ttk.Label(control_panel, text="Period:").pack(side=tk.LEFT, padx=5)
        self.period_var = tk.StringVar(value="7d")
        ttk.OptionMenu(control_panel, self.period_var, "7d", "1d", "7d", "30d", 
                      command=self._on_period_change).pack(side=tk.LEFT)

        # Report Display Area
        report_frame = ttk.Frame(self)
        report_frame.grid(row=1, column=0, sticky="nsew")
        report_frame.grid_columnconfigure(0, weight=1)
        report_frame.grid_rowconfigure(0, weight=1)

        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=report_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Data Table
        self.tree = ttk.Treeview(self, columns=("date", "orders", "revenue"), show="headings")
        self.tree.heading("date", text="Date")
        self.tree.heading("orders", text="Orders")
        self.tree.heading("revenue", text="Revenue")
        self.tree.grid(row=2, column=0, sticky="ew", pady=5)

    def _setup_time_period(self):
        self.end_date = datetime.now()
        self._update_dates_based_on_period()

    def _update_dates_based_on_period(self):
        period = self.period_var.get()
        if period == "1d":
            self.start_date = self.end_date - timedelta(days=1)
        elif period == "7d":
            self.start_date = self.end_date - timedelta(days=7)
        elif period == "30d":
            self.start_date = self.end_date - timedelta(days=30)

    def _on_period_change(self, *args):
        self._update_dates_based_on_period()
        self._generate_sales_report()

    def _generate_default_report(self):
        self._generate_sales_report()

    def _generate_sales_report(self):
        report_data = self.reporting.get_sales_report(self.start_date, self.end_date)
        self._display_sales_data(report_data)

    def _generate_top_products(self):
        top_products = self.reporting.get_top_products(limit=5)
        self._display_top_products(top_products)

    def _generate_hourly_trends(self):
        hourly_data = self.reporting.get_hourly_sales()
        self._display_hourly_trends(hourly_data)

    def _display_sales_data(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Process data for visualization
        dates = [datetime.strptime(d['created_at'], '%Y-%m-%dT%H:%M:%S').date() 
                for d in data]
        revenues = [d['total_amount'] for d in data]
        
        # Group by date
        daily_data = {}
        for date, revenue in zip(dates, revenues):
            if date in daily_data:
                daily_data[date] += revenue
            else:
                daily_data[date] = revenue
                
        sorted_dates = sorted(daily_data.keys())
        sorted_revenues = [daily_data[d] for d in sorted_dates]
        
        # Plotting
        ax.bar(sorted_dates, sorted_revenues)
        ax.set_title(f"Sales Report: {self.start_date.date()} to {self.end_date.date()}")
        ax.set_ylabel("Revenue ($)")
        ax.set_xlabel("Date")
        self.figure.autofmt_xdate()
        
        self.canvas.draw()
        
        # Update data table
        self._update_data_table(sorted_dates, sorted_revenues)

    def _display_top_products(self, products):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        names = [p['name'] for p in products]
        quantities = [p['total_quantity'] for p in products]
        
        ax.barh(names, quantities)
        ax.set_title("Top Selling Products")
        ax.set_xlabel("Quantity Sold")
        
        self.canvas.draw()
        self._clear_data_table()

    def _display_hourly_trends(self, hourly_data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        hours = [d['hour'] for d in hourly_data]
        sales = [d['total_sales'] for d in hourly_data]
        
        ax.plot(hours, sales, marker='o')
        ax.set_title("Hourly Sales Trends")
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Sales ($)")
        ax.set_xticks(range(24))
        
        self.canvas.draw()
        self._clear_data_table()

    def _update_data_table(self, dates, revenues):
        self.tree.delete(*self.tree.get_children())
        
        # Group by date and count orders
        date_counts = {}
        for date in dates:
            if date in date_counts:
                date_counts[date] += 1
            else:
                date_counts[date] = 1
                
        for date in sorted(date_counts.keys()):
            self.tree.insert("", "end", values=(
                date.strftime('%Y-%m-%d'),
                date_counts[date],
                format_currency(revenues[dates.index(date)])
            ))

    def _clear_data_table(self):
        self.tree.delete(*self.tree.get_children())