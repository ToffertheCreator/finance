from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout


class SAVINGS(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        # Sidebar
        self.add_widget(self.build_sidebar())

        # Main Content
        self.add_widget(self.build_main_content())

    def build_sidebar(self):
        sidebar = MDBoxLayout(
            orientation="vertical",
            size_hint=(0.25, 1),
            md_bg_color=[0.1, 0.1, 0.1, 1],
            padding=10,
            spacing=15
        )
        sidebar.add_widget(
            MDLabel(
                text="FINANCE TRACKER",
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1],
                bold=True,
                halign="left"
            )
        )
        sections = ["Dashboard", "Analytics", "Savings", "Transaction", "Settings"]
        for section in sections:
            color = [1, 1, 1, 1] if section == "Savings" else [0.7, 0.7, 0.7, 1]
            sidebar.add_widget(
                MDLabel(
                    text=section,
                    theme_text_color="Custom",
                    text_color=color,
                    halign="left"
                )
            )
        return sidebar

    def build_main_content(self):
        content = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        # Header
        header = MDBoxLayout(orientation="horizontal", size_hint=(1, None), height=50)
        header.add_widget(
            MDLabel(
                text="SAVINGS",
                bold=True,
                text_color= [1, 1, 1, 1],
                halign="left"
            )
        )
        # Replacing button with styled label (for outline purposes)
        header.add_widget(
            MDLabel(
                text="[ Add new savings + ]",
                theme_text_color="Custom",
                text_color=[1, 0.5, 0, 1],
                halign="right"
            )
        )
        content.add_widget(header)

        # Circular Progress Cards (placeholders)
        progress_cards = MDBoxLayout(orientation="horizontal", spacing=20, size_hint=(1, None), height=180)
        for title in ["sample 1", "sample 2", "sample 3"]:
            card = MDCard(orientation="vertical", size_hint=(None, None), size=(200, 180), padding=10, radius=[15])
            card.add_widget(MDLabel(text="10%", halign="center"))
            card.add_widget(MDLabel(text=title, halign="center" ))
            card.add_widget(MDLabel(text="1000/20000", halign="center"))
            progress_cards.add_widget(card)
        content.add_widget(progress_cards)

        # History Card
        history_card = MDCard(orientation="vertical", padding=15, size_hint=(1, None), height=250, radius=[15])
        history_card.add_widget(MDLabel(text="History", halign="left"))

        # Fake Table using GridLayout
        table = MDGridLayout(cols=3, spacing=10, size_hint_y=None)
        table.bind(minimum_height=table.setter('height'))

        headers = ["[b]Name[/b]", "[b]Date[/b]", "[b]Amount[/b]"]
        for head in headers:
            table.add_widget(MDLabel(text=head, markup=True))

        # Static rows
        rows = [
            ("sample 1", "05/09/2025", "[color=00FF00]1000.00[/color]"),
            ("sample 2", "05/09/2025", "[color=00FF00]1000.00[/color]"),
            ("sample 3", "05/09/2025", "[color=00FF00]1000.00[/color]"),
        ]
        for name, date, amount in rows:
            table.add_widget(MDLabel(text=name))
            table.add_widget(MDLabel(text=date))
            table.add_widget(MDLabel(text=amount, markup=True))

        history_card.add_widget(table)
        content.add_widget(history_card)

        return content


class SavingsApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return SAVINGS()

#GUIDE ME LORD
if __name__ == "__main__":
    SavingsApp().run()
