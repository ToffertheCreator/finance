from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDDatePicker
from datetime import timedelta

Window.maximize()

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<AnalyticsScreen>:
    name: "analytics"
    md_bg_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: 'horizontal'

        # Sidebar
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.2
            md_bg_color: 0, 0, 0, 1
            padding: 0, dp(24), 0, dp(24)
            spacing: dp(4)

            MDLabel:
                text: "FINANCE TRACKER"
                font_size: dp(22)
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_y: None
                height: self.texture_size[1] + dp(24)
                padding_x: dp(10)

            Widget:
                size_hint_y: None
                height: dp(8)

            MDFlatButton:
                text: "Dashboard"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.7
                font_size: dp(16)
                size_hint_y: None
                padding_x: dp(10)
                halign: "left"

            MDRelativeLayout:
                size_hint_y: None
                height: dp(40)

                MDBoxLayout:
                    md_bg_color: 1, 0.98, 0.93, 1
                    size_hint: 1, 1
                    pos_hint: {"x": 0, "y": 0}

                MDLabel:
                    text: "Analytics"
                    color: 0, 0, 0, 1
                    font_size: dp(16)
                    bold: True
                    pos_hint: {"center_y": 0.5}
                    x: dp(10)

            MDFlatButton:
                text: "Savings"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.7
                font_size: dp(16)
                size_hint_y: None
                padding_x: dp(10)
                halign: "left"

            MDFlatButton:
                text: "Transactions"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.7
                font_size: dp(16)
                size_hint_y: None
                padding_x: dp(10)
                halign: "left"

            MDFlatButton:
                text: "Settings"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.7
                font_size: dp(16)
                size_hint_y: None
                padding_x: dp(10)
                halign: "left"

            Widget:
                size_hint_y: 1

        # Main Content
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(32)
            size_hint_x: 0.8

            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: 0.5
                spacing: dp(10)

                MDLabel:
                    text: "ANALYTICS"
                    font_size: dp(36)
                    bold: True
                    halign: "left"
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(10)

                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    radius: [18]
                    md_bg_color: 1, 1, 1, 1
                    elevation: 1

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(36)
                        spacing: dp(10)

                        MDLabel:
                            text: "Trend"
                            halign: "left"
                            theme_text_color: "Primary"

                        MDRaisedButton:
                            id: date_picker_btn
                            text: root.date_range_text
                            on_release: root.show_date_picker()
                            md_bg_color: 1, 1, 1, 1
                            text_color: 0, 0, 0, 1
                            radius: [20]
                            elevation: 1
                            size_hint_x: None
                            width: dp(140)

                    MDLabel:
                        text: "[Bar Chart Placeholder]"
                        halign: "center"
                        theme_text_color: "Hint"

                    MDLabel:
                        text: "Legend: Income, Expenses, Expected"
                        halign: "center"
                        theme_text_color: "Hint"

            MDBoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.5
                spacing: dp(32)

                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(32)
                    size_hint_x: 0.3

                    MDCard:
                        padding: dp(10)
                        radius: [16]
                        elevation: 1

                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(8)
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}

                            MDLabel:
                                text: "Total Income"
                                theme_text_color: "Secondary"
                                halign: "center"
                            MDLabel:
                                text: f"₱{root.total_income:.2f}"
                                font_size: dp(36)
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#4CAF50")

                    MDCard:
                        padding: dp(10)
                        radius: [16]
                        elevation: 1

                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(8)
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}

                            MDLabel:
                                text: "Total Expenses"
                                theme_text_color: "Secondary"
                                halign: "center"
                            MDLabel:
                                text: f"₱{root.total_expenses:.2f}"
                                font_size: dp(36)
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#F44336")

                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    radius: [16]
                    elevation: 1

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
    date_range_text = StringProperty("Select Starting Date")

    def show_date_picker(self):
        picker = MDDatePicker()
        picker.bind(on_save=self.on_date)
        picker.open()

    def on_date(self, instance, value, date_range):
        end_date = value + timedelta(days=6)
        self.date_range_text = f"{value} to {end_date}"
        self.ids.date_picker_btn.text = self.date_range_text

class FinanceApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.theme_style = "Light"
        Builder.load_string(KV)
        return AnalyticsScreen(
            total_income=56789.00,
            total_expenses=23456.00
        )

if __name__ == "__main__":
    FinanceApp().run()
