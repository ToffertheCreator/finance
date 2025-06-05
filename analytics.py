from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty, StringProperty

KV = '''
<AnalyticsScreen>:
    MDBoxLayout:
        orientation: 'horizontal'
        md_bg_color: 1, 1, 1, 1

        # Sidebar
        MDBoxLayout:
            id: sidebar
            orientation: "vertical"
            padding: dp(10)
            spacing: dp(15)
            size_hint_x: None
            width: dp(230)
            md_bg_color: 0, 0, 0, 1

            MDLabel:
                text: "FINANCE TRACKER"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(40)
                padding: dp(10), dp(10)

            MDFlatButton:
                text: "Dashboard"
                size_hint_y: None
                height: dp(40)
                on_release: root.go_to_dashboard()
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0

            MDFlatButton:
                text: "Analytics"
                size_hint_y: None
                height: dp(40)
                md_bg_color: 1, 0.98, 0.93, 1  # Highlighted background
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
                bold: True
                halign: "left"
                padding: dp(15), 0

            MDFlatButton:
                text: "Savings"
                size_hint_y: None
                height: dp(40)
                on_release: root.go_to_savings()
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0

            MDFlatButton:
                text: "Transactions"
                size_hint_y: None
                height: dp(40)
                on_release: root.go_to_transactions()
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0

            MDFlatButton:
                text: "Settings"
                size_hint_y: None
                height: dp(40)
                on_release: root.go_to_settings()
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0

            Widget:
                size_hint_y: 1

        # Main content
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_x: 0.8

            # Top half: Analytics Card
            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: 0.5
                padding: 0
                spacing: dp(10)

                MDLabel:
                    text: "ANALYTICS"
                    font_style: "H4"
                    bold: True
                    halign: "left"
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(10)

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    radius: [16]
                    md_bg_color: 1, 1, 1, 1
                    elevation: 1  # Less shadow
                    size_hint_y: 1

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(36)

                        MDLabel:
                            text: "Trend"
                            halign: "left"
                            theme_text_color: "Primary"

                        MDDropDownItem:
                            id: year_dropdown
                            text: "2025"
                            on_release: root.open_year_menu()

                    MDLabel:
                        text: "[Bar Chart Placeholder]"
                        halign: "center"
                        theme_text_color: "Hint"

                    MDLabel:
                        text: "Legend: Income, Expenses, Expected"
                        halign: "center"
                        theme_text_color: "Hint"

            # Bottom half: Stats and Pie Chart
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.5
                spacing: dp(10)
                padding: 0

                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(10)
                    size_hint_x: 0.3

                    MDCard:
                        padding: dp(10)
                        radius: [16]
                        elevation: 1
                        size_hint_y: 0.5

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: "Total Income"
                                theme_text_color: "Secondary"

                            MDLabel:
                                text: f"{root.total_income:.2f}"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#4CAF50")

                    MDCard:
                        padding: dp(10)
                        radius: [16]
                        elevation: 1
                        size_hint_y: 0.5

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: "Total Expenses"
                                theme_text_color: "Secondary"

                            MDLabel:
                                text: f"{root.total_expenses:.2f}"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#F44336")

                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    radius: [16]
                    elevation: 1
                    md_bg_color: 1, 1, 1, 1

                    MDBoxLayout:
                        size_hint_y: 0.5
                        spacing: dp(10)

                        MDLabel:
                            text: "[Pie Chart Income]"
                            halign: "center"
                            theme_text_color: "Hint"

                        MDLabel:
                            text: "[Pie Chart Expenses]"
                            halign: "center"
                            theme_text_color: "Hint"

                    MDBoxLayout:
                        spacing: dp(10)

                        MDLabel:
                            text: "Legend: Income Sources"
                            theme_text_color: "Hint"

                        MDLabel:
                            text: "Legend: Expense Sources"
                            theme_text_color: "Hint"
'''

class AnalyticsScreen(MDScreen):
    total_income = NumericProperty(0.0)
    total_expenses = NumericProperty(0.0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None

    # def on_kv_post(self, base_widget):
    #     # Called after the widget tree is ready
    #     menu_items = [
    #         {
    #             "viewclass": "OneLineListItem",
    #             "text": str(year),
    #             "on_release": lambda x=str(year): self.set_year(x),
    #         }
    #         for year in range(2025, 2009, -1)
    #     ]
    #     self.menu = MDDropdownMenu(
    #         caller=self.ids.year_dropdown,
    #         items=menu_items,
    #         width_mult=3,
    #     )

    def set_year(self, year):
        self.ids.year_dropdown.text = year
        self.menu.dismiss()
    
    def open_year_menu(self):
        if not self.menu:
            menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": str(year),
                    "on_release": lambda x=str(year): self.set_year(x),
                }
                for year in range(2025, 2009, -1)
            ]
            self.menu = MDDropdownMenu(
                caller=self.ids.year_dropdown,
                items=menu_items,
                width_mult=3,
            )
        self.menu.open()

    # Navigation methods
    def go_to_dashboard(self):
        self.manager.current = 'dashboard'

    def go_to_savings(self):
        pass

    def go_to_transactions(self):
        pass

    def go_to_settings(self):
        pass