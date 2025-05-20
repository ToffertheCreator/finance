from abc import ABC, abstractmethod
import sqlite3
import shutil
import matplotlib.pyplot as plt
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
                goal_amount TEXT NOT NULL,
                current_saved REAL NOT NULL,
                duration TEXT
            )
        ''')

        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                duration TEXT
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
    def get_all_transactions(db: DatabaseManager):
        return db.run_query("SELECT * FROM transactions", fetch=True)
    
    @staticmethod
    def get_transaction_by_date(db: DatabaseManager, date: str):
        query = "SELECT * FROM transactions WHERE date = ?"
        result = db.fetch_query(query, (date,))
        if result:
            return result[0]
        return None
    
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


# class BudgetManager:
#     @staticmethod
#     def set_budget(db: DatabaseManager, category, amount, duration):
#         query = '''INSERT OR REPLACE INTO budgets (id, category, amount, duration)
#                    VALUES ((SELECT id FROM budgets WHERE category = ?), ?, ?, ?)'''
#         db.run_query(query, (category, amount, duration))

#     @staticmethod
#     def get_budget(db: DatabaseManager, category):
#         return db.run_query("SELECT amount, duration FROM budgets WHERE category = ?", (category,), fetchone=True)

#     @staticmethod
#     def track_budget(db: DatabaseManager, category, spent_amount):
#         budget = BudgetManager.get_budget(db, category)
#         if budget:
#             amount_limit = budget[0]
#             remaining = amount_limit - spent_amount
#             return (remaining >= 0, remaining)
#         return (False, 0)

class SavingsTracker:
    @staticmethod
    def set_savings_goal(db: DatabaseManager, amount, duration):
        db.run_query("INSERT INTO savings (goal_amount, current_saved, duration) VALUES (?, ?, ?)", (amount, 0, duration))

    @staticmethod
    def add_savings(db: DatabaseManager, amount):
        db.run_query("UPDATE savings SET current_saved = current_saved + ? WHERE id = 1", (amount,))

    @staticmethod
    def track_savings(db: DatabaseManager):
        row = db.run_query("SELECT goal_amount, current_saved FROM savings WHERE id = 1", fetchone=True)
        if row:
            return row[1], row[0] - row[1]
        return 0, 0

class SummaryTracker(TransactionManager):
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

class AnalyticsEngine(ReportGenerator, SummaryTracker, SavingsTracker, BackupManager):
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def generate_report(self):
        summary = self.generate_summary(self.db)
        savings = self.track_savings(self.db)
        return {"summary": summary, "savings": savings}

    def analyze_trends(self):
        transactions = self.get_all_transactions(self.db)  # Assuming it returns rows/tuples
        trends = defaultdict(float)

        for txn in transactions:
            date = txn[1]  # assuming index 1 is date
            amount = txn[2]  # assuming index 2 is amount
            txn_type = txn[6].lower()  # assuming index 6 is type

            month = date[:7]  # 'YYYY-MM' format
            if txn_type == "income":
                trends[month] += amount
            elif txn_type == "expense":
                trends[month] -= amount  # subtract expense

        return dict(trends)

    def visualize_data(self, chart_type, db: DatabaseManager):
        with db:
            transactions = TransactionManager.get_all_transactions(self.db)

            if chart_type == "expense_vs_income":
                income = sum(txn.amount for txn in transactions if txn.txn_type == "income")
                expenses = sum(txn.amount for txn in transactions if txn.txn_type == "expense")
                plt.bar(["Income", "Expenses"], [income, expenses])
                plt.title("Income vs Expenses")

            elif chart_type == "category_pie_chart":
                category_totals = defaultdict(float)
                for txn in transactions:
                    if txn.txn_type == "expense":
                        category_totals[txn.category] += txn.amount
                if category_totals:
                    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
                    plt.title("Expense Distribution by Category")
                else:
                    print("No expenses to visualize.")
                    return

            elif chart_type == "trend_analysis":
                trends = self.analyze_trends()
                months = sorted(trends.keys())
                balances = [trends[m] for m in months]
                plt.plot(months, balances, marker='o')
                plt.title("Monthly Net Savings Trend")
                plt.xticks(rotation=45)

            elif chart_type == "top_expenses":
                expenses = self.track_expenses()
                sorted_exp = sorted(expenses, key=lambda x: x.amount, reverse=True)[:5]
                names = [f"{e.category} - {e.date}" for e in sorted_exp]
                amounts = [e.amount for e in sorted_exp]
                if names:
                    plt.barh(names, amounts)
                    plt.title("Top 5 Expenses")
                else:
                    print("No expense data available.")
                    return

            else:
                print("Invalid chart type.")
                return

            plt.tight_layout()
            plt.show()

class FinanceUI:
    def __init__(self):
        self.engine = AnalyticsEngine(DatabaseManager("finance.db"))

    def display_menu(self):
        print("Welcome to the Finance Manager!")
        print("1. Add Transaction")
        print("2. Edit Transaction")
        print("3. Delete Transaction")
        # print("4. Set Budget")
        # print("5. Track Budget")
        print("6. Set Savings Goal")
        print("7. Add to Savings")
        print("8. View Transaction History")
        print("9. View Savings Progress")
        print("10. Generate Report")
        print("11. Visualize Data")
        print("12. Create Backup")
        print("13. Exit")

    def handle_user_input(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.edit_transaction()
            elif choice == "3":
                self.delete_transaction()
            # elif choice == "4":
            #     self.set_budget()
            # elif choice == "5":
            #     self.track_budget()
            elif choice == "6":
                self.set_savings_goal()
            elif choice == "7":
                self.add_to_savings()
            elif choice == "8":
                self.view_transaction_history()
            elif choice == "9":
                self.view_savings_progress()
            elif choice == "10":
                self.generate_report()
            elif choice == "11":
                self.visualize_data()
            elif choice == "12":
                self.create_backup()
            elif choice == "13":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_transaction(self):
        date = input("Enter date (YYYY-MM-DD): ")
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        account = input("Enter account: ")
        note = input("Enter note: ")
        txn_type = input("Enter type (Income/Expense): ")
        txn = Transaction(date, amount, category, account, note, txn_type)

        with DatabaseManager("finance.db") as db:
            self.engine.add_transaction(db, txn)

        print("Transaction added successfully!")

    def edit_transaction(self):
        date = input("Enter the date of the transaction to edit (YYYY-MM-DD): ")
        txn = self.engine.get_transaction_by_date(self.engine.db, date)
        if txn:
            print(f"Found: Date: {txn[0]}, Amount: {txn[1]}, Category: {txn[2]}, Account: {txn[3]}, Note: {txn[4]}")
            amount = float(input("Enter new amount: "))
            category = input("Enter new category: ")
            account = input("Enter new account: ")
            note = input("Enter new note: ")
            self.engine.edit_transaction(self.engine.db, date, amount, category, account, note)
            print("Transaction updated successfully!")
        else:
            print("No transaction found for that date.")

    def delete_transaction(self):
        date = input("Enter the date of the transaction to delete (YYYY-MM-DD): ")
        txn = self.engine.get_transaction_by_date(self.engine.db, date)
        if txn:
            print(f"Found: Date: {txn[0]}, Amount: {txn[1]}, Category: {txn[2]}, Account: {txn[3]}, Note: {txn[4]}")
            confirm = input("Are you sure you want to delete this transaction? (yes/no): ").lower()
            if confirm == "yes":
                self.engine.delete_transaction(self.engine.db, date)
                print("Transaction deleted.")
            else:
                print("Deletion canceled.")
        else:
            print("No transaction found.")

    # def set_budget(self):
    #     category = input("Enter category: ")
    #     amount = float(input("Enter budget amount: "))
    #     duration = input("Enter duration (e.g., Monthly): ")
    #     self.engine.set_budget(self.engine.db, category, amount, duration)
    #     print(f"Budget set for {category}: {amount} ({duration})")

    # def track_budget(self):
    #     category = input("Enter category to track: ")
    #     spent = float(input("Enter spent amount: "))
    #     ok, remaining = self.engine.track_budget(self.engine.db, category, spent)
    #     if ok:
    #         print(f"You are within budget for {category}. Remaining: {remaining}")
    #     else:
    #         print(f"Budget exceeded for {category}. Over by: {abs(remaining)}")

    def set_savings_goal(self):
        amount = float(input("Enter savings goal amount: "))
        duration = input("Enter duration (e.g., Monthly): ")
        self.engine.set_savings_goal(self.engine.db, amount, duration)
        print("Savings goal set.")

    def add_to_savings(self):
        amount = float(input("Enter amount to add to savings: "))
        self.engine.add_savings(self.engine.db, amount)
        print(f"Added {amount} to savings.")

    def view_transaction_history(self):
        with DatabaseManager("finance.db") as db:
            txns = self.engine.get_all_transactions(db)
            print("Transaction History:")
            for t in txns:
                date, amount, category, account, note = t[1], t[2], t[3], t[4], t[5]
                print(f"Date: {date}, Amount: {amount}, Category: {category}, Account: {account}, Note: {note}")

    def view_savings_progress(self):
        current, remaining = self.engine.track_savings(self.engine.db)
        print(f"Current Savings: {current}")
        print(f"Remaining to Goal: {remaining}" if remaining > 0 else "Savings goal achieved!")

    def generate_report(self):
        summary = self.engine.generate_summary(self.engine.db)
        current, remaining = self.engine.track_savings(self.engine.db)
        print("Report:")
        print({
            "summary": summary,
            "savings_ok": (current, remaining)
        })

    def visualize_data(self):
        chart = input("Chart type (expense_vs_income | category_pie_chart | trend_analysis | top_expenses): ")
        self.engine.visualize_data(chart)

    def create_backup(self):
        path = input("Enter backup file path (default: backup_finance.db): ") or "backup_finance.db"
        result = BackupManager().create_backup(path)
        print(result)

if __name__ == "__main__":
    ui = FinanceUI()
    ui.handle_user_input()
