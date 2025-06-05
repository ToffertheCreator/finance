from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty, StringProperty
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from collections import defaultdict
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

                        BoxLayout:
                            id: income_pie_chart_box
                            size_hint_x: 0.5

                        BoxLayout:
                            id: expense_pie_chart_box
                            size_hint_x: 0.5
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
        self.plot_pie_charts()
    
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

        ax.bar(x - width/3, income, width, label='Income', color="#FB8C00")
        ax.bar(x + width/3, expenses, width, label='Expenses', color="#000000")

        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.set_ylabel('Amount')
        ax.set_title('Income vs Expenses')
        ax.legend(loc='lower left', bbox_to_anchor=(0.85, 1), fontsize=6.4, markerscale=0.8, handlelength=1.5, borderaxespad=0.5, frameon=True)
        fig.subplots_adjust(left=0.12, right=0.95, top=0.85, bottom=0.18) 

        chart_box.add_widget(FigureCanvasKivyAgg(fig, size_hint=(1, 1)))
        plt.close(fig)
    
    def plot_pie_charts(self):
        # Example/mock data, replace with your real data as needed
        income_data = [
            {'Salary': 4000, 'Freelance': 1000, 'Investments': 500},
            {'Salary': 4200, 'Freelance': 1100, 'Investments': 600},
            {'Salary': 4300, 'Freelance': 900, 'Investments': 700},
            {'Salary': 4400, 'Freelance': 950, 'Investments': 750},
            {'Salary': 4600, 'Freelance': 1050, 'Investments': 800},
            {'Salary': 4700, 'Freelance': 1100, 'Investments': 900},
        ]
        expense_data = [
            {'Rent': 1500, 'Groceries': 800, 'Entertainment': 300, 'Utilities': 200},
            {'Rent': 1550, 'Groceries': 850, 'Entertainment': 350, 'Utilities': 250},
            {'Rent': 1600, 'Groceries': 900, 'Entertainment': 400, 'Utilities': 220},
            {'Rent': 1650, 'Groceries': 870, 'Entertainment': 370, 'Utilities': 230},
            {'Rent': 1700, 'Groceries': 890, 'Entertainment': 360, 'Utilities': 240},
            {'Rent': 1750, 'Groceries': 920, 'Entertainment': 380, 'Utilities': 260},
            {'movies': 1750, 'bills': 920, 'gf': 380, 'cocaine': 260},
            {'bail': 1232, 'meth': 1232, 'hookers': 3123, 'lawyer': 400},
        ]

        def aggregate(data_list):
            result = defaultdict(int)
            for month_data in data_list:
                for category, amount in month_data.items():
                    result[category] += amount
            return result
        
        def group_small_categories(data_dict, min_pct=0.05):
            total = sum(data_dict.values())
            grouped = {}
            other = 0
            for k, v in data_dict.items():
                if total == 0:
                    continue
                if v / total < min_pct:
                    other += v
                else:
                    grouped[k] = v
            if other > 0:
                grouped['Other'] = other
            return grouped

        income_totals = aggregate(income_data)
        expense_totals = aggregate(expense_data)
        income_totals = group_small_categories(income_totals, min_pct=0.07)   # 7% threshold
        expense_totals = group_small_categories(expense_totals, min_pct=0.07)

        # Clear previous widgets
        self.ids.income_pie_chart_box.clear_widgets()
        self.ids.expense_pie_chart_box.clear_widgets()

        # Income Pie
        fig1, ax1 = plt.subplots(figsize=(3, 3))
        self._plot_pie(ax1, income_totals, 'Income CAtegories Breakdown')
        self.ids.income_pie_chart_box.add_widget(FigureCanvasKivyAgg(fig1))
        plt.close(fig1)

        # Expense Pie
        fig2, ax2 = plt.subplots(figsize=(3, 3))
        self._plot_pie(ax2, expense_totals, 'Expense Categories Breakdown')
        self.ids.expense_pie_chart_box.add_widget(FigureCanvasKivyAgg(fig2))
        plt.close(fig2)

    def _plot_pie(self, ax, data_dict, title):
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        total = sum(values)

        def autopct(pct):
            val = int(round(pct * total / 100.0))
            return f"{pct:.1f}%\n(${val})"

        ax.pie(
            values,
            labels=labels,
            autopct=autopct,
            startangle=90,
            textprops={'fontsize': 9}
        )
        ax.axis('equal')
        ax.set_title(title, fontsize=12)

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