from kivymd.app import MDApp  # Import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from dashboard import DashboardScreen, kv_string
from analytics import KV  # Import KV string from analytics
from kivy.lang import Builder

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class MainApp(MDApp):  # Inherit from MDApp
    def build(self):
        Builder.load_string(kv_string)  # Load dashboard KV
        Builder.load_string(KV)  # Load analytics KV
        sm = ScreenManagement()
        sm.add_widget(DashboardScreen(name='dashboard'))
        analytics_screen = Screen(name='analytics')  # Create a Screen for Analytics
        analytics_content = Builder.load_string(KV) # Load the KV string and get the root widget
        analytics_screen.add_widget(analytics_content) # Add the content to the screen
        sm.add_widget(analytics_screen)
        self.sm = sm 
        return sm

    def go_to_dashboard(self):
        self.sm.current = 'dashboard'

    def go_to_savings(self):
        pass  # Implement as needed

    def go_to_transactions(self):
        pass  # Implement as needed

    def go_to_settings(self):
        pass  # Implement as needed

if __name__ == '__main__':
    MainApp().run()