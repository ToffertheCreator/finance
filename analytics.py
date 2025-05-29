from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

KV = '''
#:import MDDropDownItem kivymd.uix.dropdownitem.MDDropDownItem

<SidebarLabel@MDLabel>:
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 0.7
    font_size: dp(16)
    size_hint_y: None
    height: self.texture_size[1] + dp(10)
    padding_x: dp(10)
    halign: "left"

<SidebarSelected@MDBoxLayout>:
    size_hint_y: None
    height: dp(40)
    md_bg_color: 1, 0.98, 0.93, 1  # Cream white
    padding: 0
    spacing: 0
    canvas.before:
        Color:
            rgba: 1, 0.98, 0.93, 1
        Rectangle:
            pos: self.pos
            size: self.size
    MDLabel:
        text: root.label_text if hasattr(root, 'label_text') else ""
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1  # Black text
        font_size: dp(16)
        halign: "left"
        valign: "middle"
        bold: True
        padding_x: dp(10)

MDScreen:
    md_bg_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: 'horizontal'

        # Sidebar
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.2
            md_bg_color: 0, 0, 0, 1
            padding: 0, dp(24), 0, dp(24)
            spacing: dp(16)

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

            SidebarLabel:
                text: "Dashboard"
            SidebarSelected:
                label_text: "Analytics"
            SidebarLabel:
                text: "Savings"
            SidebarLabel:
                text: "Transactions"
            SidebarLabel:
                text: "Settings"

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
                    font_size: dp(24)
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
                            on_release:
                                app.menu.open()

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
                                text: "₱123,456"
                                font_size: dp(26)
                                bold: True

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
                                text: "₱78,910"
                                font_size: dp(26)
                                bold: True

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

class FinanceApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def on_start(self):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": str(year),
                "on_release": lambda x=str(year): self.set_year(x),
            }
            for year in range(2025, 2009, -1)
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.year_dropdown,
            items=menu_items,
            width_mult=3,
        )

    def set_year(self, year):
        self.root.ids.year_dropdown.text = year
        self.menu.dismiss()

if __name__ == "__main__":
    FinanceApp().run()
