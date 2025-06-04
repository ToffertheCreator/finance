from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from datetime import datetime

KV = '''
ScreenManager:
    MainScreen:
        name: "main"

<Sidebar@MDBoxLayout>:
    orientation: 'vertical'
    size_hint: None, 1
    width: dp(220)
    md_bg_color: 0.08, 0.08, 0.08, 1
    padding: dp(16)
    spacing: dp(20)

    MDLabel:
        text: "FINANCE TRACKER"
        font_size: dp(20)
        bold: True
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        size_hint_y: None
        height: dp(40)
        halign: 'left'

    MDSeparator:
        height: dp(1)

    MDLabel:
        text: "Dashboard"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 0.7
        halign: 'left'
        size_hint_y: None
        height: dp(36)

    MDLabel:
        text: "Analytics"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 0.7
        halign: 'left'
        size_hint_y: None
        height: dp(36)

    MDBoxLayout:
        md_bg_color: 1, 1, 1, 1
        radius: [10]
        size_hint_y: None
        height: dp(36)
        padding: dp(10), 0

        MDLabel:
            text: "Savings"
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
            halign: 'left'
            valign: 'middle'

    MDLabel:
        text: "Transaction"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 0.7
        halign: 'left'
        size_hint_y: None
        height: dp(36)

<ChartCard>:
    size_hint: None, None
    size: dp(130), dp(150)
    padding: dp(12)
    orientation: 'vertical'
    md_bg_color: 1,1,1,0.05
    radius: [dp(12),]
    elevation: 2

    MDLabel:
        id: percent
        text: "0%"
        font_style: "H4"
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        id: label
        text: root.label_text
        font_style: "Button"
        halign: "center"
        shorten: True
        shorten_from: "right"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        id: figures
        text: f"{int(root.current_value)}/{int(root.target_value)}"
        font_style: "Caption"
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Secondary"

<HistoryTable@MDBoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    padding: 0, dp(8)
    spacing: dp(4)

    MDBoxLayout:
        size_hint_y: None
        height: dp(32)
        MDLabel:
            text: "Name"
            font_style: "Subtitle2"
            bold: True
        MDLabel:
            text: "Date"
            font_style: "Subtitle2"
            bold: True
        MDLabel:
            text: "Amount"
            font_style: "Subtitle2"
            bold: True
            halign: 'right'

    MDSeparator:
        height: dp(1)

<MainScreen>:
    MDBoxLayout:
        orientation: 'horizontal'

        Sidebar:

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(16)
            spacing: dp(16)
            canvas.before:
                Color:
                    rgba: 0.07, 0.07, 0.07, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDBoxLayout:
                size_hint_y: None
                height: dp(48)

                MDLabel:
                    text: "SAVINGS"
                    font_style: "H4"
                    bold: True

                MDFillRoundFlatButton:
                    text: "Add new savings ▼"
                    md_bg_color: 1, 0.6, 0, 1
                    text_color: 1, 1, 1, 1
                    size_hint: None, None
                    size: dp(160), dp(36)
                    on_release: app.show_popup()

            MDBoxLayout:
                id: chart_area
                size_hint_y: None
                height: dp(160)
                spacing: dp(16)

            MDLabel:
                text: "History"
                font_style: "H6"
                size_hint_y: None
                height: self.texture_size[1]

            MDScrollView:
                MDBoxLayout:
                    id: history_container
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height

                    HistoryTable:
'''

class ChartCard(MDCard):
    label_text = StringProperty()
    current_value = NumericProperty(0)
    target_value = NumericProperty(1)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            app = MDApp.get_running_app()
            app.show_edit_delete_menu(self)
            return True
        return super().on_touch_down(touch)

class MainScreen(Screen):
    pass

class AddSavingsContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(12), padding=dp(16), size_hint=(1, None), height=dp(300), **kwargs)
        self.name_input = MDTextField(hint_text="Enter name", mode="rectangle", size_hint_y=None, height=dp(48))
        self.date_input = MDTextField(hint_text="Enter date (YYYY-MM-DD)", mode="rectangle", size_hint_y=None, height=dp(48))
        self.value_input = MDTextField(hint_text="Enter value", mode="rectangle", size_hint_y=None, height=dp(48))
        self.target_input = MDTextField(hint_text="Enter target amount", mode="rectangle", size_hint_y=None, height=dp(48))
        for label, field in [("Name", self.name_input), ("Date", self.date_input), ("Value", self.value_input), ("Target", self.target_input)]:
            self.add_widget(MDLabel(text=label, font_style="Caption", theme_text_color="Secondary", size_hint_y=None, height=dp(16)))
            self.add_widget(field)

class EditCardContent(MDBoxLayout):
    def __init__(self, card, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(12), padding=dp(16), **kwargs)
        self.card = card
        self.name_input = MDTextField(text=card.label_text, hint_text="Edit name", mode="rectangle", size_hint_y=None, height=dp(48))
        self.value_input = MDTextField(text=str(card.current_value), hint_text="Edit value", mode="rectangle", size_hint_y=None, height=dp(48))
        self.target_input = MDTextField(text=str(card.target_value), hint_text="Edit target", mode="rectangle", size_hint_y=None, height=dp(48))
        for label, field in [("Name", self.name_input), ("Value", self.value_input), ("Target", self.target_input)]:
            self.add_widget(MDLabel(text=label, font_style="Caption", theme_text_color="Secondary", size_hint_y=None, height=dp(16)))
            self.add_widget(field)

class FinanceTrackerApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def safe_dismiss(self):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def show_popup(self):
        content = AddSavingsContent()
        self.dialog = MDDialog(
            title="Add New Savings",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=dp(400),
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.safe_dismiss()),
                MDRaisedButton(text="SAVE", on_release=lambda x: self.save_savings(content)),
            ],
            auto_dismiss=False
        )
        self.dialog.open()

    def save_savings(self, content):
        name = content.name_input.text.strip()
        date = content.date_input.text.strip()
        value = content.value_input.text.strip()
        target = content.target_input.text.strip()

        if not name or not date or not value or not target:
            print("Please fill all fields")
            return

        try:
            value_num = float(value)
            target_num = float(target)
        except ValueError:
            print("Value and Target must be numbers")
            return

        card = ChartCard(label_text=name, current_value=value_num, target_value=target_num)
        percent = int((value_num / target_num) * 100)
        card.ids.percent.text = f"{percent}%"
        card.ids.figures.text = f"{int(value_num)}/{int(target_num)}"

        chart_area = self.root.get_screen("main").ids.chart_area
        chart_area.add_widget(card)

        self.add_history(name, date, value_num)
        self.safe_dismiss()

    def show_edit_delete_menu(self, card):
        content = EditCardContent(card)
        self.dialog = MDDialog(
            title=f"Edit {card.label_text}",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=dp(320),
            buttons=[
                MDFlatButton(text="DELETE", text_color=(1, 0, 0, 1), on_release=lambda x: self.delete_card(card)),
                MDFlatButton(text="CANCEL", on_release=lambda x: self.safe_dismiss()),
                MDRaisedButton(text="SAVE", on_release=lambda x: self.save_card_edit(content)),
            ],
            auto_dismiss=False
        )
        self.dialog.open()

    def save_card_edit(self, content):
        try:
            name = content.name_input.text.strip()
            value = float(content.value_input.text.strip())
            target = float(content.target_input.text.strip())
        except ValueError:
            print("Invalid input")
            return

        card = content.card
        card.label_text = name
        card.current_value = value
        card.target_value = target
        card.ids.label.text = name
        card.ids.percent.text = f"{int((value / target) * 100)}%"
        card.ids.figures.text = f"{int(value)}/{int(target)}"

        self.safe_dismiss()

    def delete_card(self, card):
        self.root.get_screen("main").ids.chart_area.remove_widget(card)
        self.safe_dismiss()

    def add_history(self, name, date, amount):
        container = self.root.get_screen("main").ids.history_container
        row = MDBoxLayout(size_hint_y=None, height=dp(28))
        row.add_widget(MDLabel(text=name, font_style="Body2", shorten=True))
        row.add_widget(MDLabel(text=date, font_style="Body2"))
        row.add_widget(MDLabel(text=f"[color=00FF00]{amount}[/color]", markup=True, font_style="Body2", halign="right"))
        container.add_widget(row)
        container.height = container.minimum_height

if __name__ == "__main__":
    FinanceTrackerApp().run()
