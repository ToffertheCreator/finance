from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from backend import TransactionManager, DatabaseManager, Transaction


def txn_tuple_to_dict(txn):
    return {
        "id": txn[0],
        "date": txn[1],
        "amount": txn[2],
        "category": txn[3],
        "account": txn[4],
        "note": txn[5],
        "type": txn[6]
    }

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

<TransactionItem@MDBoxLayout>:
    category: ""
    date: ""
    account: ""
    note: ""
    amount: ""
    type: ""

    size_hint_y: None
    height: dp(40)
    padding: dp(10), 0

    MDLabel:
        text: root.category
        size_hint_x: 1.2
        halign: "left"

    MDLabel:
        text: root.date
        size_hint_x: 1
        halign: "left"

    MDLabel:
        text: root.account
        size_hint_x: 1
        halign: "left"

    MDLabel:
        text: root.note
        size_hint_x: 1.5
        halign: "left"

    MDLabel:
        text: root.amount
        size_hint_x: 0.8
        halign: "left"
        theme_text_color: "Custom"
        text_color: (0, 0.5, 0, 1) if root.type == "income" else (1, 0, 0, 1)


<TransactionsScreen@MDScreen>:
    name: 'transactions'
    MDBoxLayout:
        orientation: 'horizontal'

        MDBoxLayout:
            id: nav_drawer_panel
            orientation: "vertical"
            #padding: dp(10)
            spacing: dp(15)
            size_hint_x: None
            width: dp(230)
            md_bg_color: 0, 0, 0, 1

            MDLabel:
                text: "FINANCE TRACKER"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                bold: True
                size_hint_y: None
                height: dp(40)
                padding: dp(10), dp(10)

            MDFlatButton:
                text: "Dashboard"
                size_hint_y: None
                height: dp(40)
                on_release: app.go_to_dashboard()
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0

            MDFlatButton:
                text: "Analytics"
                size_hint_y: None
                height: dp(40)
                on_release: app.go_to_analytics()
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0

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
                size_hint_x: 1
                height: dp(40)
                md_bg_color: 1,1,1,1
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
                halign: "center"
                padding: 0, 0

            MDFlatButton:
                text: "Settings"
                size_hint_y: None
                height: dp(40)
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0

            MDBoxLayout:  # Spacer
                size_hint_y: 1

        MDBoxLayout:
            orientation: 'vertical'
            md_bg_color: 0.98, 0.98, 0.98, 1
    
            ScreenManager:
                id: screen_manager

                Screen:
                    name: "main"

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(10)
                        padding: dp(10)

                        MDLabel:
                            text: "TRANSACTIONS"
                            halign: "left"
                            bold: True
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
                                amount: f"{root.total_income:.2f}"
                                size_hint: 0.5, None 
                                on_release: root.show_income()

                            ClickableCard:
                                title: "Total Expenses"
                                amount: f"{root.total_expenses:.2f}"
                                size_hint: 0.5, None
                                on_release: root.show_expenses()

                        MDCard:  # Enclose transaction history in a card
                            orientation: 'vertical'
                            padding: dp(15)
                            spacing: dp(10)
                            size_hint_y: 1
                            elevation: 1
                            radius: [15, 15, 15, 15]

                            MDLabel:
                                text: "All Transactions"
                                font_style: "H6"
                                adaptive_height: True

                            MDLabel:
                                text: "All your transactions are recorded"
                                theme_text_color: "Hint"
                                adaptive_height: True

                            MDBoxLayout:  # Header
                                orientation: "horizontal"
                                size_hint_y: None
                                height: dp(40)
                                padding: (dp(10), 0)

                                MDLabel:
                                    text: "Category"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1.2

                                MDLabel:
                                    text: "Date"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1

                                MDLabel:
                                    text: "Account"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1

                                MDLabel:
                                    text: "Note"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1.5

                                MDLabel:
                                    text: "Amount"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 0.8

                            RecycleView:
                                id: main_rv
                                viewclass: 'TransactionItem'
                                bar_width: dp(5)

                                RecycleBoxLayout:
                                    default_size: None, dp(40)
                                    default_size_hint: 1, None
                                    size_hint_y: None
                                    height: self.minimum_height
                                    orientation: 'vertical'

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
                                amount: f"{root.total_income:.2f}"
                                on_release: root.go_to_main_page()

                        MDCard:  # Enclose transaction history in a card
                            orientation: 'vertical'
                            padding: dp(15)
                            spacing: dp(10)
                            size_hint_y: 1
                            elevation: 1
                            radius: [15, 15, 15, 15]

                            MDLabel:
                                text: "All Transactions"
                                font_style: "H6"
                                adaptive_height: True

                            MDLabel:
                                text: "All your transactions are recorded"
                                theme_text_color: "Hint"
                                adaptive_height: True

                            MDBoxLayout:  # Header
                                orientation: "horizontal"
                                size_hint_y: None
                                height: dp(40)
                                padding: (dp(10), 0)

                                MDLabel:
                                    text: "Category"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1.2

                                MDLabel:
                                    text: "Date"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1

                                MDLabel:
                                    text: "Account"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1

                                MDLabel:
                                    text: "Note"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1.5

                                MDLabel:
                                    text: "Amount"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 0.8

                            RecycleView:
                                id: income_rv
                                viewclass: 'TransactionItem'
                                bar_width: dp(5)

                                RecycleBoxLayout:
                                    default_size: None, dp(40)
                                    default_size_hint: 1, None
                                    size_hint_y: None
                                    height: self.minimum_height
                                    orientation: 'vertical'

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
                                amount: f"{root.total_expenses:.2f}"
                                on_release: root.go_to_main_page()

                        MDCard:  # Enclose transaction history in a card
                            orientation: 'vertical'
                            padding: dp(15)
                            spacing: dp(10)
                            size_hint_y: 1
                            elevation: 1
                            radius: [15, 15, 15, 15]

                            MDLabel:
                                text: "All Transactions"
                                font_style: "H6"
                                adaptive_height: True

                            MDLabel:
                                text: "All your transactions are recorded"
                                theme_text_color: "Hint"
                                adaptive_height: True

                            MDBoxLayout:  # Header
                                orientation: "horizontal"
                                size_hint_y: None
                                height: dp(40)
                                padding: (dp(10), 0)

                                MDLabel:
                                    text: "Category"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1.2

                                MDLabel:
                                    text: "Date"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1

                                MDLabel:
                                    text: "Account"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1

                                MDLabel:
                                    text: "Note"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 1.5

                                MDLabel:
                                    text: "Amount"
                                    halign: "left"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                                    size_hint_x: 0.8

                            RecycleView:
                                id: expenses_rv
                                viewclass: 'TransactionItem'
                                bar_width: dp(5)

                                RecycleBoxLayout:
                                    default_size: None, dp(40)
                                    default_size_hint: 1, None
                                    size_hint_y: None
                                    height: self.minimum_height
                                    orientation: 'vertical'
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

        amount_color = (0, 0.5, 0, 1) if transaction['type'].lower() == "income" else (1, 0, 0, 1)
        amount_label = create_label(f"{abs(transaction['amount']):.2f}", color=amount_color, size_hint_x=0.8)

        self.add_widget(category_label)
        self.add_widget(date_label)
        self.add_widget(account_label)
        self.add_widget(note_label)
        self.add_widget(amount_label)

class TransactionsScreen(MDScreen):
    total_income = NumericProperty(0.0)
    total_expenses = NumericProperty(0.0)
    transactions = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_dirty = True
        self._transaction_map = {}
        self._income_map = {}
        self._expenses_map = {}
        
    def on_pre_enter(self, *args):
        if self.data_dirty:
            self.transactions = self.fetch_transactions_from_db()
            self.calc_totals()
            self.populate_all()
            self.data_dirty = False 

    def fetch_transactions_from_db(self):
        with DatabaseManager("finance.db") as db:
            txns = TransactionManager.get_all_transactions(db)
            return [txn_tuple_to_dict(txn) for txn in txns]

    def calc_totals(self):
        self.total_income = sum(t["amount"] for t in self.transactions if t["type"].lower() == "income")
        self.total_expenses = sum(t["amount"] for t in self.transactions if t["type"].lower() == "expense")

    def populate_all(self):
        self.populate_main_history()
        self.populate_income_history()
        self.populate_expenses_history()

    def clear_layout(self, layout):
        layout.clear_widgets()

    def populate_main_history(self):
        rv = self.ids.main_rv
        new_txns = {
            t["id"]: {
                "category": t["category"],
                "date": t["date"],
                "account": t["account"],
                "note": t["note"],
                "amount": f"{abs(t['amount']):.2f}",
                "type": t["type"].lower()
            }
            for t in sorted(self.transactions, key=lambda x: x["date"], reverse=True)
        }

        # Only update what's changed
        old_txns = self._transaction_map
        updated_data = []
        for txn_id, txn_data in new_txns.items():
            if txn_id not in old_txns or old_txns[txn_id] != txn_data:
                updated_data.append(txn_data)
            else:
                updated_data.append(old_txns[txn_id])  # Unchanged, keep as is

        # Update RV only if something changed
        if updated_data != rv.data:
            rv.data = list(updated_data)

        self._transaction_map = new_txns
    
    def populate_income_history(self):
        rv = self.ids.income_rv

        income_txns = {
            t["id"]: {
                "category": t["category"],
                "date": t["date"],
                "account": t["account"],
                "note": t["note"],
                "amount": f"{abs(t['amount']):.2f}",
                "type": t["type"].lower()
            }
            for t in sorted(
                [x for x in self.transactions if x["type"].lower() == "income"],
                key=lambda x: x["date"],
                reverse=True
            )
        }

        updated_data = []
        old_data = self._income_map
        for txn_id, txn_data in income_txns.items():
            if txn_id not in old_data or old_data[txn_id] != txn_data:
                updated_data.append(txn_data)
            else:
                updated_data.append(old_data[txn_id])  # reuse unchanged data

        if updated_data != rv.data:
            rv.data = list(updated_data)

        self._income_map = income_txns
    
    def populate_expenses_history(self):
        rv = self.ids.expenses_rv

        expenses_txns = {
            t["id"]: {
                "category": t["category"],
                "date": t["date"],
                "account": t["account"],
                "note": t["note"],
                "amount": f"{abs(t['amount']):.2f}",
                "type": t["type"].lower()
            }
            for t in sorted(
                [x for x in self.transactions if x["type"].lower() == "expense"],
                key=lambda x: x["date"],
                reverse=True
            )
        }

        updated_data = []
        old_data = self._expenses_map
        for txn_id, txn_data in expenses_txns.items():
            if txn_id not in old_data or old_data[txn_id] != txn_data:
                updated_data.append(txn_data)
            else:
                updated_data.append(old_data[txn_id])

        if updated_data != rv.data:
            rv.data = list(updated_data)

        self._expenses_map = expenses_txns
    
    def show_income(self):
        self.ids.screen_manager.current = "income"

    def show_expenses(self):
        self.ids.screen_manager.current = "expenses"

    def go_to_main_page(self):
        self.ids.screen_manager.current = "main"

# class FinanceApp(MDApp):
#     def build(self):
#         self.title = "Finance App with KV String"
#         self.theme_cls.primary_palette = "Blue"
#         self.theme_cls.theme_style = "Light"
#         Builder.load_string(kv)
#         self.screen = TransactionsScreen()
#         self.screen.calc_totals()
#         self.screen.populate_all()
#         return self.screen
    
# if __name__ == "__main__":
#     FinanceApp().run()