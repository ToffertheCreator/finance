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

KV = '''
ScreenManager:
    SavingsScreen:
        name: "main"

<ChartCard@MDCard>:
    size_hint: None, None
    size: dp(130), dp(150)
    padding: dp(12)
    orientation: 'vertical'
    md_bg_color: 1, 1, 1, 1
    radius: [dp(12),]
    elevation: 1
    on_release: app.root.get_screen('main').show_update_dialog(root)

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
            on_release: app.root.get_screen('main').safe_dismiss()

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
                on_release: app.root.get_screen('main').save_savings(root)
                size_hint_x: None
                width: dp(100)
                height: dp(48)

            MDFlatButton:
                text: "CANCEL"
                on_release: app.root.get_screen('main').safe_dismiss()
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
            on_release: app.root.get_screen('main').safe_dismiss()

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
                on_release: app.root.get_screen('main').update_card(root.root_card, root)
                size_hint_x: None
                width: dp(100)
                height: dp(48)
            
            MDFlatButton:
                text: "DELETE"
                text_color: 1, 0, 0, 1
                on_release: app.root.get_screen('main').delete_card(root.root_card)
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

    # def on_touch_up(self, touch):
    #     if self.collide_point(*touch.pos):
    #         # Only respond to left mouse button or touch (not scroll)
    #         if hasattr(touch, "button") and touch.button != "left":
    #             return super().on_touch_up(touch)
    #         app = MDApp.get_running_app()
    #         if hasattr(app.root.get_screen("main"), "show_update_dialog"):
    #             app.root.get_screen("main").show_update_dialog(self)
    #         return True
    #     return super().on_touch_up(touch)

    def update_display(self):
        percent = int((self.current_value / self.target_value) * 100) if self.target_value else 0
        self.ids.percent.text = f"{percent}%"
        self.ids.label.text = self.label_text
        self.ids.figures.text = f"{int(self.current_value)}/{int(self.target_value)}"
        from datetime import datetime
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

    def on_pre_enter(self, *args):
        Window.bind(on_resize=self.update_chart_cols)
        from kivy.clock import Clock
        Clock.schedule_once(self.update_chart_cols, 0)

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

        if not name or not date or not target:
            print("Please fill all fields")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
            target = float(target)
        except ValueError:
            print("Invalid date or number")
            return

        chart_card = ChartCard()
        chart_card.label_text = name
        chart_card.current_value = 0  # Start at 0
        chart_card.target_value = target
        chart_card.target_date = date
        chart_card.update_display()

        chart_area = self.ids.chart_area
        chart_area.add_widget(chart_card)

        self.sort_chart_cards()
        self.update_chart_cols()

        # Add to history (optional, you may want to only add when value > 0)
        history_container = self.ids.history_container
        row = MDBoxLayout(size_hint_y=None, height=dp(32), padding=(dp(15), 0, 0, 0))
        row.add_widget(MDLabel(text=name, size_hint_x=0.35, halign="left"))
        row.add_widget(MDLabel(text=datetime.now().strftime("%Y-%m-%d"), size_hint_x=0.38, halign="left"))
        row.add_widget(MDLabel(
            text="0",
            size_hint_x=0.38,
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 1, 0, 1)
        ))
        row.add_widget(MDLabel(
            text="created",
            size_hint_x=None,
            halign="left",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1)
        ))
        history_container.add_widget(row)

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
                card.current_value += add_amount  # Add instead of replace
                card.update_display()
                # Log this addition in history
                history_container = self.ids.history_container
                from datetime import datetime
                row = MDBoxLayout(size_hint_y=None, height=dp(32), padding=(dp(15), 0, 0, 0))
                row.add_widget(MDLabel(text=card.label_text, size_hint_x=0.35, halign="left"))
                row.add_widget(MDLabel(text=datetime.now().strftime("%Y-%m-%d"), size_hint_x=0.38, halign="left"))
                row.add_widget(MDLabel(
                    text=str(add_amount),
                    size_hint_x=0.38,
                    halign="left",
                    theme_text_color="Custom",
                    text_color=(0, 1, 0, 1)
                ))
                row.add_widget(MDLabel(
                    text="added",
                    size_hint_x=None,
                    halign="left",
                    theme_text_color="Custom",
                    text_color=(0, 0.5, 0, 1)
                ))
                history_container.add_widget(row)
                content.ids.value_input.text = ""
        except Exception as e:
            print("Error updating card:", e)
        self.safe_dismiss()
    
    def delete_card(self, card):
        # Remove the card from the chart area
        chart_area = self.ids.chart_area
        if card in chart_area.children:
            chart_area.remove_widget(card)
        # Remove all history rows for this card
        history_container = self.ids.history_container
        name = card.label_text
        to_remove = []
        for row in history_container.children[:]:
            if len(row.children) >= 3:
                # Name label is the first added, so it's the last in children
                name_label = row.children[-1]
                if name_label.text == name:
                    to_remove.append(row)
        for row in to_remove:
            history_container.remove_widget(row)
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

class FinanceTrackerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

if __name__ == '__main__':
    FinanceTrackerApp().run()