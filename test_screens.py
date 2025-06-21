import unittest
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder

from dashboard import DashboardScreen, kv_string as dashboard_kv
from transactions import TransactionsScreen, kv as transactions_kv
from savings import SavingsScreen, KV as savings_kv

class TestApp(MDApp):
    def build(self):
        return ScreenManager()

class TestScreens(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp()
        cls.app.run = lambda *a, **kw: None
        cls.app._run_prepare()
        EventLoop.ensure_window()
        # Load all KV strings
        Builder.load_string(dashboard_kv)
        Builder.load_string(transactions_kv)
        Builder.load_string(savings_kv)

    def setUp(self):
        self.sm = ScreenManager()
        self.dashboard = DashboardScreen(name="dashboard")
        self.transactions = TransactionsScreen(name="transactions")
        self.savings = SavingsScreen(name="savings")
        self.sm.add_widget(self.dashboard)
        self.sm.add_widget(self.transactions)
        self.sm.add_widget(self.savings)

    def test_dashboard_screen_loads(self):
        self.sm.current = "dashboard"
        Clock.tick()
        self.assertEqual(self.sm.current, "dashboard")
        self.assertIsNotNone(self.dashboard)

    def test_transactions_screen_loads(self):
        self.sm.current = "transactions"
        Clock.tick()
        self.assertEqual(self.sm.current, "transactions")
        self.assertIsNotNone(self.transactions)

    def test_savings_screen_loads(self):
        self.sm.current = "savings"
        Clock.tick()
        self.assertEqual(self.sm.current, "savings")
        self.assertIsNotNone(self.savings)

if __name__ == "__main__":
    unittest.main()