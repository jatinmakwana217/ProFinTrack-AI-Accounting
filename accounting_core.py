import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class AccountingManager:
    def __init__(self, business_name="Default Business", currency="USD", jurisdiction="US"):
        self.business_name = business_name
        self.currency = currency
        self.jurisdiction = jurisdiction
        self.ledger = pd.DataFrame(columns=[
            'Date', 'Transaction_ID', 'Account', 'Description', 
            'Debit', 'Credit', 'Balance', 'Category', 'Type'
        ])
        self.chart_of_accounts = self._default_coa()
        self.invoices = pd.DataFrame()
        self.transactions = []
        self.cash_balance = 0.0
        self._ensure_dirs()

    def _default_coa(self):
        return {
            'Assets': {
                '1000': 'Cash', '1010': 'Bank', '1100': 'Accounts Receivable',
                '1200': 'Inventory', '1300': 'Fixed Assets'
            },
            'Liabilities': {
                '2000': 'Accounts Payable', '2100': 'Loans', '2200': 'Tax Payable'
            },
            'Equity': {
                '3000': 'Owner Equity', '3100': 'Retained Earnings'
            },
            'Revenue': {
                '4000': 'Sales Revenue', '4100': 'Service Revenue'
            },
            'Expenses': {
                '5000': 'Cost of Goods Sold', '5100': 'Rent', '5200': 'Salaries',
                '5300': 'Utilities', '5400': 'Marketing', '5500': 'Taxes'
            }
        }

    def _ensure_dirs(self):
        os.makedirs('/home/workdir/artifacts/reports', exist_ok=True)
        os.makedirs('/home/workdir/artifacts/data', exist_ok=True)

    def add_transaction(self, date, description, account, debit=0, credit=0, category=None):
        """Add a double-entry transaction"""
        tid = f"TX{datetime.now().strftime('%Y%m%d%H%M%S')}"
        balance = self.cash_balance + debit - credit
        self.cash_balance = balance
        
        new_row = {
            'Date': pd.to_datetime(date),
            'Transaction_ID': tid,
            'Account': account,
            'Description': description,
            'Debit': float(debit),
            'Credit': float(credit),
            'Balance': balance,
            'Category': category or 'Uncategorized',
            'Type': 'Expense' if debit > 0 else 'Income' if credit > 0 else 'Transfer'
        }
        self.ledger = pd.concat([self.ledger, pd.DataFrame([new_row])], ignore_index=True)
        self.ledger = self.ledger.sort_values('Date').reset_index(drop=True)
        return tid

    def generate_profit_loss(self, start_date=None, end_date=None):
        """Generate P&L Statement"""
        df = self.ledger.copy()
        if start_date:
            df = df[df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['Date'] <= pd.to_datetime(end_date)]
        
        revenue = df[df['Type'] == 'Income']['Credit'].sum()
        expenses = df[df['Type'] == 'Expense']['Debit'].sum()
        net_profit = revenue - expenses
        
        pl = {
            'Revenue': revenue,
            'Total_Expenses': expenses,
            'Net_Profit': net_profit,
            'Period': f"{start_date or 'All'} to {end_date or 'Now'}"
        }
        return pl

    def generate_balance_sheet(self):
        """Simple Balance Sheet"""
        assets = self.ledger[self.ledger['Account'].str.contains('Cash|Bank|Receivable|Inventory|Assets', na=False)]['Balance'].sum()
        liabilities = self.ledger[self.ledger['Account'].str.contains('Payable|Loans|Tax', na=False)]['Balance'].sum()  # Simplified
        equity = assets - liabilities
        
        return {
            'Assets': max(assets, 0),
            'Liabilities': max(liabilities, 0),
            'Equity': equity,
            'Total': assets
        }

    def export_ledger(self, filename="ledger.csv"):
        path = f"/home/workdir/artifacts/data/{filename}"
        self.ledger.to_csv(path, index=False)
        return path

    def generate_report(self, report_type="full"):
        """Generate various reports"""
        reports = {}
        reports['Profit_Loss'] = self.generate_profit_loss()
        reports['Balance_Sheet'] = self.generate_balance_sheet()
        reports['Cash_Position'] = self.cash_balance
        return reports

    def save_state(self):
        self.ledger.to_csv('/home/workdir/artifacts/data/ledger.csv', index=False)

print("AccountingManager class loaded successfully.")