# app/ui/components/order_panel.py

import tkinter as tk
from tkinter import ttk, messagebox
from app.models.order import Order
from app.services.database import DatabaseService
from app.services.loyalty import LoyaltyService
from app.utils.receipt_printer import ReceiptPrinter

class OrderPanel(ttk.LabelFrame):
    def __init__(self, parent, db: DatabaseService):
        super().__init__(parent, text="Current Order", padding=10)
        self.db = db
        self.loyalty = LoyaltyService()
        self.printer = ReceiptPrinter()
        self.order = Order()
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Customer info
        self.customer_frame = ttk.Frame(self)
        self.customer_frame.grid(row=0, column=0, sticky="ew")
        
        ttk.Label(self.customer_frame, text="Customer Phone:").pack(side=tk.LEFT)
        self.customer_phone = ttk.Entry(self.customer_frame, width=15)
        self.customer_phone.pack(side=tk.LEFT, padx=5)
        
        self.customer_btn = ttk.Button(self.customer_frame, text="Find", command=self._find_customer)
        self.customer_btn.pack(side=tk.LEFT)
        
        # Order items
        self.tree = ttk.Treeview(self, columns=("qty", "name", "price", "total"), show="headings")
        self.tree.heading("qty", text="Qty")
        self.tree.heading("name", text="Item")
        self.tree.heading("price", text="Price")
        self.tree.heading("total", text="Total")
        self.tree.column("qty", width=50, anchor="center")
        self.tree.column("price", width=80, anchor="e")
        self.tree.column("total", width=80, anchor="e")
        self.tree.grid(row=1, column=0, sticky="nsew", pady=5)
        
        # Totals
        self.subtotal_var = tk.StringVar(value="Subtotal: $0.00")
        ttk.Label(self, textvariable=self.subtotal_var).grid(row=2, column=0, sticky="e")
        
        self.tax_var = tk.StringVar(value="Tax: $0.00")
        ttk.Label(self, textvariable=self.tax_var).grid(row=3, column=0, sticky="e")
        
        self.total_var = tk.StringVar(value="Total: $0.00")
        ttk.Label(self, textvariable=self.total_var, font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="e")
        
        # Payment
        payment_frame = ttk.Frame(self)
        payment_frame.grid(row=5, column=0, sticky="ew", pady=10)
        
        self.payment_method = tk.StringVar(value="cash")
        ttk.Radiobutton(payment_frame, text="Cash", variable=self.payment_method, value="cash").pack(side=tk.LEFT)
        ttk.Radiobutton(payment_frame, text="Card", variable=self.payment_method, value="card").pack(side=tk.LEFT)
        ttk.Radiobutton(payment_frame, text="Mobile", variable=self.payment_method, value="mobile").pack(side=tk.LEFT)
        
        # Complete order
        ttk.Button(self, text="Complete Order", command=self._complete_order).grid(row=6, column=0, sticky="ew")
    
    def _find_customer(self):
        phone = self.customer_phone.get()
        if not phone:
            return
            
        customer = self.db.get_customer_by_phone(phone)
        if customer:
            self.order.customer_id = customer['id']
            messagebox.showinfo("Customer Found", f"Welcome back {customer['name']}!\nPoints: {customer['points']}")
        else:
            if messagebox.askyesno("New Customer", "Customer not found. Create new account?"):
                name = simpledialog.askstring("New Customer", "Enter customer name:")
                if name:
                    try:
                        new_customer = self.db.client.table('customers').insert({
                            'name': name,
                            'phone': phone
                        }).execute().data[0]
                        self.order.customer_id = new_customer['id']
                        messagebox.showinfo("Success", "New customer created")
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not create customer: {e}")
    
    def add_item(self, product_id: str, quantity: int = 1, unit_price: float):
        self.order.add_item(product_id, quantity, unit_price)
        self._update_display()
    
    def _update_display(self):
        self.tree.delete(*self.tree.get_children())
        
        for item in self.order.items:
            product = self.db.get_product(item.product_id)
            total = item.quantity * item.unit_price
            self.tree.insert("", "end", values=(
                item.quantity,
                product['name'],
                f"${item.unit_price:.2f}",
                f"${total:.2f}"
            ))
        
        subtotal = self.order.total
        tax = subtotal * 0.08  # Example 8% tax
        total = subtotal + tax
        
        self.subtotal_var.set(f"Subtotal: ${subtotal:.2f}")
        self.tax_var.set(f"Tax: ${tax:.2f}")
        self.total_var.set(f"Total: ${total:.2f}")
    
    def _complete_order(self):
        if not self.order.items:
            messagebox.showwarning("Empty Order", "No items in current order")
            return
            
        # Calculate totals
        subtotal = self.order.total
        tax = subtotal * 0.08
        total = subtotal + tax
        
        # Set payment method
        self.order.payment_method = self.payment_method.get()
        self.order.status = "completed"
        
        # Save order
        order_data = {
            'total_amount': total,
            'subtotal': subtotal,
            'tax': tax,
            'payment_method': self.order.payment_method,
            'status': self.order.status,
            'customer_id': self.order.customer_id
        }
        
        saved_order = self.db.create_order(order_data)
        if not saved_order:
            messagebox.showerror("Error", "Failed to save order")
            return
            
        # Save order items
        items_data = [{
            'order_id': saved_order['id'],
            'product_id': item.product_id,
            'quantity': item.quantity,
            'unit_price': item.unit_price
        } for item in self.order.items]
        
        if not self.db.add_order_items(saved_order['id'], items_data):
            messagebox.showerror("Error", "Failed to save order items")
            return
        
        # Update loyalty points if customer exists
        if self.order.customer_id:
            self.loyalty.add_points(self.order.customer_id, subtotal)
        
        # Print receipt
        receipt_data = {
            'id': saved_order['id'],
            'created_at': datetime.now().isoformat(),
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
            'items': [{
                'product': {'name': self.db.get_product(item.product_id)['name']},
                'quantity': item.quantity,
                'unit_price': item.unit_price
            } for item in self.order.items]
        }
        
        customer = None
        if self.order.customer_id:
            customer = self.db.get_customer_by_phone(self.customer_phone.get())
        
        self.printer.print_receipt(receipt_data, customer)
        
        # Reset order
        self.order = Order()
        self._update_display()
        self.customer_phone.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Order #{saved_order['id']} completed")