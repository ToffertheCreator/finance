from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView


KV = '''
<Sidebar@MDBoxLayout>:
    orientation: 'vertical'
    size_hint_x: None
    width: dp(200)
    size_hint_y: None
    height: self.minimum_height
    padding: dp(16), dp(8), dp(16), dp(16)  # top padding reduced
    spacing: dp(12)
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    MDLabel:
        text: "Finance Tracker"
        font_style: "H5"
        size_hint_y: None
        height: self.texture_size[1]

    MDSeparator:
        height: dp(1)

    MDLabel:
        text: "Dashboard"
        font_style: "Subtitle1"
        size_hint_y: None
        height: self.texture_size[1]

    MDRaisedButton:
        text: "Dashboard"
        size_hint_y: None
        height: dp(40)

    MDRaisedButton:
        text: "Analytics"
        size_hint_y: None
        height: dp(40)

    MDRaisedButton:
        text: "Savings"
        size_hint_y: None
        height: dp(40)

    MDRaisedButton:
        text: "Transactions"
        size_hint_y: None
        height: dp(40)

    MDRaisedButton:
        text: "Settings"
        size_hint_y: None
        height: dp(40)

ScreenManager:
    MainScreen:
        name: "main"

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
        text: "10%"
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
        text: root.figures_text
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
        color: 1,1,1,0.1

<MainScreen>:
    MDBoxLayout:
        orientation: 'horizontal'

        AnchorLayout:
            anchor_x: 'left'
            anchor_y: 'top'
            size_hint_x: None
            width: dp(200)

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
                padding: 0, 0, dp(16), 0
                MDLabel:
                    text: "SAVINGS"
                    font_style: "H4"
                    bold: True
                    size_hint_x: 0.9
                    valign: 'middle'

                MDFillRoundFlatButton:
                    id: add_savings_btn
                    text: "Add new savings \u25BE"
                    md_bg_color: 1, 0.6, 0, 1
                    text_color: 1,1,1,1
                    size_hint: None, None
                    size: dp(160), dp(36)
                    pos_hint: {"center_y": 0.5}
                    on_release: app.show_popup()

            MDBoxLayout:
                id: chart_area
                size_hint_y: None
                height: dp(160)
                spacing: dp(16)
                padding: 0,0,0,dp(8)

                ChartCard:
                    label_text: "world domination fund"
                    figures_text: "1000/20000"

                ChartCard:
                    label_text: "vacation"
                    figures_text: "250/5000"

                ChartCard:
                    label_text: "car repair"
                    figures_text: "150/1000"

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
    label_text = StringProperty("")
    figures_text = StringProperty("")

class MainScreen(Screen):
    pass

class FinanceTrackerApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def show_popup(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.label import MDLabel

        content = BoxLayout(orientation='vertical', spacing=dp(12), padding=dp(16), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        self.name_input = MDTextField(hint_text="Enter name", mode="rectangle", size_hint_y=None, height=dp(40))
        self.date_input = MDTextField(hint_text="Enter date", mode="rectangle", size_hint_y=None, height=dp(40))
        self.value_input = MDTextField(hint_text="Enter value", mode="rectangle", size_hint_y=None, height=dp(40))
        self.target_input = MDTextField(hint_text="Enter target amount", mode="rectangle", size_hint_y=None, height=dp(40))

        for label, field in [("Name", self.name_input), ("Date", self.date_input), ("Value", self.value_input), ("Target Amount", self.target_input)]:
            content.add_widget(MDLabel(text=label, theme_text_color="Secondary", font_style="Caption", size_hint_y=None, height=dp(16)))
            content.add_widget(field)

        self.dialog = MDDialog(
            title="Add New Savings",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="SAVE", on_release=lambda x: self.save_savings())
            ]
        )
        self.dialog.open()

    def save_savings(self):
        name = self.name_input.text.strip()
        date = self.date_input.text.strip()
        value = self.value_input.text.strip()
        target = self.target_input.text.strip()

        if not name or not date or not value or not target:
            print("Please fill in all required fields (Name, Date, Value, Target).")
            return

        try:
            value_num = float(value)
            target_num = float(target)
        except ValueError:
            print("Value and Target must be numbers.")
            return

        percent = int((value_num / target_num) * 100) if target_num != 0 else 0

        main_screen = self.root.get_screen("main")
        history_container = main_screen.ids.history_container

        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel

        # Add new row to history table
        new_row = MDBoxLayout(size_hint_y=None, height=dp(28))
        name_label = MDLabel(text=name, font_style="Body2", shorten=True)
        date_label = MDLabel(text=date, font_style="Body2")
        value_label = MDLabel(text=f"[color=00FF00]{value}[/color]", markup=True, font_style="Body2", halign="right")

        new_row.add_widget(name_label)
        new_row.add_widget(date_label)
        new_row.add_widget(value_label)

        history_container.add_widget(new_row)
        history_container.height = history_container.minimum_height

        # Add new ChartCard dynamically
        chart_area = main_screen.ids.chart_area
        new_card = ChartCard()
        new_card.label_text = name
        new_card.figures_text = f"{value}/{target}"
        new_card.ids.percent.text = f"{percent}%"

        chart_area.add_widget(new_card)

        self.dialog.dismiss()
        self.dialog = None

if __name__ == "__main__":
    FinanceTrackerApp().run()
