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
from kivymd.uix.toolbar import MDTopAppBar
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

transactions_data = [
    {"category": "Allowance", "date": "05/09/2025", "account": "Cash", "note": "Galing kay papa", "amount": 1000.00, "type": "income"},
    {"category": "Food", "date": "05/12/2025", "account": "Cash", "note": "Chowking", "amount": 100.00, "type": "expense"}
]

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
            pos_hint: {'center_y': .5} 
            on_release: app.root.dismiss_current_dialog() 

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
                on_release: app.root.save_transaction_action(root.dialog_type, app.root.dialog)
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
            padding: dp(10)
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
                height: dp(40)
                on_release: root.on_nav_item_press()
                theme_text_color: "Custom"
                text_color: 0.9, 0.9, 0.9, 1
                halign: "left"
                padding: dp(15), 0
            MDFlatButton:
                text: "Analytics"
                size_hint_y: None
                height: dp(40)
                on_release: root.on_nav_item_press()
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
                on_release: root.on_nav_item_press()
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

                ScrollView:
                    size_hint_y: 1
                    MDBoxLayout:
                        id: dashboard_inner_scroll_content
                        orientation: 'vertical'
                        padding: dp(20)
                        spacing: dp(20)
                        adaptive_height: True
                        size_hint_y: None
                        width: self.parent.width

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(15)
                            adaptive_height: True
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
                            size_hint_y: None
                            adaptive_height: True
                            elevation: 1
                            radius: [15, 15, 15, 15]
                            size_hint_x: 1
                            MDLabel:
                                text: "Recent Transactions"
                                font_style: "H6"
                                adaptive_height: True
                            MDLabel:
                                text: "All your transactions are recorded"
                                theme_text_color: "Hint"
                                adaptive_height: True
                            MDBoxLayout:
                                id: transactions_table_container
                                adaptive_height: True
                                size_hint_y: None
                                size_hint_x: 1
                                height: self.minimum_height
                                padding: 0, dp(10), 0, 0

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

class DashboardScreen(MDScreen):
    dialog = ObjectProperty(None, allownone=True) 
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.bind(on_kv_post_build=self.on_dashboard_screen_post_build)

    def on_dashboard_screen_post_build(self, *args):
        self.update_dashboard()
        Clock.schedule_once(lambda dt: self.ids.transactions_table_container.bind(width=self.on_table_container_width_changed))

    def on_table_container_width_changed(self, instance, value):
        Clock.schedule_once(lambda dt: self.populate_transactions_table())

    def update_dashboard(self, *args):
        total_income = sum(t['amount'] for t in transactions_data if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in transactions_data if t['type'] == 'expense')
        remaining = total_income - total_expense

        self.ids.income_amount_label.text = f"₱{total_income:,.2f}"
        self.ids.expense_amount_label.text = f"₱{total_expense:,.2f}"
        self.ids.remaining_amount_label.text = f"₱{remaining:,.2f}"
        self.ids.remaining_amount_label.text_color = get_color_from_hex("#4CAF50") if remaining >= 0 else get_color_from_hex("#F44336")
        self.populate_transactions_table()

    def populate_transactions_table(self):
        container = self.ids.transactions_table_container
        container.clear_widgets()
        row_data = [(t['category'], t['date'], t['account'], t['note'], f"₱{t['amount']:,.2f}") for t in reversed(transactions_data)]

        if row_data:
            num_rows = len(row_data)
            table_header_height = dp(56)
            row_height = dp(48)
            table_height = table_header_height + (num_rows * row_height)
            table_width_available = container.width
            column_weights = [0.1, 0.1, 0.1, 0.1, 0.1]

            col_category_width = table_width_available * column_weights[0]
            col_date_width = table_width_available * column_weights[1]
            col_account_width = table_width_available * column_weights[1]
            col_note_width = table_width_available * column_weights[1]
            col_amount_width = table_width_available * column_weights[1]

            min_dp_width_per_col = dp(10) 
            col_category_width = max(col_category_width, min_dp_width_per_col)
            col_date_width = max(col_date_width, min_dp_width_per_col)
            col_account_width = max(col_account_width, min_dp_width_per_col)
            col_note_width = max(col_note_width, min_dp_width_per_col)
            col_amount_width = max(col_amount_width, min_dp_width_per_col)

            column_data = [
                ("Category", col_category_width),
                ("Date", col_date_width),
                ("Account", col_account_width),
                ("Note", col_note_width),
                ("Amount", col_amount_width, None, "right")
            ]
            data_table = MDDataTable(
                size_hint=(1, None), 
                height=table_height,
                use_pagination=False,
                column_data=column_data, 
                row_data=row_data, 
                elevation=0,
            )
            container.bind(width=data_table.setter('width'))
            container.add_widget(data_table)
        else: 
            container.height = dp(100)
            container.add_widget(
                MDLabel(text="No transactions yet.", halign="center", theme_text_color="Hint", padding=(0, dp(20)))
            )

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

    def _open_transaction_dialog(self, dialog_type):
        self.hide_add_options()
        is_income = dialog_type == "income"
        title = "Add Income" if is_income else "Add Expense"

        dialog_content_instance = DialogContent(dialog_title=title, dialog_type=dialog_type)

        self.dialog = MDDialog(
            type="custom",
            content_cls=dialog_content_instance,
            padding=0, 
            radius=[0, 0, 0, 0], 
            md_bg_color = (0, 0, 0, 0),
            elevation = 0
        )

        dialog_content_instance.clear_fields()
        self.dialog.open()

    def dismiss_current_dialog(self):
        if self.dialog:
            self.dialog.dismiss()

    def open_add_income_dialog(self):
        self._open_transaction_dialog("income")

    def open_add_expense_dialog(self):
        self._open_transaction_dialog("expense")

    def save_transaction_action(self, transaction_type, dialog_instance):
        data = dialog_instance.content_cls.get_data()

        dialog_instance.content_cls.ids.amount_field.error = False
        dialog_instance.content_cls.ids.amount_field.helper_text = ""
        dialog_instance.content_cls.ids.category_field.error = False
        dialog_instance.content_cls.ids.date_field.error = False
        dialog_instance.content_cls.ids.account_field.error = False


        try:
            amount_val = float(data['amount'])
            missing_fields = []
            if not data['category']:
                missing_fields.append("Category")
                dialog_instance.content_cls.ids.category_field.error = True
            if not data['date']:
                missing_fields.append("Date")
                dialog_instance.content_cls.ids.date_field.error = True
            if not data['account']:
                missing_fields.append("Account")
                dialog_instance.content_cls.ids.account_field.error = True
            if amount_val <= 0:
                missing_fields.append("Amount (> 0)")
                dialog_instance.content_cls.ids.amount_field.error = True
            if missing_fields:
                error_msg = f"Please fill: {', '.join(missing_fields)}."
                dialog_instance.content_cls.ids.amount_field.helper_text = error_msg
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

class FinanceApp(MDApp):
    def build(self):
        Window.size = (1000, 600)
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.theme_style = "Light"
        Builder.load_string(kv_string) 
        return DashboardScreen()

if __name__ == '__main__':
    FinanceApp().run()
