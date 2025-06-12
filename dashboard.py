from kivy.utils import get_color_from_hex
from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivy.properties import DictProperty, StringProperty
from backend import TransactionManager, DatabaseManager, Transaction
from threading import Thread
from kivy.clock import Clock
from datetime import datetime
from kivy.storage.jsonstore import JsonStore


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

kv_string = """
<DialogContent>:
    orientation: "vertical"
    padding: 0
    size_hint_y: None
    width: dp(320) 
    adaptive_height: True 

    MDBoxLayout: 
        orientation: "horizontal"
        size_hint: (1, None) 
        height: dp(40) 
        md_bg_color: get_color_from_hex("#000000")
        padding: dp(20), 0, dp(10), 0
        
        MDLabel:
            text: root.dialog_title
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            halign: "left"
            valign: "center" 
            size_hint_x: 1 

        MDIconButton: 
            icon: "close"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {'center_y': .5, 'right': 1} 
            on_release: app.root.get_screen('dashboard').dismiss_current_dialog()

    MDBoxLayout: 
        orientation: "vertical"
        md_bg_color: get_color_from_hex ("#FFFFFF")
        spacing: dp(15)
        padding: dp(24) 
        adaptive_height: True
        MDTextField:
            id: category_field
            hint_text: "Category"
            mode: "rectangle"
            padding: dp(20), dp(15)
        MDTextField:
            id: date_field
            hint_text: "Enter date (YYYY-MM-DD)"
            mode: "rectangle"
            size_hint_y: None
            height: dp(48)
            helper_text: ""
            helper_text_mode: "on_error"
            error: False
        MDTextField:
            id: account_field
            hint_text: "Account"
            mode: "rectangle"
            padding: dp(20), dp(15)
        MDTextField:
            id: note_field
            hint_text: "Note"
            mode: "rectangle"
            padding: dp(20), dp(15)
        MDTextField:
            id: amount_field
            hint_text: "Amount"
            mode: "rectangle"
            input_filter: "float"
            padding: dp(20), dp(15)
        
        MDBoxLayout: 
            orientation: "horizontal"
            size_hint_y: None
            height: dp(48) 
            padding: 0, dp(10), 0, 0 
            Widget: 
                size_hint_x: 1
            
            MDRaisedButton: 
                text: "Save"
                md_bg_color: get_color_from_hex("#F89411")
                on_release: app.root.get_screen('dashboard').save_transaction_action(root.dialog_type, app.root.get_screen('dashboard').dialog)
                size_hint_x: 100
                size_hint_y: 0
                height: dp(48) 

<DashboardScreen>:
    name: 'dashboard'
    MDBoxLayout:
        orientation: 'horizontal'

        MDBoxLayout:
            id: nav_drawer_panel
            orientation: "vertical"
            #padding: dp(10)
            spacing: dp(15)
            size_hint_x: None
            width: dp(230)
            md_bg_color: get_color_from_hex("#000000")
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
                size_hint_x: 1
                height: dp(40)
                on_release: root.on_nav_item_press()
                md_bg_color: 1, 1, 1, 1
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
                halign: "center"
                padding: 0, 0
            MDFlatButton:
                text: "Analytics"
                size_hint_y: None
                height: dp(40)
                on_release: root.go_to_analytics()
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
                text: "Transaction"
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
                on_release: root.on_nav_item_press()
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0
            MDBoxLayout: 

        MDRelativeLayout:
            id: content_area_root
            md_bg_color: get_color_from_hex("#FAFAFA")

            MDBoxLayout:
                orientation: 'vertical'
                size_hint: (1,1)

                MDLabel:
                    id: dashboard_main_title
                    text: "DASHBOARD"
                    font_style: "H4"
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(60)
                    padding: dp(20), dp(10)

                MDBoxLayout:
                    id: dashboard_inner_scroll_content
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(20)
                    #adaptive_height: True
                    size_hint_y: 1

                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(15)
                        size_hint_y: None
                        height: dp(120)
                        MDCard:
                            id: income_card
                            orientation: "vertical"
                            padding: dp(15)
                            spacing: dp(5)
                            size_hint: (1, None)
                            height: dp(100)
                            elevation: 1
                            radius: [15, 15, 15, 15]
                            MDLabel:
                                text: "Total Income"
                                halign: "center"
                                theme_text_color: "Secondary"
                            MDLabel:
                                id: income_amount_label
                                text: "0.00"
                                font_style: "H5"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#4CAF50")
                        MDCard:
                            id: expense_card
                            orientation: "vertical"
                            padding: dp(15)
                            spacing: dp(5)
                            size_hint: (1, None)
                            height: dp(100)
                            elevation: 1
                            radius: [15, 15, 15, 15]
                            MDLabel:
                                text: "Total Expense"
                                halign: "center"
                                theme_text_color: "Secondary"
                            MDLabel:
                                id: expense_amount_label
                                text: "0.00"
                                font_style: "H5"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#F44336")
                        MDCard:
                            id: remaining_card
                            orientation: "vertical"
                            padding: dp(15)
                            spacing: dp(5)
                            size_hint: (1, None)
                            height: dp(100)
                            elevation: 1
                            radius: [15, 15, 15, 15]
                            MDLabel:
                                text: "Remaining"
                                halign: "center"
                                theme_text_color: "Secondary"
                            MDLabel:
                                id: remaining_amount_label
                                text: "0.00"
                                font_style: "H5"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#000000")

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(10)
                        size_hint_y: 1
                        #adaptive_height: True
                        elevation: 1
                        radius: [15, 15, 15, 15]
                        MDLabel:
                            text: "Recent Transactions"
                            font_style: "H6"
                            adaptive_height: True
                        MDLabel:
                            text: "All your transactions are recorded"
                            theme_text_color: "Hint"
                            adaptive_height: True
                        MDBoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
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
                            id: transactions_rv
                            viewclass: 'TransactionRow'
                            scroll_type: ['bars', 'content']
                            bar_width: dp(10)
                            size_hint_y: 1

                            RecycleBoxLayout:
                                default_size: None, dp(40)
                                default_size_hint: 1, None
                                size_hint_y: None
                                height: self.minimum_height
                                orientation: 'vertical'

            MDFloatingActionButton:
                id: add_fab
                icon: "plus"
                md_bg_color: get_color_from_hex("#F89411")
                pos_hint: {'right': 0.95, 'y': 0.05}
                on_release: root.show_add_options()
                elevation: 0

            MDRaisedButton:
                id: add_income_btn
                text: "Add Income"
                md_bg_color: get_color_from_hex("#F89411")
                pos_hint: {'right': 0.95, 'y': 0.15}
                opacity: 0
                disabled: True
                on_release: root.open_add_income_dialog()
                size_hint: None, None
                size: dp(150), dp(40)

            MDRaisedButton:
                id: add_expense_btn
                text: "Add Expense"
                md_bg_color: get_color_from_hex("#F89411")
                pos_hint: {'right': 0.95, 'y': 0.23}
                opacity: 0
                disabled: True
                on_release: root.open_add_expense_dialog()
                size_hint: None, None
                size: dp(150), dp(40)
"""

class DialogContent(MDBoxLayout):
    dialog_title = StringProperty()
    dialog_type = StringProperty() 

    def __init__(self, dialog_title, dialog_type, **kwargs): 
        super().__init__(**kwargs)
        self.dialog_title = dialog_title 
        self.dialog_type = dialog_type 

    def get_data(self):
        return {
            "category": self.ids.category_field.text,
            "date": self.ids.date_field.text,
            "account": self.ids.account_field.text,
            "note": self.ids.note_field.text,
            "amount": self.ids.amount_field.text,
        }

    def clear_fields(self):
        self.ids.category_field.text = ""
        self.ids.date_field.text = ""
        self.ids.account_field.text = ""
        self.ids.note_field.text = ""
        self.ids.amount_field.text = ""

        self.ids.amount_field.error = False
        self.ids.amount_field.helper_text = ""

        self.ids.date_field.error = False
        self.ids.date_field.helper_text = ""
class TransactionRow(MDBoxLayout):
    transaction = DictProperty({})
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(40)
        self.padding = [dp(10), 0, dp(10), 0]
        self.bind(transaction=self.update_row)
    
    def update_row(self, instance, value):
        self.clear_widgets()
        txn = self.transaction

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

        category_label = create_label(txn.get('category', ''), size_hint_x=1.2)
        date_label = create_label(txn.get('date', ''), size_hint_x=1)
        account_label = create_label(txn.get('account', ''), size_hint_x=1)
        note_label = create_label(txn.get('note', ''), size_hint_x=1.5)
        amount_color = (0, 0.5, 0, 1) if txn.get('type') == 'income' else (1, 0, 0, 1)
        amount_label = create_label(f"{abs(txn.get('amount', 0)):.2f}", color=amount_color, size_hint_x=0.8)

        self.add_widget(category_label)
        self.add_widget(date_label)
        self.add_widget(account_label)
        self.add_widget(note_label)
        self.add_widget(amount_label)
class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.dialog = None 

        self.bind(on_kv_post_build=self.get_transactions_async)
    
    def on_pre_enter(self, *args):
        self.reset_ui_if_new_month()
        self.get_transactions_async()
    
    def reset_ui_if_new_month(self):
        store = JsonStore("dashboard_ui_state.json")
        current_month = datetime.now().strftime("%Y-%m")

        if not store.exists("last_reset") or store.get("last_reset")["month"] != current_month:
            # Clear only the UI
            self.ids.income_amount_label.text = "0.00"
            self.ids.expense_amount_label.text = "0.00"
            self.ids.remaining_amount_label.text = "0.00"
            self.ids.transactions_rv.data = []

            # Update reset marker
            store.put("last_reset", month=current_month)
    
    def get_transactions_async(self):
        def fetch():
            with DatabaseManager("finance.db") as db:
                txns = TransactionManager.get_all_transactions(db)
                mapped_txns = [txn_tuple_to_dict(txn) for txn in txns]
                Clock.schedule_once(lambda dt: self.populate_transactions(mapped_txns))
                Clock.schedule_once(lambda dt: self.update_summary_labels(mapped_txns))
        Thread(target=fetch).start()
    
    def update_summary_labels(self, transactions):
        total_income = sum(t['amount'] for t in transactions if t['type'].lower() == 'income')
        total_expense = sum(t['amount'] for t in transactions if t['type'].lower() == 'expense')
        remaining = total_income - total_expense

        self.ids.income_amount_label.text = f"{total_income:,.2f}"
        self.ids.expense_amount_label.text = f"{total_expense:,.2f}"
        self.ids.remaining_amount_label.text = f"{remaining:,.2f}"
        self.ids.remaining_amount_label.text_color = get_color_from_hex("#4CAF50") if remaining >= 0 else get_color_from_hex("#F44336")

    def get_transactions_from_db(self):
        with DatabaseManager("finance.db") as db:
            txns = TransactionManager.get_all_transactions(db)
            return [txn_tuple_to_dict(txn) for txn in txns]

    def update_dashboard(self, *args):
        transactions = self.get_transactions_from_db()
        total_income = sum(t['amount'] for t in transactions if t['type'].lower() == 'income')
        total_expense = sum(t['amount'] for t in transactions if t['type'].lower() == 'expense')
        remaining = total_income - total_expense

        self.ids.income_amount_label.text = f"{total_income:,.2f}"
        self.ids.expense_amount_label.text = f"{total_expense:,.2f}"
        self.ids.remaining_amount_label.text = f"{remaining:,.2f}"
        self.ids.remaining_amount_label.text_color = get_color_from_hex("#4CAF50") if remaining >= 0 else get_color_from_hex("#F44336")

        self.populate_transactions(transactions)

    def populate_transactions(self, transactions=None):
        if transactions is None:
            transactions = self.get_transactions_from_db()
        self.ids.transactions_rv.data = [{'transaction': txn} for txn in reversed(transactions)]

    def show_add_options(self):
        target_opacity = 1 if self.ids.add_income_btn.opacity == 0 else 0
        self.ids.add_income_btn.opacity = target_opacity
        self.ids.add_income_btn.disabled = not bool(target_opacity)
        self.ids.add_expense_btn.opacity = target_opacity
        self.ids.add_expense_btn.disabled = not bool(target_opacity)

    def hide_add_options(self):
        if self.ids.add_income_btn.opacity == 1:
            self.ids.add_income_btn.opacity = 0
            self.ids.add_income_btn.disabled = True
            self.ids.add_expense_btn.opacity = 0
            self.ids.add_expense_btn.disabled = True

    def on_nav_item_press(self):
        self.hide_add_options()

    def open_transaction_dialog(self, dialog_type):
        self.hide_add_options()
        is_income = dialog_type == "income"
        title = "Add Income" if is_income else "Add Expense"

        dialog_content_instance = DialogContent(dialog_title=title, dialog_type=dialog_type)

        self.dialog = MDDialog(
            type="custom",
            content_cls=dialog_content_instance,
            padding=0,
            md_bg_color = (0, 0, 0, 0),
            elevation = 0
        )

        dialog_content_instance.clear_fields()
        self.dialog.open()

    def dismiss_current_dialog(self):
        if self.dialog:
            self.dialog.dismiss()

    def open_add_income_dialog(self):
        self.open_transaction_dialog("income")

    def open_add_expense_dialog(self):
        self.open_transaction_dialog("expense")

    def save_transaction_action(self, transaction_type, dialog_instance):
        data = dialog_instance.content_cls.get_data()
        content = dialog_instance.content_cls

        # Reset errors
        content.ids.amount_field.error = False
        content.ids.amount_field.helper_text = ""
        content.ids.date_field.error = False
        content.ids.date_field.helper_text = ""

        try:
            amount_val = float(data['amount'])
            if not all([data['category'], data['date'], data['account']]) or amount_val <= 0:
                content.ids.amount_field.error = True
                content.ids.amount_field.helper_text = "Category, Date, Account must be filled. Amount must be > 0."
                return
        except ValueError:
            content.ids.amount_field.error = True
            content.ids.amount_field.helper_text = "Enter a valid number for amount."
            return

        # Validate date format
        try:
            datetime.strptime(data['date'], "%Y-%m-%d")
        except ValueError:
            content.ids.date_field.error = True
            content.ids.date_field.helper_text = "Invalid format. Use YYYY-MM-DD."
            return

        txn = Transaction(
            data['date'],
            amount_val,
            data['category'],
            data['account'],
            data['note'],
            transaction_type
        )

        with DatabaseManager("finance.db") as db:
            TransactionManager.add_transaction(db, txn)

        App.get_running_app().root.get_screen('transactions').data_dirty = True
        self.get_transactions_async()
        dialog_instance.dismiss()

    def go_to_analytics(self):
        self.manager.current = 'analytics'