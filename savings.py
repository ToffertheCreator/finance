from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from datetime import datetime
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from datetime import datetime
from kivy.clock import Clock
from backend import DatabaseManager, SavingsManager


KV = '''
ScreenManager:
    SavingsScreen:
        name: "savings"

<ChartCard@MDCard>:
    size_hint: None, None
    size: dp(130), dp(150)
    padding: dp(12)
    orientation: 'vertical'
    md_bg_color: 1, 1, 1, 1
    radius: [dp(12),]
    elevation: 1
    on_release: app.root.get_screen('savings').show_update_dialog(root)

    MDLabel:
        id: percent
        text: "0%"
        font_style: "H4"
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Primary"

    MDLabel:
        id: label
        text: root.label_text
        font_style: "Button"
        halign: "center"
        shorten: True
        shorten_from: "right"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Primary"

    MDLabel:
        id: figures
        text: f"{int(root.current_value)}/{int(root.target_value)}"
        font_style: "Caption"
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Secondary"
    
    MDLabel:
        id: days_left
        text: ""
        font_style: "Caption"
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1

    MDLabel:
        id: target_date
        text: ""
        font_style: "Caption"
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Custom"
        text_color: 0.2, 0.2, 0.2, 1

<AddSavingsContent@MDBoxLayout>:
    orientation: 'vertical'
    spacing: dp(0)
    padding: 0
    size_hint_y: None
    adaptive_height: True
    width: dp(500)

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: dp(48)
        md_bg_color: get_color_from_hex("#000000")
        padding: dp(20), 0, dp(10), 0

        MDLabel:
            text: "Add New Saving"
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
            on_release: app.root.get_screen('savings').safe_dismiss()

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#FFFFFF")
        spacing: dp(12)
        padding: dp(24)
        adaptive_height: True

        MDTextField:
            id: name_input
            hint_text: "Enter name"
            mode: "rectangle"
            size_hint_y: None
            height: dp(48)

        MDTextField:
            id: date_input
            hint_text: "Enter target date (YYYY-MM-DD)"
            mode: "rectangle"
            size_hint_y: None
            height: dp(48)
            helper_text: ""
            helper_text_mode: "on_error"
            error: False

        MDTextField:
            id: target_input
            hint_text: "Enter target amount"
            mode: "rectangle"
            size_hint_y: None
            height: dp(48)
            input_filter: 'float'

        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(48)
            padding: 0, dp(10), 0, 0
            Widget:
                size_hint_x: 1

            MDRaisedButton:
                text: "SAVE"
                md_bg_color: get_color_from_hex("#F89411")
                on_release: app.root.get_screen('savings').save_savings(root)
                size_hint_x: None
                width: dp(100)
                height: dp(48)

            MDFlatButton:
                text: "CANCEL"
                on_release: app.root.get_screen('savings').safe_dismiss()
                size_hint_x: None
                width: dp(100)
                height: dp(48)

<EditCardContent@MDBoxLayout>:
    orientation: "vertical"
    padding: 0
    size_hint_y: None
    width: dp(320)   # Match dashboard.py
    adaptive_height: True

    MDBoxLayout:
        orientation: "horizontal"
        size_hint: (1, None)
        height: dp(40)
        md_bg_color: get_color_from_hex("#000000")
        padding: dp(20), 0, dp(10), 0

        MDLabel:
            text: "Edit Saving"
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
            on_release: app.root.get_screen('savings').safe_dismiss()

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#FFFFFF")
        spacing: dp(15)
        padding: dp(24)
        adaptive_height: True

        MDTextField:
            id: name_input
            hint_text: "Name"
            mode: "rectangle"
            size_hint_y: None
            height: dp(48)

        MDTextField:
            id: value_input
            hint_text: "Add Amount"
            mode: "rectangle"
            size_hint_y: None
            height: dp(48)
            input_filter: 'float'

        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(48)
            padding: 0, dp(10), 0, 0
            Widget:
                size_hint_x: 1

            MDRaisedButton:
                text: "UPDATE"
                md_bg_color: get_color_from_hex("#F89411")
                on_release: app.root.get_screen('savings').update_card(root.root_card, root)
                size_hint_x: None
                width: dp(100)
                height: dp(48)
            
            MDFlatButton:
                text: "DELETE"
                text_color: 1, 0, 0, 1
                on_release: app.root.get_screen('savings').delete_card(root.root_card)
                size_hint_x: None
                width: dp(100)
                height: dp(48)

<Sidebar@MDBoxLayout>:
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
        size_hint_x: 1
        height: dp(40)
        theme_text_color: "Custom"
        md_bg_color: 1, 1, 1, 1
        text_color: 0, 0, 0, 1
        halign: "center"
        padding: 0, 0
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
        theme_text_color: "Custom"
        text_color: 0.9, 0.9, 0.9, 1
        halign: "left"
        padding: dp(15), 0
    MDBoxLayout: 

<SavingsScreen>:
    MDBoxLayout:
        orientation: 'horizontal'

        Sidebar:
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(16)
            spacing: dp(16)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: dp(56)
                padding: [0, dp(16), 0, 0]
                spacing: dp(8)

                MDLabel:
                    text: "SAVINGS"
                    font_style: "H4"
                    bold: True
                    halign: "left"
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(10)
                    valign: "middle"

                Widget:  # pushes the button to the right

                MDRaisedButton:
                    id: add_savings_btn
                    text: "Add Savings"
                    md_bg_color: get_color_from_hex("#F89411")
                    text_color: 1, 1, 1, 1
                    size_hint: None, None
                    size: dp(120), dp(36)
                    on_release: root.show_popup()

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(16)
                size_hint_y: 1

                MDCard:
                    size_hint_y: 1
                    padding: dp(16)
                    radius: [dp(12),]
                    elevation: 1
                    orientation: "vertical"
                    MDLabel:
                        text: "Your Savings"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: self.texture_size[1]
                    ScrollView:
                        bar_width: 5
                        scroll_type: ['bars', 'content']
                        do_scroll_y: True
                        do_scroll_x: False

                        GridLayout:
                            id: chart_area
                            cols: 1
                            row_default_height: dp(160)
                            row_force_default: True
                            spacing: dp(16)
                            padding: dp(8)
                            size_hint_y: None
                            height: self.minimum_height

                MDCard:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: 1
                    elevation: 1
                    radius: [15, 15, 15, 15]
                    MDLabel:
                        text: "History"
                        font_style: "H6"
                        adaptive_height: True
                    MDLabel:
                        text: "All your savings history"
                        theme_text_color: "Hint"
                        adaptive_height: True

                    MDBoxLayout:
                        orientation: "horizontal"
                        size_hint_y: None
                        height: dp(40)
                        padding: (dp(10), 0)
                        MDLabel:
                            text: "Name"
                            halign: "left"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0, 0, 0, 1
                            size_hint_x: 0.35
                        MDLabel:
                            text: "Date"
                            halign: "left"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0, 0, 0, 1
                            size_hint_x: 0.38
                        MDLabel:
                            text: "Amount"
                            halign: "left"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0, 0, 0, 1
                            size_hint_x: 0.38
                        MDLabel:
                            text: "Action"
                            halign: "left"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0, 0, 0, 1
                            size_hint_x: None
                    ScrollView:
                        size_hint_y: 1
                        MDBoxLayout:
                            id: history_container
                            orientation: "vertical"
                            adaptive_height: True
                            size_hint_x: 1
                            size_hint_y: None
'''

class ChartCard(MDCard):
    label_text = StringProperty("")
    current_value = NumericProperty(0)
    target_value = NumericProperty(1)
    target_date = StringProperty("")

    def update_display(self):
        percent = int((self.current_value / self.target_value) * 100) if self.target_value else 0
        self.ids.percent.text = f"{percent}%"
        self.ids.label.text = self.label_text
        self.ids.figures.text = f"{int(self.current_value)}/{int(self.target_value)}"
        try:
            target = datetime.strptime(self.target_date, "%Y-%m-%d")
            today = datetime.now()
            days_left = (target - today).days
            if percent >= 100:
                self.ids.days_left.text = "Complete"
                self.ids.days_left.text_color = (0, 0.6, 0, 1)
            elif days_left < 0:
                self.ids.days_left.text = f"Overdue by {-days_left} days"
                self.ids.days_left.text_color = (1, 0, 0, 1)
            else:
                self.ids.days_left.text = f"{days_left} days left"
                self.ids.days_left.text_color = (0, 0.5, 0, 1)
            self.ids.target_date.text = f"Target: {self.target_date}"
        except Exception:
            self.ids.days_left.text = ""
            self.ids.target_date.text = ""

class AddSavingsContent(MDBoxLayout):
    pass

class EditCardContent(MDBoxLayout):
    root_card = ObjectProperty(None)

class SavingsScreen(MDScreen):
    dialog = None
    _loading_event = None  # To prevent duplicates

    def on_pre_enter(self, *args):
        Window.bind(on_resize=self.update_chart_cols)
        Clock.schedule_once(self.update_chart_cols, 0)
        # Delay loading savings data until screen is built
        if not self._loading_event:
            self._loading_event = Clock.schedule_interval(self._safe_load_existing_savings, 0.1)

    def _safe_load_existing_savings(self, dt):
        if "chart_area" in self.ids:
            self._loading_event.cancel()
            self._loading_event = None
            self.load_existing_savings()
            return True  # stop the interval
        return False  # keep waiting


    def safe_dismiss(self):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def show_popup(self):
        self.safe_dismiss()
        content = AddSavingsContent()
        self.dialog = MDDialog(
            type="custom",
            content_cls=content,
            md_bg_color=(0, 0, 0, 0),
            elevation=0,
            padding=0,
            auto_dismiss=False
        )
        self.dialog.open()
    
    def sort_chart_cards(self):
        chart_area = self.ids.chart_area
        cards = list(chart_area.children)
        from datetime import datetime
        def get_date(card):
            try:
                return datetime.strptime(card.target_date, "%Y-%m-%d")
            except Exception:
                return datetime.max
        cards.sort(key=get_date)
        chart_area.clear_widgets()
        for card in cards:
            chart_area.add_widget(card)

    def save_savings(self, content):
        name = content.ids.name_input.text.strip()
        date = content.ids.date_input.text.strip()
        target = content.ids.target_input.text.strip()

        # Reset date input error state
        content.ids.date_input.error = False
        content.ids.date_input.helper_text = ""

        if not name or not date or not target:
            print("Please fill all fields")
            return

        # Validate date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            content.ids.date_input.error = True
            content.ids.date_input.helper_text = "Invalid date format. Use YYYY-MM-DD."
            return

        # Validate target amount
        try:
            target = float(target)
        except ValueError:
            print("Invalid target amount")
            return

        # Save to database
        with DatabaseManager("finance.db") as db:
            SavingsManager.set_savings_goal(db, name, target, date)

        # UI update
        chart_card = ChartCard()
        chart_card.label_text = name
        chart_card.current_value = 0
        chart_card.target_value = target
        chart_card.target_date = date
        chart_card.update_display()

        self.ids.chart_area.add_widget(chart_card)
        self.sort_chart_cards()
        self.update_chart_cols()
        self.safe_dismiss()

    def show_update_dialog(self, card):
        self.safe_dismiss()
        content = EditCardContent()
        content.ids.name_input.text = card.label_text
        content.ids.value_input.text = ""
        content.root_card = card
        self.dialog = MDDialog(
            type="custom",
            content_cls=content,
            md_bg_color=(0, 0, 0, 0),  # Transparent like dashboard.py
            elevation=0,
            padding=0,
            auto_dismiss=False,
        )
        self.dialog.open()

    def update_card(self, card, content):
        try:
            card.label_text = content.ids.name_input.text.strip()
            add_amount_str = content.ids.value_input.text.strip()
            if add_amount_str:
                add_amount = float(add_amount_str)
                card.current_value += add_amount
                card.update_display()

                with DatabaseManager("finance.db") as db:
                    SavingsManager.add_savings(db, card.label_text, add_amount)

                # Add history log
                history_container = self.ids.history_container
                row = MDBoxLayout(size_hint_y=None, height=dp(32), padding=(dp(15), 0, 0, 0))
                row.add_widget(MDLabel(text=card.label_text, size_hint_x=0.35, halign="left"))
                row.add_widget(MDLabel(text=datetime.now().strftime("%Y-%m-%d"), size_hint_x=0.38, halign="left"))
                row.add_widget(MDLabel(text=str(add_amount), size_hint_x=0.38, halign="left",
                                    theme_text_color="Custom", text_color=(0, 1, 0, 1)))
                row.add_widget(MDLabel(text="added", size_hint_x=None, halign="left",
                                    theme_text_color="Custom", text_color=(0, 0.5, 0, 1)))
                history_container.add_widget(row)
                content.ids.value_input.text = ""
        except Exception as e:
            print("Error updating card:", e)
        self.safe_dismiss()

    
    def delete_card(self, card):
        name = card.label_text

        # 1. Remove from the database
        try:
            with DatabaseManager("finance.db") as db:
                SavingsManager.delete_savings(db, name)
        except Exception as e:
            print("Failed to delete from database:", e)

        # 2. Remove the chart card
        chart_area = self.ids.chart_area
        if card in chart_area.children:
            chart_area.remove_widget(card)

        # 3. Remove all related history entries
        history_container = self.ids.history_container
        to_remove = []
        for row in history_container.children[:]:
            if len(row.children) >= 3:
                name_label = row.children[-1]  # First label added is the last in .children
                if name_label.text == name:
                    to_remove.append(row)
        for row in to_remove:
            history_container.remove_widget(row)

        # 4. Dismiss dialog
        self.safe_dismiss()


    def update_chart_cols(self, *args):
        if "chart_area" not in self.ids:
            return  # Don't do anything if chart_area is not ready yet
        chart_area = self.ids.chart_area
        card_width = dp(130) + dp(16)
        available_width = Window.width - dp(220) - dp(48)
        cols = max(int(available_width // card_width), 1)
        chart_area.cols = cols

        rows = (len(chart_area.children) + cols - 1) // cols
        chart_area.height = rows * (dp(160) + dp(16))
    
    def load_existing_savings(self):
        chart_area = self.ids.get("chart_area")
        history_container = self.ids.get("history_container")
        
        if not chart_area or not history_container:
            print("chart_area or history_container not found yet")
            return

        chart_area.clear_widgets()
        history_container.clear_widgets()

        with DatabaseManager("finance.db") as db:
            # Step 1: Load all savings goals
            savings_rows = db.run_query("SELECT name, current_saved, target_amount, target_date FROM savings", fetch=True)
            if savings_rows:
                for name, current_saved, target_amount, target_date in savings_rows:
                    card = ChartCard()
                    card.label_text = name
                    card.current_value = current_saved
                    card.target_value = target_amount
                    card.target_date = target_date
                    card.update_display()
                    chart_area.add_widget(card)

                # Step 2: Load savings history
                history_rows = SavingsManager.get_savings_history(db)
                for name, date, amount, action in history_rows:
                    row = MDBoxLayout(size_hint_y=None, height=dp(32), padding=(dp(15), 0, 0, 0))
                    row.add_widget(MDLabel(text=name, size_hint_x=0.35, halign="left"))
                    row.add_widget(MDLabel(text=date, size_hint_x=0.38, halign="left"))
                    row.add_widget(MDLabel(text=str(amount), size_hint_x=0.38, halign="left",
                                        theme_text_color="Custom", text_color=(0, 1, 0, 1)))
                    row.add_widget(MDLabel(text=action, size_hint_x=None, halign="left",
                                        theme_text_color="Custom", text_color=(0, 0.5, 0, 1)))
                    history_container.add_widget(row)

        self.sort_chart_cards()
        self.update_chart_cols()