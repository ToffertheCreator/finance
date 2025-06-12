from abc import ABC, abstractmethod
import sqlite3
import shutil
from datetime import datetime
from collections import defaultdict


class Transaction:
    def __init__(self, date, amount, category, account, note, txn_type):
        self.__date = date
        self.__amount = amount
        self.__category = category
        self.__account = account
        self.__note = note
        self.__txn_type = txn_type

    def get_data(self):
        return (self.__date, self.__amount, self.__category, self.__account, self.__note, self.__txn_type)

class DatabaseManager:
    def __init__(self, db_name):
        self.__db_name = db_name
        self.__connection = None
        self.__cursor = None

    def __enter__(self):
        self.__connection = sqlite3.connect(self.__db_name)
        self.__cursor = self.__connection.cursor()
        self.__initialize_schema()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.commit()
        self.__connection.close()

    def run_query(self, query, params=(), fetch=False, fetchone=False):
        self.__cursor.execute(query, params)
        self.__connection.commit()
        if fetchone:
            return self.__cursor.fetchone()
        elif fetch:
            return self.__cursor.fetchall()

    def fetch_query(self, query, params=None):
        if params:
            self.__cursor.execute(query, params)
        else:
            self.__cursor.execute(query)
        return self.__cursor.fetchall()

    def __initialize_schema(self):
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                account TEXT NOT NULL,
                note TEXT,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
            )
        ''')

        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                current_saved REAL NOT NULL,
                target_amount REAL NOT NULL,
                target_date TEXT NOT NULL
            )
        ''')

        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                action TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')

        self.__connection.commit()

class TransactionManager:
    @staticmethod
    def add_transaction(db: DatabaseManager, transaction: Transaction):
        query = '''INSERT INTO transactions (date, amount, category, account, note, type)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        db.run_query(query, transaction.get_data())

    @staticmethod
    def get_all_transactions(db: DatabaseManager, year=None):
        if year:
            query = "SELECT * FROM transactions WHERE strftime('%Y', date) = ?"
            return db.run_query(query, (str(year),), fetch=True)
        else:
            return db.run_query("SELECT * FROM transactions", fetch=True)
    
    @staticmethod
    def get_transaction_by_date(db: DatabaseManager, date: str):
        query = "SELECT * FROM transactions WHERE date = ?"
        result = db.fetch_query(query, (date,))
        if result:
            return result[0]
        return None
    
    @staticmethod
    def get_transaction_by_type(db: DatabaseManager, txn_type):
        query = "SELECT * FROM transactions WHERE type = ?"
        result = db.fetch_query(query, (txn_type,))
        return result
    
    @staticmethod
    def edit_transaction(db_manager: DatabaseManager, date: str, new_amount: float, new_category: str, new_mode: str, new_note: str, new_type: str):
        query = "SELECT * FROM transactions WHERE date = ?"
        result = db_manager.run_query(query, (date,), fetchone=True)
        
        if result:
            update_query = '''
                UPDATE transactions
                SET amount = ?, category = ?, account = ?, note = ?, type = ?
                WHERE date = ?
            '''
            db_manager.run_query(update_query, (new_amount, new_category, new_mode, new_note, new_type, date))
            print("Transaction updated successfully.")
        else:
            print("No transaction found on that date.")

    @staticmethod
    def delete_transaction(db_manager: DatabaseManager, date: str):
        query = "SELECT * FROM transactions WHERE date = ?"
        result = db_manager.run_query(query, (date,), fetchone=True)
        
        if result:
            delete_query = "DELETE FROM transactions WHERE date = ?"
            db_manager.run_query(delete_query, (date,))
            print("Transaction deleted successfully.")
        else:
            print("No transaction found on that date.")

class SavingsManager:
    @staticmethod
    def set_savings_goal(db: DatabaseManager, name, target_amount, target_date):
        db.run_query("INSERT INTO savings (name, target_amount, current_saved, target_date) VALUES (?, ?, ?, ?)", (name, target_amount, 0, target_date))

    @staticmethod
    def add_savings(db: DatabaseManager, name, amount):
        db.run_query("UPDATE savings SET current_saved = current_saved + ? WHERE name = ?", (amount, name))
        db.run_query("INSERT INTO savings_history (name, amount, action, date) VALUES (?, ?, ?, ?)",
                    (name, amount, "added", datetime.now().strftime("%Y-%m-%d")))


    @staticmethod
    def track_savings(db: DatabaseManager):
        row = db.run_query("SELECT target_amount, current_saved FROM savings WHERE id = 1", fetchone=True)
        if row:
            return row[1], row[0] - row[1]
        return 0, 0

    @staticmethod
    def get_savings_name(db: DatabaseManager):
        row = db.run_query("SELECT name FROM savings WHERE id = 1", fetchone=True)
        return row[0] if row else None
    
    @staticmethod
    def get_savings_target_date(db: DatabaseManager):
        row = db.run_query("SELECT target_date FROM savings WHERE id = 1", fetchone=True)
        return row[0] if row else None
    
    @staticmethod
    def get_savings_history(db: DatabaseManager):
        return db.run_query("SELECT name, date, amount, action FROM savings_history", fetch=True)

    @staticmethod
    def delete_savings(db: DatabaseManager, name):
        db.run_query("DELETE FROM savings WHERE name = ?", (name,))
        db.run_query("DELETE FROM savings_history WHERE name = ?", (name,))


#for transactions page
class SummaryManager(TransactionManager):
    def __init__(self, db: DatabaseManager):
        self.db = db
        
    def generate_summary(self):
        transactions = self.get_all_transactions(self.db)
        summary = {"income": 0, "expense": 0, "category_breakdown": {}}
        for _, _, amount, category, *_ in transactions:
            if category not in summary["category_breakdown"]:
                summary["category_breakdown"][category] = {"income": 0, "expense": 0}
            if amount >= 0:
                summary["income"] += amount
                summary["category_breakdown"][category]["income"] += amount
            else:
                summary["expense"] += abs(amount)
                summary["category_breakdown"][category]["expense"] += abs(amount)
        summary["remaining_budget"] = summary["income"] - summary["expense"]
        return summary
    
    def track_expenses(self):
        transactions = self.get_all_transactions(self.db)
        expenses = [txn for txn in transactions if txn[6].lower() == "expense"]
        return expenses

    def track_income(self):
        transactions = self.get_all_transactions(self.db)
        income = [txn for txn in transactions if txn[6].lower() == "income"]
        return income

class BackupManager:
    def __init__(self, db_path='finance.db'):
        self.db_path = db_path

    def create_backup(self, backup_path='backup_finance.db'):
        shutil.copyfile(self.db_path, backup_path)
        return f"Backup saved to {backup_path}"

class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, db: DatabaseManager):
        pass

class AnalyticsManager(ReportGenerator, SummaryManager, SavingsManager):
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def generate_report(self):
        summary = self.generate_summary(self.db)
        savings = self.track_savings(self.db)
        return {"summary": summary, "savings": savings}

    def get_totals(self, year=None):
        transactions = self.get_all_transactions(self.db, year)
        total_income = sum(txn[2] for txn in transactions if str(txn[6]).lower() == "income")
        total_expense = sum(abs(txn[2]) for txn in transactions if str(txn[6]).lower() == "expense")
        return total_income, total_expense

    def get_category_totals(self, year=None):
        transactions = self.get_all_transactions(self.db, year)
        category_totals = {}
        for txn in transactions:
            category = txn[3]
            amount = txn[2]
            txn_type = str(txn[6]).lower()
            if category not in category_totals:
                category_totals[category] = {"income": 0, "expense": 0}
            if txn_type == "income":
                category_totals[category]["income"] += amount
            elif txn_type == "expense":
                category_totals[category]["expense"] += abs(amount)
        return category_totals
    
    def get_monthly_totals(self, year=None):
        transactions = self.get_all_transactions(self.db, year)
        monthly_totals = defaultdict(lambda: {"income": 0, "expense": 0})
        for txn in transactions:
            date_str = txn[1]
            amount = txn[2]
            txn_type = str(txn[6]).lower()
            month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")
            if txn_type == "income":
                monthly_totals[month]["income"] += amount
            elif txn_type == "expense":
                monthly_totals[month]["expense"] += abs(amount)
        return dict(monthly_totals)
    
    def get_available_years(self):
        result = self.db.run_query(
            "SELECT DISTINCT strftime('%Y', date) AS year FROM transactions ORDER BY year DESC",
            fetch=True
        )
        return [row[0] for row in result]

