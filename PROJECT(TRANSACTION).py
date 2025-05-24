from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView


income = 1000.00

transactions = [
    {"category": "Food", "date": "2025-05-01", "account": "Cash", "note": "Lunch", "amount": -120},
    {"category": "Salary", "date": "2025-05-05", "account": "Bank", "note": "Monthly Salary", "amount": 1500.00},
    {"category": "Transport", "date": "2025-05-10", "account": "Card", "note": "Bus fare", "amount": 3.00},
    {"category": "Food", "date": "2025-05-01", "account": "Cash", "note": "Lunch", "amount": -120},
    {"category": "Salary", "date": "2025-05-05", "account": "Bank", "note": "Monthly Salary", "amount": 1500.00},
    {"category": "Food", "date": "2025-05-01", "account": "Cash", "note": "Lunch", "amount": -120},
    {"category": "Salary", "date": "2025-05-05", "account": "Bank", "note": "Monthly Salary", "amount": 1500.00},
    {"category": "Food", "date": "2025-05-01", "account": "Cash", "note": "Lunch", "amount": -120},
    {"category": "Salary", "date": "2025-05-05", "account": "Bank", "note": "Monthly Salary", "amount": 1500.00},
    {"category": "Food", "date": "2025-05-01", "account": "Cash", "note": "Lunch", "amount": -120},
    {"category": "Salary", "date": "2025-05-05", "account": "Bank", "note": "Monthly Salary", "amount": 1500.00},

]

class ClickableCard(MDCard):
    def __init__(self, title, amount, on_click, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (None, None)
        self.size = (dp(250), dp(120))
        self.elevation = 2
        self.md_bg_color = (1, 1, 1, 1)
        self.orientation = "vertical"
        self.padding = dp(10)
        self.on_click = on_click

        layout = MDBoxLayout(orientation="vertical")
        self.add_widget(layout)

        title_label = MDLabel( text=title, halign="center", theme_text_color="Custom", text_color=(0, 0, 0, 1), font_style="H5", bold=True, size_hint_y=None, height=dp(40),)

        self.amount_label = MDLabel(text=amount, halign="center", theme_text_color="Custom", text_color=(1, 0, 0, 1), font_style="H6", )

        layout.add_widget(title_label)
        layout.add_widget(self.amount_label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.on_click()
            return True
        return super().on_touch_down(touch)


class MyApp(MDApp):
    def build(self):
        root_layout = MDBoxLayout(orientation="horizontal")

        # Left Navigation
        nav_box = MDBoxLayout(orientation="vertical", size_hint_x=0.25, padding=dp(10), spacing=dp(10), md_bg_color=(0.1, 0.1, 0.1, 1),)

        nav_top = MDBoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        nav_top.bind(minimum_height=nav_top.setter("height"))

        nav_top.add_widget(
            MDLabel(text="TRANSACTIONS", font_style="H5", halign="left", valign="top", theme_text_color="Custom", text_color=(1, 1, 1, 1), size_hint_y= None, height=dp(40),
            )
        )

        nav_items = ["Dashboard", "Analytics", "Savings", "Transaction", "Settings"]
        for item in nav_items:
            btn = MDRaisedButton(
                text=item,
                height=dp(50),
                size_hint=(1, None),
                md_bg_color=(0.2, 0.6, 1, 1) if item == "Transaction" else (0, 0, 0, 0),
                text_color=(1, 1, 1, 1),
                elevation=8 if item == "Transaction" else 2,
            )
            btn.bind(on_release=lambda x, scr=item.lower(): setattr(self.screen_manager, 'current', scr))
            nav_top.add_widget(btn)

        nav_box.add_widget(nav_top)
        nav_box.add_widget(Widget())

        self.screen_manager = ScreenManager()

#main screen
        main_screen = Screen(name="main")
        content_box = MDBoxLayout(orientation="vertical", padding=dp(50), spacing=dp(8)) # spacing = 10

        top_info_column = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(600), padding=(dp(10), 0), spacing=dp(10))

        transactions_label = MDLabel(text="TRANSACTIONS", halign="left", valign="top", size_hint_y = None, height=dp(80), theme_text_color="Custom", text_color=(0, 0, 0, 1), font_style="H4", bold=True,)

        top_info_column.add_widget(transactions_label)

        income_buttons_box = MDBoxLayout(
            orientation="horizontal", spacing=dp(20), size_hint=(None, None), size=(dp(520), dp(120)), pos_hint={"center_x": 0.5},)

        income_card = ClickableCard("Total Income", f"${income:.2f}", on_click=self.show_income)
        income_card.amount_label.text_color = (0, 0.5, 0, 1)

        total_expenses = sum(txn["amount"] for txn in transactions if txn["amount"] < 0)
        expense_card = ClickableCard("Total Expenses", f"${-total_expenses:.2f}", on_click=self.show_expenses)
        expense_card.amount_label.text_color = (1, 0, 0, 1)

        income_buttons_box.add_widget(income_card)
        income_buttons_box.add_widget(expense_card)
        top_info_column.add_widget(income_buttons_box)

        # history and date row
        history_row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), padding=(dp(10), 0),)

        history_label = MDLabel(text="HISTORY", bold=True, font_style="H6", theme_text_color="Custom", text_color=(0, 0, 0, 1), halign="left",)

        date_button = MDFillRoundFlatButton(text="Date", size_hint=(None, None), width=dp(100), height=dp(36), pos_hint={"center_y": 0.5},)

        history_row.add_widget(history_label)
        history_row.add_widget(Widget())
        history_row.add_widget(date_button)
        top_info_column.add_widget(history_row)

        # transaction columns
        header = MDBoxLayout(orientation="horizontal", spacing=dp(20), padding=(dp(20), 0), size_hint_y=None, height=dp(50))
        for title in ["Category", "Date", "Account", "Note", "Amount"]:
            header.add_widget(
                MDLabel(text=title, halign="left", bold=True, theme_text_color="Custom", text_color=(0, 0, 0, 1))
            )

        scroll = MDScrollView(size_hint=(1, 1), height=dp(300))
        scroll_box = MDBoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=dp(10))
        scroll_box.bind(minimum_height=scroll_box.setter("height"))

        for txn in transactions:
            row = MDBoxLayout(
                orientation="horizontal", spacing=dp(20), size_hint_y=None, height=dp(40), padding=(dp(20), 0)
            )
            row.add_widget(MDLabel(text=txn["category"], halign="left"))
            row.add_widget(MDLabel(text=txn["date"], halign="left"))
            row.add_widget(MDLabel(text=txn["account"], halign="left"))
            row.add_widget(MDLabel(text=txn["note"], halign="left"))
            amount_color = (0, 0.5, 0, 1) if txn["amount"] > 0 else (1, 0, 0, 1)
            row.add_widget(
                MDLabel(
                    text=f"{txn['amount']:+.2f}",
                    halign="left",
                    theme_text_color="Custom",
                    text_color=amount_color,
                )
            )
            scroll_box.add_widget(row)

        scroll.add_widget(scroll_box)

        top_info_column.add_widget(header)
        top_info_column.add_widget(scroll)
        content_box.add_widget(top_info_column)
        main_screen.add_widget(content_box)

        # income screen
        income_screen = Screen(name="income")
        income_layout = MDBoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        top_info_column = MDBoxLayout(
            orientation="vertical", size_hint_y=None, height=dp(600), padding=(dp(10), 0), spacing=dp(10)
        )

        income_label = MDLabel(text="TRANSACTION", halign="left", font_style="H5", theme_text_color="Custom", text_color=(0, 0, 0, 1), bold=True, size_hint_y=None, height=dp(50),)
        top_info_column.add_widget(income_label)

        income_buttons_box = MDBoxLayout(
            orientation="horizontal", spacing=dp(20), size_hint=(None, None), size=(dp(250), dp(120)),pos_hint={"center_x": 0.5},)

        income_card = ClickableCard("Total Income", f"${income:.2f}", on_click=self.show_income)
        income_card.amount_label.text_color = (0, 0.5, 0, 1)

        income_buttons_box.add_widget(income_card)
        top_info_column.add_widget(income_buttons_box)

        history_row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), padding=(dp(10), 0))
        history_label = MDLabel(text="HISTORY", bold=True, font_style="H6", theme_text_color="Custom", text_color=(0, 0, 0, 1), halign="left")
        date_button = MDFillRoundFlatButton(text="Date", size_hint=(None, None), width=dp(100), height=dp(36))
        history_row.add_widget(history_label)
        history_row.add_widget(Widget())
        history_row.add_widget(date_button)
        top_info_column.add_widget(history_row)

        # Income Transactions Only
        header = MDBoxLayout(orientation="horizontal", spacing=dp(20), padding=(dp(20), 0), size_hint_y=None, height=dp(50))
        for title in ["Category", "Date", "Account", "Note", "Amount"]:
            header.add_widget(
                MDLabel(text=title, halign="left", bold=True, theme_text_color="Custom", text_color=(0, 0, 0, 1))
            )

        scroll = MDScrollView(size_hint=(1, None), height=dp(300))
        scroll_box = MDBoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=dp(10))
        scroll_box.bind(minimum_height=scroll_box.setter("height"))

        for txn in transactions:
            if txn["amount"] > 0:
                row = MDBoxLayout(orientation="horizontal", spacing=dp(20), size_hint_y=None, height=dp(40), padding=(dp(20), 0))
                row.add_widget(MDLabel(text=txn["category"], halign="left"))
                row.add_widget(MDLabel(text=txn["date"], halign="left"))
                row.add_widget(MDLabel(text=txn["account"], halign="left"))
                row.add_widget(MDLabel(text=txn["note"], halign="left"))
                row.add_widget(
                    MDLabel(text=f"{txn['amount']:+.2f}", halign="left", theme_text_color="Custom", text_color=(0, 0.5, 0, 1),)
                )
                scroll_box.add_widget(row)

        scroll.add_widget(scroll_box)
        top_info_column.add_widget(header)
        top_info_column.add_widget(scroll)
        income_layout.add_widget(top_info_column)
        income_screen.add_widget(income_layout)

        # --- Expenses Screen ---
        expenses_screen = Screen(name="expenses")
        expenses_layout = MDBoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        top_info_column = MDBoxLayout(
            orientation="vertical", size_hint_y=None, height=dp(600), padding=(dp(10), 0), spacing=dp(10)
        )

        expenses_label = MDLabel( text="TRANSACTION", halign="left", font_style="H5", theme_text_color="Custom", text_color=(0, 0, 0, 1), bold=True, size_hint_y=None, height=dp(50),)

        top_info_column.add_widget(expenses_label)

        expense_buttons_box = MDBoxLayout(orientation="horizontal", spacing=dp(20), size_hint=(None, None), size=(dp(250), dp(120)), pos_hint={"center_x": 0.5},)

        total_expenses = sum(txn["amount"] for txn in transactions if txn["amount"] < 0)
        expense_card = ClickableCard("Total Expenses", f"${-total_expenses:.2f}", on_click=self.show_expenses)
        expense_card.amount_label.text_color = (1, 0, 0, 1)

        expense_buttons_box.add_widget(expense_card)
        top_info_column.add_widget(expense_buttons_box)

        history_row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), padding=(dp(10), 0))
        history_label = MDLabel(text="HISTORY", bold=True, font_style="H6", theme_text_color="Custom", text_color=(0, 0, 0, 1), halign="left")
        date_button = MDFillRoundFlatButton(text="Date", size_hint=(None, None), width=dp(100), height=dp(36))
        history_row.add_widget(history_label)
        history_row.add_widget(Widget())
        history_row.add_widget(date_button)
        top_info_column.add_widget(history_row)

        header = MDBoxLayout(orientation="horizontal", spacing=dp(20), padding=(dp(20), 0), size_hint_y=None, height=dp(50))
        for title in ["Category", "Date", "Account", "Note", "Amount"]:
            header.add_widget(
                MDLabel(text=title, halign="left", bold=True, theme_text_color="Custom", text_color=(0, 0, 0, 1))
            )

        scroll = MDScrollView(size_hint=(1, None), height=dp(300))
        scroll_box = MDBoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=dp(10))
        scroll_box.bind(minimum_height=scroll_box.setter("height"))

        for txn in transactions:
            if txn["amount"] < 0:
                row = MDBoxLayout(orientation="horizontal", spacing=dp(20), size_hint_y=None, height=dp(40), padding=(dp(20), 0))
                row.add_widget(MDLabel(text=txn["category"], halign="left", size_hint_x = 0.2))
                row.add_widget(MDLabel(text=txn["date"], halign="left",size_hint_x = 0.2))
                row.add_widget(MDLabel(text=txn["account"], halign="left",size_hint_x = 0.2))
                row.add_widget(MDLabel(text=txn["note"], halign="left",size_hint_x = 0.2))
                row.add_widget(
                    MDLabel(
                        text=f"{txn['amount']:+.2f}",
                        halign="left",
                        theme_text_color="Custom",
                        text_color=(1, 0, 0, 1),
                    )
                )
                scroll_box.add_widget(row)

        scroll.add_widget(scroll_box)
        top_info_column.add_widget(header)
        top_info_column.add_widget(scroll)
        expenses_layout.add_widget(top_info_column)
        expenses_screen.add_widget(expenses_layout)

        # Add screens to manager
        self.screen_manager.add_widget(main_screen)
        self.screen_manager.add_widget(income_screen)
        self.screen_manager.add_widget(expenses_screen)

        root_layout.add_widget(nav_box)
        root_layout.add_widget(self.screen_manager)

        return root_layout

    def show_income(self):
        self.screen_manager.current = "income"

    def show_expenses(self):
        self.screen_manager.current = "expenses"


if __name__ == "__main__":
    MyApp().run()
