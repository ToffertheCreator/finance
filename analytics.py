from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty, StringProperty
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from threading import Thread
from kivy.clock import Clock
from collections import defaultdict
import numpy as np
from backend import DatabaseManager, AnalyticsManager
import matplotlib
matplotlib.use('Agg')

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
                on_release: app.go_to_savings()
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

    def on_pre_enter(self):
        self.build_year_dropdown()
        self.update_analytics()

    def update_analytics(self):
        selected_year = self.ids.year_dropdown.text
        try:
            self.year = int(selected_year)
        except ValueError:
            self.year = None

        def worker():
            with DatabaseManager("finance.db") as db:
                analytics = AnalyticsManager(db)

                # Get totals
                total_income, total_expenses = analytics.get_totals(self.year)

                # Get chart data
                category_totals = analytics.get_category_totals(self.year)
                monthly_totals = analytics.get_monthly_totals(self.year)

            # Process chart data
            income_data = {k: v['income'] for k, v in category_totals.items() if v['income'] > 0}
            expense_data = {k: v['expense'] for k, v in category_totals.items() if v['expense'] > 0}
            income_data = self.group_small(income_data, 0.07)
            expense_data = self.group_small(expense_data, 0.07)

            # Generate chart figures
            bar_fig = self.build_monthly_chart(monthly_totals)
            pie_income_fig = self.build_pie_chart(income_data, "Income Breakdown")
            pie_expense_fig = self.build_pie_chart(expense_data, "Expense Breakdown")

            # Update UI
            Clock.schedule_once(lambda dt: self.update_totals(total_income, total_expenses))
            Clock.schedule_once(lambda dt: self.update_charts(bar_fig, pie_income_fig, pie_expense_fig))

        Thread(target=worker).start()

    def update_totals(self, income, expense):
        self.total_income = income
        self.total_expenses = expense

    def build_pie_chart(self, data_dict, title):
        fig, ax = plt.subplots(figsize=(3, 3))
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        total = sum(values)

        def autopct(pct):
            val = int(round(pct * total / 100.0))
            return f"{pct:.1f}%\n({val})"

        ax.pie(
            values,
            labels=labels,
            autopct=autopct,
            startangle=90,
            textprops={'fontsize': 9}
        )
        ax.axis('equal')
        ax.set_title(title, fontsize=12)
        return fig

    def build_monthly_chart(self, data):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        income = []
        expenses = []
        current_year = str(self.year) if hasattr(self, "year") and self.year else "2025"

        for i in range(1, 13):
            key = f"{current_year}-{i:02}"
            totals = data.get(key, {"income": 0, "expense": 0})
            income.append(totals["income"])
            expenses.append(totals["expense"])

        x = np.arange(len(months))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 4), dpi=100)
        ax.bar(x - width/2, income, width, label='Income', color="#FB8C00")
        ax.bar(x + width/2, expenses, width, label='Expenses', color="#000000")

        ax.set_ylabel('Amount')
        ax.set_title('Income vs Expenses by Month')
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend()
        fig.tight_layout()
        return fig

    def update_charts(self, bar_fig, income_fig, expense_fig):
        self.ids.bar_chart_box.clear_widgets()
        self.ids.income_pie_chart_box.clear_widgets()
        self.ids.expense_pie_chart_box.clear_widgets()

        self.ids.bar_chart_box.add_widget(FigureCanvasKivyAgg(bar_fig))
        self.ids.income_pie_chart_box.add_widget(FigureCanvasKivyAgg(income_fig))
        self.ids.expense_pie_chart_box.add_widget(FigureCanvasKivyAgg(expense_fig))

    def group_small(self, data, min_pct=0.05):
        total = sum(data.values())
        grouped, other = {}, 0
        for k, v in data.items():
            if total == 0 or v / total >= min_pct:
                grouped[k] = v
            else:
                other += v
        if other > 0:
            grouped['Other'] = other
        return grouped

    def set_year(self, year):
        self.ids.year_dropdown.text = year
        self.menu.dismiss()
        self.update_analytics()

    def build_year_dropdown(self):
        with DatabaseManager("finance.db") as db:
            analytics = AnalyticsManager(db)
            years = analytics.get_available_years()

        years = [str(y) for y in years if y is not None and str(y).strip()]

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": year,
                "on_release": lambda x=year: self.set_year(x),
            }
            for year in years
        ]

        if self.menu:
            self.menu.dismiss()

        self.menu = MDDropdownMenu(
            caller=self.ids.year_dropdown,
            items=menu_items,
            width_mult=3,
        )

        if years and self.ids.year_dropdown.text not in years:
            self.ids.year_dropdown.text = years[0]

    def open_year_menu(self):
        if self.menu:
            self.menu.open()

    def go_to_dashboard(self):
        self.manager.current = 'dashboard'