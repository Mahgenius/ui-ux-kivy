from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Window.size = (300, 500)

history_data = []

class CalculatorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical')

        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, padding=[5, 5])
        header_layout.add_widget(Label(text="Kalkulator", font_size=18, bold=True))
        
        history_btn = Button(
            text="History", 
            size_hint_x=0.4, 
            on_press=self.go_to_history
        )
        header_layout.add_widget(history_btn)
        main_layout.add_widget(header_layout)

        self.result = TextInput(
            font_size=40,
            size_hint_y=0.3,
            readonly=True,
            halign="right",
            multiline=False,
        )
        main_layout.add_widget(self.result)

        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '00', '.', '=']
        ]

        grid = GridLayout(cols=4, spacing=5, padding=10)
        for row in buttons:
            for item in row:
                button = Button(
                    text=item,
                    font_size=28,
                    on_press=self.button_click
                )
                grid.add_widget(button)

        main_layout.add_widget(grid)
        self.add_widget(main_layout)

    def button_click(self, instance):
        text = instance.text

        if text == "C":
            self.result.text = ""
        elif text == "=":
            self.calculate()
        elif text == "+/-":
            self.toggle_neg()
        elif text == "%":
            self.convert_percent()
        else:
            self.result.text += text

    def calculate(self):
        try:
            expression = self.result.text
            if expression:
                outcome = str(eval(expression))
                # Simpan ke riwayat jika perhitungan berhasil
                history_data.append(f"{expression} = {outcome}")
                self.result.text = outcome
        except Exception:
            self.result.text = "ERROR!"    

    def toggle_neg(self):
        if self.result.text:
            self.result.text = self.result.text[1:] if self.result.text[0] == "-" else "-" + self.result.text

    def convert_percent(self):
        try:
            self.result.text = str(float(self.result.text)/100)
        except ValueError:
            self.result.text = "ERROR!"

    def go_to_history(self, instance):
        self.manager.current = 'history'


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        back_btn = Button(text="< Kembali", size_hint_x=0.4, on_press=self.go_back)
        title = Label(text="Riwayat", font_size=20, bold=True)
        header.add_widget(back_btn)
        header.add_widget(title)
        self.main_layout.add_widget(header)

        self.scroll = ScrollView(size_hint_y=0.9)
        self.history_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.history_list_layout.bind(minimum_height=self.history_list_layout.setter('height'))
        self.scroll.add_widget(self.history_list_layout)
        
        self.main_layout.add_widget(self.scroll)
        self.add_widget(self.main_layout)

    def on_enter(self):
        """Dipanggil otomatis setiap kali membuka halaman history untuk menyegarkan tampilan."""
        self.refresh_history()

    def refresh_history(self):
        self.history_list_layout.clear_widgets()

        if not history_data:
            empty_label = Label(text="Belum ada riwayat", size_hint_y=None, height=40)
            self.history_list_layout.add_widget(empty_label)
            return

        for index, item in enumerate(history_data):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
            lbl = Label(text=item, halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            
            del_btn = Button(
                text="Delete", 
                size_hint_x=0.3,
                background_color=(0.9, 0.2, 0.2, 1)
            )
            del_btn.bind(on_press=lambda btn, idx=index: self.delete_entry(idx))
            
            row.add_widget(lbl)
            row.add_widget(del_btn)
            self.history_list_layout.add_widget(row)

    def delete_entry(self, index):
        history_data.pop(index)
        self.refresh_history()

    def go_back(self, instance):
        self.manager.current = 'calculator'


class CalculatorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CalculatorScreen(name='calculator'))
        sm.add_widget(HistoryScreen(name='history'))
        return sm

if __name__ == "__main__":
    CalculatorApp().run()