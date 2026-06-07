from accounting_core import AccountingManager
from invoice_manager import InvoiceManager
import pandas as pd
import json
from datetime import datetime

class FinanceOrchestrator:
    def __init__(self, business_name="My Business"):
        self.accounting = AccountingManager(business_name)
        self.invoices = InvoiceManager()
        self.business_name = business_name
    
    def process_transaction(self, date, desc, account, debit=0, credit=0):
        return self.accounting.add_transaction(date, desc, account, debit, credit)
    
    def run_full_report(self):
        reports = self.accounting.generate_report()
        summary = {
            "Business": self.business_name,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Cash_Balance": reports['Cash_Position'],
            **reports['Profit_Loss'],
            **reports['Balance_Sheet']
        }
        return summary
    
    def save_all(self):
        self.accounting.save_state()
        self.invoices.export_invoices()
        print("All data saved.")

# Quick test / demo
if __name__ == "__main__":
    fo = FinanceOrchestrator("Test Business")
    fo.process_transaction("2026-06-01", "Initial capital", "1000", 10000, 0)
    fo.process_transaction("2026-06-02", "Rent payment", "5100", 1500, 0)
    print(fo.run_full_report())