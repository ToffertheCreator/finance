import unittest
import os
from backend import DatabaseManager, TransactionManager, Transaction, SavingsManager, AnalyticsManager

TEST_DB = "test_finance.db"

class TestFinanceBackend(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        self.db = DatabaseManager(TEST_DB)
        self.db.__enter__()

    def tearDown(self):
        self.db.__exit__(None, None, None)
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    # Transaction tests
    def test_add_transaction(self):
        txn = Transaction("2025-06-19", 100.0, "Salary", "Bank", "June Salary", "income")
        TransactionManager.add(self.db, txn)
        txns = TransactionManager.get_all(self.db)
        self.assertEqual(len(txns), 1)

    def test_get_transaction_by_date(self):
        txn = Transaction("2025-06-19", 100.0, "Salary", "Bank", "June Salary", "income")
        TransactionManager.add(self.db, txn)
        txn_row = TransactionManager.get_transaction_by_date(self.db, "2025-06-19")
        self.assertIsNotNone(txn_row)
        self.assertEqual(txn_row[2], 100.0)

    def test_get_transaction_by_type(self):
        txn = Transaction("2025-06-19", 100.0, "Salary", "Bank", "June Salary", "income")
        TransactionManager.add(self.db, txn)
        txns_income = TransactionManager.get_transaction_by_type(self.db, "income")
        self.assertEqual(len(txns_income), 1)

    def test_edit_transaction(self):
        txn = Transaction("2025-06-19", 100.0, "Salary", "Bank", "June Salary", "income")
        TransactionManager.add(self.db, txn)
        TransactionManager.edit_transaction(self.db, "2025-06-19", 150.0, "Bonus", "Bank", "Edited", "income")
        txn_row = TransactionManager.get_transaction_by_date(self.db, "2025-06-19")
        self.assertEqual(txn_row[2], 150.0)
        self.assertEqual(txn_row[3], "Bonus")
        self.assertEqual(txn_row[5], "Edited")

    def test_delete_transaction(self):
        txn = Transaction("2025-06-19", 100.0, "Salary", "Bank", "June Salary", "income")
        TransactionManager.add(self.db, txn)
        TransactionManager.delete(self.db, "2025-06-19")
        txns = TransactionManager.get_all(self.db)
        self.assertEqual(len(txns), 0)

    # Savings tests
    def test_set_savings_goal(self):
        SavingsManager.set_savings_goal(self.db, "Vacation", 1000, "2025-12-31")
        row = self.db.run_query("SELECT * FROM savings WHERE name = ?", ("Vacation",), fetchone=True)
        self.assertIsNotNone(row)
        self.assertEqual(row[1], "Vacation")
        self.assertEqual(row[2], 0)
        self.assertEqual(row[3], 1000)

    def test_add_savings(self):
        SavingsManager.set_savings_goal(self.db, "Vacation", 1000, "2025-12-31")
        SavingsManager.add(self.db, "Vacation", 200)
        row = self.db.run_query("SELECT current_saved FROM savings WHERE name = ?", ("Vacation",), fetchone=True)
        self.assertEqual(row[0], 200)

    def test_track_savings(self):
        SavingsManager.set_savings_goal(self.db, "Vacation", 1000, "2025-12-31")
        SavingsManager.add(self.db, "Vacation", 200)
        current, remaining = SavingsManager.track_savings(self.db)
        self.assertEqual(current, 200)
        self.assertEqual(remaining, 800)

    def test_get_savings_name(self):
        SavingsManager.set_savings_goal(self.db, "Vacation", 1000, "2025-12-31")
        name = SavingsManager.get_savings_name(self.db)
        self.assertEqual(name, "Vacation")

    def test_get_savings_target_date(self):
        SavingsManager.set_savings_goal(self.db, "Vacation", 1000, "2025-12-31")
        date = SavingsManager.get_savings_target_date(self.db)
        self.assertEqual(date, "2025-12-31")

    def test_get_savings_history(self):
        SavingsManager.set_savings_goal(self.db, "Vacation", 1000, "2025-12-31")
        SavingsManager.add(self.db, "Vacation", 200)
        history = SavingsManager.get_savings_history(self.db)
        self.assertTrue(any(h[0] == "Vacation" and h[2] == 200 for h in history))

    def test_delete_savings(self):
        SavingsManager.set_savings_goal(self.db, "Vacation", 1000, "2025-12-31")
        SavingsManager.delete(self.db, "Vacation")
        row = self.db.run_query("SELECT * FROM savings WHERE name = ?", ("Vacation",), fetchone=True)
        self.assertIsNone(row)

    # Analytics tests
    def test_analytics_get_totals(self):
        TransactionManager.add(self.db, Transaction("2024-01-10", 1000, "Salary", "Bank", "Jan Salary", "income"))
        TransactionManager.add(self.db, Transaction("2024-01-15", -200, "Food", "Cash", "Groceries", "expense"))
        total_income, total_expense = AnalyticsManager.get_totals(self.db, year="2024")
        self.assertEqual(total_income, 1000)
        self.assertEqual(total_expense, 200)

    def test_analytics_get_category_totals(self):
        TransactionManager.add(self.db, Transaction("2024-01-10", 1000, "Salary", "Bank", "Jan Salary", "income"))
        TransactionManager.add(self.db, Transaction("2024-01-15", -200, "Food", "Cash", "Groceries", "expense"))
        cat_totals = AnalyticsManager.get_category_totals(self.db, year="2024")
        self.assertEqual(cat_totals["Salary"]["income"], 1000)
        self.assertEqual(cat_totals["Food"]["expense"], 200)

    def test_analytics_get_monthly_totals(self):
        TransactionManager.add(self.db, Transaction("2024-01-10", 1000, "Salary", "Bank", "Jan Salary", "income"))
        TransactionManager.add(self.db, Transaction("2024-01-15", -200, "Food", "Cash", "Groceries", "expense"))
        monthly_totals = AnalyticsManager.get_monthly_totals(self.db, year="2024")
        self.assertEqual(monthly_totals["2024-01"]["income"], 1000)
        self.assertEqual(monthly_totals["2024-01"]["expense"], 200)

    def test_analytics_get_available_years(self):
        TransactionManager.add(self.db, Transaction("2024-01-10", 1000, "Salary", "Bank", "Jan Salary", "income"))
        TransactionManager.add(self.db, Transaction("2025-03-05", 1200, "Salary", "Bank", "Mar Salary", "income"))
        years = AnalyticsManager.get_available_years(self.db)
        self.assertIn("2024", years)
        self.assertIn("2025", years)

if __name__ == "__main__":
    unittest.main(verbosity=2)