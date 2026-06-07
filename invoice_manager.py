import pandas as pd
from datetime import datetime

class InvoiceManager:
    def __init__(self):
        self.invoices = pd.DataFrame(columns=[
            'Invoice_ID', 'Customer', 'Date', 'Due_Date', 
            'Amount', 'Status', 'Description'
        ])
    
    def create_invoice(self, customer, amount, description="", days_due=30):
        inv_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{len(self.invoices)+1:03d}"
        due_date = datetime.now() + timedelta(days=days_due)
        
        new_inv = {
            'Invoice_ID': inv_id,
            'Customer': customer,
            'Date': datetime.now().date(),
            'Due_Date': due_date.date(),
            'Amount': float(amount),
            'Status': 'Unpaid',
            'Description': description
        }
        self.invoices = pd.concat([self.invoices, pd.DataFrame([new_inv])], ignore_index=True)
        return inv_id
    
    def mark_paid(self, invoice_id):
        self.invoices.loc[self.invoices['Invoice_ID'] == invoice_id, 'Status'] = 'Paid'
    
    def get_overdue(self):
        today = datetime.now().date()
        return self.invoices[(self.invoices['Status'] == 'Unpaid') & 
                           (self.invoices['Due_Date'] < today)]
    
    def export_invoices(self):
        path = "/home/workdir/artifacts/data/invoices.csv"
        self.invoices.to_csv(path, index=False)
        return path

print("InvoiceManager loaded.")