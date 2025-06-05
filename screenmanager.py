from kivymd.app import MDApp  # Import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from dashboard import DashboardScreen, kv_string
from analytics import KV, AnalyticsScreen
from transactions import TransactionsScreen, kv as transactions_kv
from kivy.lang import Builder

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class MainApp(MDApp):  # Inherit from MDApp
    def build(self):
        Builder.load_string(kv_string)  # Load dashboard KV
        Builder.load_string(KV)  # Load analytics KV
        Builder.load_string(transactions_kv)
        sm = ScreenManagement()
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(AnalyticsScreen(name='analytics'))
        sm.add_widget(TransactionsScreen(name='transactions'))
        self.sm = sm 
        return sm

    def go_to_dashboard(self):
        self.sm.current = 'dashboard'
    
    def go_to_analytics(self):
        self.sm.current = 'analytics'

    def go_to_savings(self):
        pass  # Implement as needed

    def go_to_transactions(self):
        self.sm.current = 'transactions'

    def go_to_settings(self):
        pass  # Implement as needed

if __name__ == '__main__':
    MainApp().run()