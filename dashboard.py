from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty
from kivy.properties import StringProperty

transactions_data = []

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
            hint_text: "Date"
            mode: "rectangle"
            padding: dp(20), dp(15)
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
                on_release: root.go_to_analytics()  # Call the go_to_analytics method
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0
            MDFlatButton:
                text: "Savings"
                size_hint_y: None
                height: dp(40)
                on_release: root.on_nav_item_press()
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
                        ScrollView:
                            size_hint_y: 1
                            #height: dp(250)  # or any height you want
                            MDBoxLayout:
                                id: transactions_table_container
                                orientation: "vertical"
                                adaptive_height: True
                                size_hint_x: 1
                                size_hint_y: None

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
        amount_color = (0, 0.5, 0, 1) if transaction['type'] == 'income' else (1, 0, 0, 1)
        amount_label = create_label(f"{abs(transaction['amount']):.2f}", color=amount_color, size_hint_x=0.8)

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

        self.bind(on_kv_post_build=self.update_dashboard)

    def create_summary_card(self, title_text, amount, amount_color):
        pass

    def update_dashboard(self, *args):
        total_income = sum(t['amount'] for t in transactions_data if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in transactions_data if t['type'] == 'expense')
        remaining = total_income - total_expense

        self.ids.income_amount_label.text = f"{total_income:,.2f}"
        self.ids.expense_amount_label.text = f"{total_expense:,.2f}"
        self.ids.remaining_amount_label.text = f"{remaining:,.2f}"
        self.ids.remaining_amount_label.text_color = get_color_from_hex("#4CAF50") if remaining >= 0 else get_color_from_hex("#F44336")

        self.populate_transactions()

    def populate_transactions(self):
        self.ids.transactions_table_container.clear_widgets()
        for transaction in reversed(transactions_data):
            row = TransactionRow(transaction)
            self.ids.transactions_table_container.add_widget(row)

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

        dialog_instance.content_cls.ids.amount_field.error = False
        dialog_instance.content_cls.ids.amount_field.helper_text = ""

        try:
            amount_val = float(data['amount'])

            if not all([data['category'], data['date'], data['account']]) or amount_val <= 0:
                dialog_instance.content_cls.ids.amount_field.error = True
                dialog_instance.content_cls.ids.amount_field.helper_text = "Category, Date, Account must be filled. Amount must be > 0."
                return
        except ValueError:
            dialog_instance.content_cls.ids.amount_field.error = True
            dialog_instance.content_cls.ids.amount_field.helper_text = "Enter a valid number for amount."
            return

        transactions_data.append({
            "category": data['category'], "date": data['date'], "account": data['account'],
            "note": data['note'], "amount": amount_val, "type": transaction_type
        })
        self.update_dashboard()
        dialog_instance.dismiss()

    def go_to_analytics(self):
        self.manager.current = 'analytics'

# class FinanceApp(MDApp):
#     def build(self):
#         Window.size = (1000, 600)
#         self.theme_cls.primary_palette = "Orange"
#         self.theme_cls.accent_palette = "Orange"
#         self.theme_cls.theme_style = "Light"
#         Builder.load_string(kv_string) 
#         return DashboardScreen()

# if __name__ == '__main__':
#     FinanceApp().run()