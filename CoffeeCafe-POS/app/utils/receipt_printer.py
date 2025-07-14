# Receipt Printing (app/utils/receipt_printer.py)

from escpos.printer import Usb
from app.config import Config
import logging

logger = logging.getLogger(__name__)

class ReceiptPrinter:
    def __init__(self):
        try:
            self.printer = Usb(
                idVendor=Config.PRINTER_VENDOR_ID,
                idProduct=Config.PRINTER_PRODUCT_ID
            )
        except Exception as e:
            logger.error(f"Printer initialization failed: {e}")
            self.printer = None
    
    def print_receipt(self, order: dict, customer: dict = None):
        if not self.printer:
            logger.warning("No printer configured")
            return False
            
        try:
            self.printer.set(align='center')
            self.printer.text("\nCoffeeCafe\n")
            self.printer.text("123 Java Street\n")
            self.printer.text("Brewville, CA 90210\n\n")
            
            self.printer.set(align='left')
            self.printer.text(f"Order #: {order['id']}\n")
            self.printer.text(f"Date: {order['created_at']}\n")
            self.printer.text("------------------------------\n")
            
            for item in order['items']:
                self.printer.text(f"{item['quantity']}x {item['product']['name']}\n")
                self.printer.text(f"  ${item['unit_price']:.2f} each = ${item['quantity'] * item['unit_price']:.2f}\n")
            
            self.printer.text("------------------------------\n")
            self.printer.text(f"Subtotal: ${order['subtotal']:.2f}\n")
            self.printer.text(f"Tax: ${order['tax']:.2f}\n")
            self.printer.text(f"Total: ${order['total']:.2f}\n")
            
            if customer:
                self.printer.text(f"\nCustomer: {customer['name']}\n")
                self.printer.text(f"Points: {customer['points']}\n")
            
            self.printer.text("\nThank you for visiting!\n")
            self.printer.cut()
            return True
        except Exception as e:
            logger.error(f"Printing failed: {e}")
            return False