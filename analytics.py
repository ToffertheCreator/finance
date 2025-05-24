from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

KV = '''
MDScreen:
    md_bg_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: 'horizontal'

        # Sidebar
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.2
            md_bg_color: 0.08, 0.08, 0.08, 1
            padding: dp(10)
            spacing: dp(10)

            MDLabel:
                text: "FINANCE TRACKER"
                font_size: dp(20)
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_y: None
                height: self.texture_size[1] + dp(20)
                padding_x: dp(10)

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(10)

                MDLabel:
                    text: "Dashboard"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.7
                MDCard:
                    size_hint_y: None
                    height: dp(40)
                    md_bg_color: 1, 1, 1, 0.1
                    radius: [20]
                    padding: dp(10)

                    MDLabel:
                        text: "Analytics"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1

                MDLabel:
                    text: "Savings"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.7
                MDLabel:
                    text: "Transactions"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.7
                MDLabel:
                    text: "Settings"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.7

        # Main content
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            size_hint_x: 0.8

            MDLabel:
                text: "ANALYTICS"
                font_size: dp(24)
                bold: True
                halign: "left"

            MDCard:
                orientation: 'vertical'
                padding: dp(20)
                size_hint_y: 0.45
                radius: [20]
                md_bg_color: 1, 1, 1, 1
                elevation: 3

                MDBoxLayout:
                    size_hint_y: None
                    height: dp(30)

                    MDLabel:
                        text: "Trend"
                        halign: "left"

                    MDButton:
                        text: "2025"
                        style: "elevated"
                        md_bg_color: 0, 0.6, 0.3, 1
                        text_color: 1, 1, 1, 1
                        size_hint_x: None
                        width: dp(80)

                MDLabel:
                    text: "[Bar Chart Placeholder]"
                    halign: "center"
                    theme_text_color: "Hint"

                MDLabel:
                    text: "Legend: Income, Expenses, Expected"
                    halign: "center"
                    theme_text_color: "Hint"

            MDBoxLayout:
                size_hint_y: 0.5
                spacing: dp(20)

                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(20)
                    size_hint_x: 0.3

                    MDCard:
                        padding: dp(15)
                        radius: [20]
                        elevation: 3

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: "Total Income"
                                theme_text_color: "Secondary"

                            MDLabel:
                                text: "₱123,456"
                                font_size: dp(26)
                                bold: True

                    MDCard:
                        padding: dp(15)
                        radius: [20]
                        elevation: 3

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: "Total Expenses"
                                theme_text_color: "Secondary"

                            MDLabel:
                                text: "₱78,910"
                                font_size: dp(26)
                                bold: True

                MDCard:
                    orientation: "vertical"
                    padding: dp(20)
                    radius: [20]
                    elevation: 3
                    md_bg_color: 1, 1, 1, 1

                    MDBoxLayout:
                        size_hint_y: 0.5
                        spacing: dp(20)

                        MDLabel:
                            text: "[Pie Chart Income]"
                            halign: "center"
                            theme_text_color: "Hint"

                        MDLabel:
                            text: "[Pie Chart Expenses]"
                            halign: "center"
                            theme_text_color: "Hint"

                    MDBoxLayout:
                        spacing: dp(20)

                        MDLabel:
                            text: "Legend: Income Sources"
                            theme_text_color: "Hint"

                        MDLabel:
                            text: "Legend: Expense Sources"
                            theme_text_color: "Hint"
'''

class FinanceApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

if __name__ == "__main__":
    FinanceApp().run()
