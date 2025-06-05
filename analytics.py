from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty, StringProperty
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np

KV = '''
<AnalyticsScreen>:
    MDBoxLayout:
        orientation: 'horizontal'
        md_bg_color: 1, 1, 1, 1

        # Sidebar
        MDBoxLayout:
            id: sidebar
            orientation: "vertical"
            #padding: dp(10)
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
                size_hint_x: 1
                height: dp(40)
                md_bg_color: 1,1,1,1  # Highlighted background
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
                bold: True
                halign: "center"
                padding: 0, 0

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
                on_release: app.go_to_transactions()
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
                size_hint_y: 0.7
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

                    BoxLayout:
                        id: bar_chart_box
                        size_hint_y: 1
                        size_hint_x: 1
                        adaptive_size: True

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

    def on_kv_post(self, base_widget):
        self.ids.bar_chart_box.bind(size=self._update_chart_size)
        self.plot_bar_chart()
    
    def _update_chart_size(self, instance, value):
        self.plot_bar_chart()

    def plot_bar_chart(self):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        income = [6500, 4800, 9100, 6600, 1100, 3210, 4500, 5200, 6000, 7200, 8000, 9000]
        expenses = [4300, 5700, 7600, 4500, 300, 230, 1200, 1500, 2000, 2500, 3000, 3500]

        x = np.arange(len(months))
        width = 0.35

        chart_box = self.ids.bar_chart_box
        chart_box.clear_widgets()

        # Dynamically set figure size based on widget size (convert px to inches)
        dpi = 120
        width_in = max(chart_box.width / dpi, 4)
        height_in = max(chart_box.height / dpi, 3)
        fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=dpi)

        ax.bar(x - width/3, income, width, label='Income', color='#4CAF50')
        ax.bar(x + width/3, expenses, width, label='Expenses', color='#F44336')

        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.set_ylabel('Amount')
        ax.set_title('Income vs Expenses')
        ax.legend(loc='lower left', bbox_to_anchor=(0.85, 1), fontsize=6.4, markerscale=0.8, handlelength=1.5, borderaxespad=0.5, frameon=True)
        fig.subplots_adjust(left=0.12, right=0.95, top=0.85, bottom=0.18) 

        chart_box.add_widget(FigureCanvasKivyAgg(fig, size_hint=(1, 1)))
        plt.close(fig)

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