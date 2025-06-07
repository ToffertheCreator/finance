from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from datetime import datetime
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

KV = '''
ScreenManager:
    MainScreen:
        name: "main"

<Sidebar@MDBoxLayout>:
    size_hint: None, 1
    width: dp(220)
    md_bg_color: get_color_from_hex("#1c1c1c")

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(16)
        
        size_hint: 1, None
        height: self.minimum_height
        pos_hint: {"top": 1}

        MDLabel:
            text: "FINANCE TRACKER"
            font_size: dp(20)
            bold: True
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            halign: 'left'
            valign: 'middle'
            size_hint_y: None
            height: dp(40)
            padding_x: dp(16) 

        MDLabel:
            text: "Dashboard"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 0.7
            halign: 'left'
            size_hint_y: None
            height: dp(36)
            padding_x: dp(16) 

        MDLabel:
            text: "Analytics"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 0.7
            halign: 'left'
            size_hint_y: None
            height: dp(36)
            padding_x: dp(16)  

        MDBoxLayout:
            size_hint_y: None
            height: dp(36)
            md_bg_color: 1, 1, 1, 1
            padding: 0

            MDLabel:
                text: "Savings"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
                halign: 'left'
                valign: 'middle'
                size_hint_x: 1  
                padding_x: dp(16)  

        MDLabel:
            text: "Transaction"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 0.7
            halign: 'left'
            size_hint_y: None
            height: dp(36)
            padding_x: dp(16)  

        MDLabel:
            text: "Settings"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 0.7
            halign: 'left'
            size_hint_y: None
            height: dp(36)
            padding_x: dp(16)  

<ChartCard@MDCard>:
    size_hint: None, None
    size: dp(130), dp(150)
    padding: dp(12)
    orientation: 'vertical'
    md_bg_color: 1, 1, 1, 1
    radius: [dp(12),]
    elevation: 2

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
            theme_text_color: "Custom"
            text_color: 0, 1, 0, 1

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
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: dp(100)
                padding: [0, dp(16), 0, 0]
                spacing: dp(0)
                
                

                MDLabel:
                    text: "SAVINGS"
                    font_style: "H4"
                    bold: True
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDBoxLayout:
                    size_hint_y: None
                    height: dp(36)
                    padding: 0, 0, dp(16), 0
                    spacing: dp(8)

                 

                    
                MDRaisedButton:
                    id: add_savings_btn
                    text: "Add Savings"
                    md_bg_color: get_color_from_hex("#F89411")
                    text_color: 1, 1, 1, 1
                    size_hint: None, None
                    size: dp(120), dp(36)
                    pos_hint: {"right": 1}
                    padding: dp(8), 0
                    on_release: app.show_popup()

            ScrollView:
                size_hint_y: None
                height: dp(160)
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
                size_hint_y: None
                height: dp(280)
                padding: dp(16)
                radius: [dp(12),]
                elevation: 4
                orientation: "vertical"

                MDLabel:
                    text: "History"
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDScrollView:
                    do_scroll_x: False
                    bar_width: dp(5)

                    MDBoxLayout:
                        id: history_container
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height

                        HistoryTable:
'''



class ChartCard(MDCard):
    label_text = StringProperty("")
    current_value = NumericProperty(0)
    target_value = NumericProperty(1)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            MDApp.get_running_app().show_update_dialog(self)
            return True
        return super().on_touch_up(touch)

    def update_display(self):
        percent = int((self.current_value / self.target_value) * 100) if self.target_value else 0
        self.ids.percent.text = f"{percent}%"
        self.ids.label.text = self.label_text
        self.ids.figures.text = f"{int(self.current_value)}/{int(self.target_value)}"


class MainScreen(Screen):
    pass


class AddSavingsContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(12), padding=dp(16), size_hint=(1, None), height=dp(400), **kwargs)
        self.name_input = MDTextField(hint_text="Enter name", mode="rectangle", size_hint_y=None, height=dp(48))
        self.date_input = MDTextField(hint_text="Enter date (YYYY-MM-DD)", mode="rectangle", size_hint_y=None, height=dp(48))
        self.value_input = MDTextField(hint_text="Enter value", mode="rectangle", size_hint_y=None, height=dp(48), input_filter='float')
        self.target_input = MDTextField(hint_text="Enter target amount", mode="rectangle", size_hint_y=None, height=dp(48), input_filter='float')
        for label, field in [("Name", self.name_input), ("Date", self.date_input), ("Value", self.value_input), ("Target", self.target_input)]:
            self.add_widget(MDLabel(text=label, font_style="Caption", theme_text_color="Secondary", size_hint_y=None, height=dp(16)))
            self.add_widget(field)


class EditCardContent(MDBoxLayout):
    def __init__(self, card, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(12), padding=dp(16), size_hint=(1, None), height=dp(220), **kwargs)
        self.name_input = MDTextField(text=card.label_text, hint_text="Name", mode="rectangle", size_hint_y=None, height=dp(48))
        self.value_input = MDTextField(text=str(card.current_value), hint_text="Current Value", mode="rectangle", size_hint_y=None, height=dp(48), input_filter='float')
        self.add_widget(self.name_input)
        self.add_widget(self.value_input)


class FinanceTrackerApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        root = Builder.load_string(KV)

        
        Window.bind(on_resize=self.update_chart_cols)

        
        from kivy.clock import Clock
        Clock.schedule_once(self.update_chart_cols, 0)

        return root

    def safe_dismiss(self):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def show_popup(self):
        self.safe_dismiss()
        content = AddSavingsContent()
        self.dialog = MDDialog(
            title="Add New Saving",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=dp(500),
            buttons=[
                MDRaisedButton(text="SAVE", on_release=lambda x: self.save_savings(content), md_bg_color=get_color_from_hex("#F89411"), text_color=(1,1,1,1)),
                MDFlatButton(text="CANCEL", on_release=lambda x: self.safe_dismiss())
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
            datetime.strptime(date, "%Y-%m-%d")
            value = float(value)
            target = float(target)
        except ValueError:
            print("Invalid date or number")
            return

        chart_card = ChartCard()
        chart_card.label_text = name
        chart_card.current_value = value
        chart_card.target_value = target
        chart_card.update_display()

        chart_area = self.root.get_screen("main").ids.chart_area
        chart_area.add_widget(chart_card)

        # Update cols and height dynamically
        self.update_chart_cols()

        # Add to history
        history_container = self.root.get_screen("main").ids.history_container
        row = MDBoxLayout(size_hint_y=None, height=dp(32))
        row.add_widget(MDLabel(text=name))
        row.add_widget(MDLabel(text=date))
        row.add_widget(MDLabel(text=str(value), halign="right", theme_text_color="Custom", text_color=(0, 1, 0, 1)))
        history_container.add_widget(row)

        self.safe_dismiss()

    def show_update_dialog(self, card):
        self.safe_dismiss()
        content = EditCardContent(card)
        self.dialog = MDDialog(
            title=f"Update {card.label_text}",
            type="custom",
            content_cls=content,
            size_hint=(0.9, None),
            height=dp(280),
            buttons=[
                MDRaisedButton(text="UPDATE", on_release=lambda x: self.update_card(card, content), md_bg_color=get_color_from_hex("#F89411"), text_color=(1,1,1,1)),
                MDFlatButton(text="CANCEL", on_release=lambda x: self.safe_dismiss())
            ],
            auto_dismiss=False
        )
        self.dialog.open()

    def update_card(self, card, content):
        try:
            card.label_text = content.name_input.text.strip()
            card.current_value = float(content.value_input.text.strip())
            card.update_display()
        except Exception as e:
            print("Error updating card:", e)
        self.safe_dismiss()

    def update_chart_cols(self, *args):
        chart_area = self.root.get_screen("main").ids.chart_area
        card_width = dp(130) + dp(16)  
        available_width = Window.width - dp(220) - dp(48) 
        cols = max(int(available_width // card_width), 1)
        chart_area.cols = cols

        # Calculate rows needed and adjust height accordingly
        rows = (len(chart_area.children) + cols - 1) // cols
        chart_area.height = rows * (dp(160) + dp(16)) 


if __name__ == '__main__':
    FinanceTrackerApp().run()
