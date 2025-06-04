from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

kv = '''
<ClickableCard@MDCard>:
    title: ""
    amount: ""
    elevation: 2
    size_hint: None, None
    size: dp(250), dp(120)
    md_bg_color: 1, 1, 1, 1
    orientation: "vertical"
    padding: dp(10)

    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            text: root.title
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
            font_style: "H5"
            bold: True
            size_hint_y: None
            height: dp(40)

        MDLabel:
            text: root.amount
            halign: "center"
            theme_text_color: "Custom"
            font_style: "H6"
            text_color: (0, 0.5, 0, 1) if "Income" in root.title else (1, 0, 0, 1)

BoxLayout:
    orientation: "horizontal"

    MDBoxLayout:
        orientation: "vertical"
        size_hint_x: None
        width: dp(250)
        padding: dp(10)
        spacing: dp(10)
        md_bg_color: 0.1, 0.1, 0.1, 1

        BoxLayout:
            orientation: "vertical"
            size_hint_x: None
            width: dp(220)
            padding: dp(10)
            spacing: dp(12)

            MDRaisedButton:
                text: "Dashboard"
                size_hint: None, None
                size: dp(200), dp(50)
                on_release: app.root.ids.screen_manager.current = "Dashboard"

            MDRaisedButton:
                text: "Analytics"
                size_hint: None, None
                size: dp(200), dp(50)
                on_release: app.root.ids.screen_manager.current = "Analytics"

            MDRaisedButton:
                text: "Savings"
                size_hint: None, None
                size: dp(200), dp(50)
                on_release: app.root.ids.screen_manager.current = "Savings"

            MDRaisedButton:
                text: "Transactions"
                size_hint: None, None
                size: dp(200), dp(50)
                on_release: app.root.ids.screen_manager.current = "Settings"
                
            MDRaisedButton:
                text: "Settings"
                size_hint: None, None
                size: dp(200), dp(50)
                on_release: app.root.ids.screen_manager.current = "settings"

        Widget:
        Widget:

    ScreenManager:
        id: screen_manager

        Screen:
            name: "main"

            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(10)
                padding: dp(10)

                MDLabel:
                    text: "Transaction"
                    halign: "left"
                    font_style: "H4"
                    size_hint_y: None
                    height: dp(50)

                MDBoxLayout:
                    spacing: dp(10)
                    padding: dp(20)
                    size_hint_y: None
                    height: dp(150)


                    ClickableCard:
                        title: "Total Income"
                        amount: f"$ {app.total_income}"
                        size_hint: 0.5, None 
                        on_release: app.show_income()

                    ClickableCard:
                        title: "Total Expenses"
                        amount: f"$ {app.total_expenses}"
                        size_hint: 0.5, None
                        on_release: app.show_expenses()


                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: dp(40)
                    padding: (dp(10), 0)

                    MDLabel:
                        text: "HISTORY"
                        bold: True
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1
                        halign: "left"

                    Widget:

                    MDFillRoundFlatButton:
                        text: "Date"
                        size_hint: None, None
                        width: dp(100)
                        height: dp(36)

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(20)
                    padding: (dp(20), 0)
                    size_hint_y: None
                    height: dp(50)

                    MDLabel:
                        text: "Category"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Date"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Account"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Note"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Amount"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                ScrollView:
                    MDBoxLayout:
                        id: main_scroll_box
                        orientation: "vertical"
                        spacing: dp(10)
                        size_hint_y: None
                        padding: dp(10)
                        height: self.minimum_height


        Screen:
            name: "income"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(10)


                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(10)
                    size_hint: None, None
                    size: dp(250), dp(120)
                    pos_hint: {"center_x": 0.5}

                    ClickableCard:
                        title: "Total Income"
                        amount: f"${app.total_income:.2f}"
                        on_touch_down:
                            if self.collide_point(*args[1].pos): app.go_to_main_page()

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: dp(40)
                    padding: (dp(10), 0)

                    MDLabel:
                        text: "HISTORY"
                        bold: True
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1
                        halign: "left"

                    Widget:

                    MDFillRoundFlatButton:
                        text: "Date"
                        size_hint: None, None
                        width: dp(100)
                        height: dp(36)

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(20)
                    padding: (dp(20), 0)
                    size_hint_y: None
                    height: dp(50)

                    MDLabel:
                        text: "Category"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Date"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Account"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Note"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Amount"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                ScrollView:
                    MDBoxLayout:
                        id: income_scroll_box
                        orientation: "vertical"
                        spacing: dp(10)
                        size_hint_y: None
                        padding: dp(10)
                        height: self.minimum_height


        Screen:
            name: "expenses"
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(10)
                spacing: dp(10)


                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(10)
                    size_hint: None, None
                    size: dp(250), dp(120)
                    pos_hint: {"center_x": 0.5}

                    ClickableCard:
                        title: "Total Expenses"
                        amount: f"${app.total_expenses:.2f}"
                        on_touch_down:
                            if self.collide_point(*args[1].pos): app.go_to_main_page()

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: dp(40)
                    padding: (dp(10), 0)

                    MDLabel:
                        text: "HISTORY"
                        bold: True
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1
                        halign: "left"

                    Widget:

                    MDFillRoundFlatButton:
                        text: "Date"
                        size_hint: None, None
                        width: dp(100)
                        height: dp(36)

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(20)
                    padding: (dp(20), 0)
                    size_hint_y: None
                    height: dp(50)

                    MDLabel:
                        text: "Category"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Date"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Account"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Note"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                    MDLabel:
                        text: "Amount"
                        halign: "left"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1

                ScrollView:
                    MDBoxLayout:
                        id: expenses_scroll_box
                        orientation: "vertical"
                        spacing: dp(10)
                        size_hint_y: None
                        padding: dp(10)
                        height: self.minimum_height
'''

class TransactionRow(MDBoxLayout):
    def __init__(self, transaction, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(40)
        self.padding = [dp(10), 0, dp(10), 0]

        def create_label(text, color=(0, 0, 0, 1), size_hint_x=1):
            from kivymd.uix.label import MDLabel
            lbl = MDLabel(
                text=text,
                halign="left",
                theme_text_color="Custom",
                text_color=color,
                size_hint_x=size_hint_x,
                valign="middle",
                shorten=True,
                shorten_from="right",
            )
            lbl.bind(texture_size=lbl.setter('size'))
            return lbl


        category_label = create_label(transaction['category'], size_hint_x=1.2)
        date_label = create_label(transaction['date'], size_hint_x=1)
        account_label = create_label(transaction['account'], size_hint_x=1)
        note_label = create_label(transaction['note'], size_hint_x=1.5)

        amount_color = (0, 0.5, 0, 1) if transaction['amount'] > 0 else (1, 0, 0, 1)
        amount_label = create_label(f"${abs(transaction['amount']):.2f}", color=amount_color, size_hint_x=0.8)

        self.add_widget(category_label)
        self.add_widget(date_label)
        self.add_widget(account_label)
        self.add_widget(note_label)
        self.add_widget(amount_label)



class FinanceApp(MDApp):
    total_income = 3000     #values sa income
    total_expenses = 2000   #values sa expense

    transactions = [
        {"category": "Salary", "date": "2023-06-01", "account": "Bank", "note": "Monthly salary", "amount": 3000},
        {"category": "Groceries", "date": "2023-06-02", "account": "Credit Card", "note": "Food", "amount": -150},
        {"category": "Freelance", "date": "2023-06-03", "account": "Paypal", "note": "Project", "amount": 800},
        {"category": "Rent", "date": "2023-06-05", "account": "Bank", "note": "Apartment", "amount": -1200},
        {"category": "Investment", "date": "2023-06-07", "account": "Broker", "note": "Stocks", "amount": 500},
        {"category": "Utilities", "date": "2023-06-08", "account": "Bank", "note": "Electricity", "amount": -200},
    ] # values sa list

    def build(self):
        self.title = "Finance App with KV String"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.screen = Builder.load_string(kv)

        self.calc_totals()
        self.populate_all()

        return self.screen

    def calc_totals(self):
        self.total_income = sum(t["amount"] for t in self.transactions if t["amount"] > 0)
        self.total_expenses = -sum(t["amount"] for t in self.transactions if t["amount"] < 0)

    def populate_all(self):
        self.populate_main_history()
        self.populate_income_history()
        self.populate_expenses_history()

    def clear_layout(self, layout):
        layout.clear_widgets()

    def populate_main_history(self):
        box = self.screen.ids.main_scroll_box
        self.clear_layout(box)
        for t in sorted(self.transactions, key=lambda x: x["date"], reverse=True):
            box.add_widget(TransactionRow(t))

    def populate_income_history(self):
        box = self.screen.ids.income_scroll_box
        self.clear_layout(box)
        for t in sorted([x for x in self.transactions if x["amount"] > 0], key=lambda x: x["date"], reverse=True):
            box.add_widget(TransactionRow(t))

    def populate_expenses_history(self):
        box = self.screen.ids.expenses_scroll_box
        self.clear_layout(box)
        for t in sorted([x for x in self.transactions if x["amount"] < 0], key=lambda x: x["date"], reverse=True):
            box.add_widget(TransactionRow(t))

    def show_income(self):
        self.screen.ids.screen_manager.current = "income"

    def show_expenses(self):
        self.screen.ids.screen_manager.current = "expenses"

    def go_to_main_page(self):
        self.screen.ids.screen_manager.current = "main"


if __name__ == "__main__":
    FinanceApp().run()
