from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

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
                on_release: app.root.ids.screen_manager.current = "savings"
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
                on_release: app.root.ids.screen_manager.current = "settings"
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
                                amount: f"${root.total_income:.2f}"
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
                                amount: f"${root.total_expenses:.2f}"
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

class TransactionsScreen(MDScreen):
    total_income = NumericProperty(0.0)
    total_expenses = NumericProperty(0.0)
    transactions = ListProperty([])

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
        box = self.ids.main_scroll_box
        self.clear_layout(box)
        for t in sorted(self.transactions, key=lambda x: x["date"], reverse=True):
            box.add_widget(TransactionRow(t))

    def populate_income_history(self):
        box = self.ids.income_scroll_box
        self.clear_layout(box)
        for t in sorted([x for x in self.transactions if x["amount"] > 0], key=lambda x: x["date"], reverse=True):
            box.add_widget(TransactionRow(t))

    def populate_expenses_history(self):
        box = self.ids.expenses_scroll_box
        self.clear_layout(box)
        for t in sorted([x for x in self.transactions if x["amount"] < 0], key=lambda x: x["date"], reverse=True):
            box.add_widget(TransactionRow(t))

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