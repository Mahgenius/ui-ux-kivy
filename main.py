from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.metrics import dp
from kivy.lang import Builder

BG_DARK = (0.07, 0.09, 0.14, 1)        
CARD_BG = (0.12, 0.15, 0.22, 1)        
ACCENT_CYAN = (0.15, 0.85, 0.85, 1)    
ACCENT_PURPLE = (0.55, 0.35, 0.95, 1)  
ACCENT_PINK = (0.95, 0.30, 0.55, 1)    
ACCENT_GREEN = (0.25, 0.85, 0.45, 1)   
TEXT_LIGHT = (0.92, 0.94, 0.98, 1)
TEXT_MUTED = (0.55, 0.60, 0.70, 1)

Window.clearcolor = BG_DARK

KV = """
<RoundedButton@Button>:
    btn_color: 1, 1, 1, 1
    btn_color_down: 0.8, 0.8, 0.8, 1
    background_normal: ''
    background_down: ''
    background_color: (0,0,0,0)
    font_size: '18sp'
    bold: True
    color: 1,1,1,1
    canvas.before:
        Color:
            rgba: root.btn_color if root.state != 'down' else root.btn_color_down
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [18,]
"""
Builder.load_string(KV)


class RoundedButtonBase(Button):
    """Custom button dengan properti warna dinamis (dipakai lewat KV di atas)."""
    pass


class ColoredCard(BoxLayout):
    """BoxLayout dengan background rounded rectangle berwarna."""
    def __init__(self, bg_color=CARD_BG, radius=24, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size


def make_button(text, color):
    """Helper membuat tombol bulat/rounded dengan warna kustom."""
    from kivy.factory import Factory
    btn = Factory.RoundedButton()
    btn.text = text
    btn.btn_color = color
    btn.btn_color_down = tuple(max(c - 0.15, 0) for c in color[:3]) + (1,)
    return btn


# ------------------- Layar Utama (Navigasi) -------------------
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(25))

        title = Label(
            text='[b]Time Studio[/b]',
            markup=True,
            font_size='34sp',
            color=ACCENT_CYAN,
            size_hint=(1, 0.25),
        )
        subtitle = Label(
            text='Pilih mode di bawah ini',
            font_size='16sp',
            color=TEXT_MUTED,
            size_hint=(1, 0.1),
        )
        root.add_widget(title)
        root.add_widget(subtitle)

        btn_timer = make_button('TIMER', ACCENT_PURPLE)
        btn_timer.size_hint = (1, 0.25)
        btn_timer.bind(on_release=lambda x: self.go_to('timer'))

        btn_stopwatch = make_button('STOPWATCH', ACCENT_CYAN)
        btn_stopwatch.size_hint = (1, 0.25)
        btn_stopwatch.bind(on_release=lambda x: self.go_to('stopwatch'))

        root.add_widget(btn_timer)
        root.add_widget(btn_stopwatch)
        root.add_widget(BoxLayout(size_hint=(1, 0.15)))

        self.add_widget(root)

    def go_to(self, name):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = name


class TimerScreen(Screen):
    remaining = NumericProperty(0)
    running = BooleanProperty(False)
    display_text = StringProperty('00:00:00')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._event = None
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation='vertical', padding=dp(24), spacing=dp(18))

        header = BoxLayout(size_hint=(1, 0.12))
        back_btn = make_button('X', ACCENT_PURPLE)
        back_btn.size_hint = (0.2, 1)
        back_btn.bind(on_release=lambda x: self.go_back())
        title = Label(text='[b]Timer[/b]', markup=True, font_size='26sp', color=TEXT_LIGHT)
        header.add_widget(back_btn)
        header.add_widget(title)
        root.add_widget(header)

        display_card = ColoredCard(bg_color=CARD_BG, orientation='vertical', size_hint=(1, 0.35), padding=dp(10))
        self.time_label = Label(
            text=self.display_text,
            font_size='56sp',
            bold=True,
            color=ACCENT_CYAN,
        )
        display_card.add_widget(self.time_label)
        root.add_widget(display_card)

        input_row = BoxLayout(size_hint=(1, 0.15), spacing=dp(12))
        self.hh_input = TextInput(hint_text='JJ', input_filter='int', multiline=False,
                                   font_size='22sp', halign='center', padding_y=[dp(14), 0],
                                   background_color=CARD_BG, foreground_color=TEXT_LIGHT,
                                   cursor_color=ACCENT_CYAN)
        self.mm_input = TextInput(hint_text='MM', input_filter='int', multiline=False,
                                   font_size='22sp', halign='center', padding_y=[dp(14), 0],
                                   background_color=CARD_BG, foreground_color=TEXT_LIGHT,
                                   cursor_color=ACCENT_CYAN)
        self.ss_input = TextInput(hint_text='DD', input_filter='int', multiline=False,
                                   font_size='22sp', halign='center', padding_y=[dp(14), 0],
                                   background_color=CARD_BG, foreground_color=TEXT_LIGHT,
                                   cursor_color=ACCENT_CYAN)
        input_row.add_widget(self.hh_input)
        input_row.add_widget(self.mm_input)
        input_row.add_widget(self.ss_input)
        root.add_widget(input_row)

        btn_row = BoxLayout(size_hint=(1, 0.18), spacing=dp(12))
        self.start_btn = make_button('MULAI', ACCENT_GREEN)
        self.start_btn.bind(on_release=lambda x: self.start_timer())
        self.pause_btn = make_button('JEDA', ACCENT_PURPLE)
        self.pause_btn.bind(on_release=lambda x: self.pause_timer())
        self.reset_btn = make_button('RESET', ACCENT_PINK)
        self.reset_btn.bind(on_release=lambda x: self.reset_timer())
        btn_row.add_widget(self.start_btn)
        btn_row.add_widget(self.pause_btn)
        btn_row.add_widget(self.reset_btn)
        root.add_widget(btn_row)

        self.status_label = Label(text='Atur waktu lalu tekan Mulai', color=TEXT_MUTED,
                                   size_hint=(1, 0.1), font_size='14sp')
        root.add_widget(self.status_label)

        self.add_widget(root)

    def go_back(self):
        self.pause_timer()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'menu'

    def start_timer(self):
        if not self.running:
            if self.remaining <= 0:
                try:
                    h = int(self.hh_input.text or 0)
                    m = int(self.mm_input.text or 0)
                    s = int(self.ss_input.text or 0)
                except ValueError:
                    h, m, s = 0, 0, 0
                self.remaining = h * 3600 + m * 60 + s
                if self.remaining <= 0:
                    self.status_label.text = 'Masukkan waktu terlebih dahulu!'
                    return
            self.running = True
            self.status_label.text = 'Sedang berjalan...'
            self._event = Clock.schedule_interval(self._tick, 1)

    def pause_timer(self):
        self.running = False
        self.status_label.text = 'Dijeda' if self.remaining > 0 else self.status_label.text
        if self._event:
            self._event.cancel()
            self._event = None

    def reset_timer(self):
        self.pause_timer()
        self.remaining = 0
        self.hh_input.text = ''
        self.mm_input.text = ''
        self.ss_input.text = ''
        self.time_label.text = '00:00:00'
        self.status_label.text = 'Atur waktu lalu tekan Mulai'

    def _tick(self, dt):
        if self.remaining > 0:
            self.remaining -= 1
            self.time_label.text = self._format(self.remaining)
        else:
            self.pause_timer()
            self.status_label.text = "Waktu habis!"
            self.time_label.text = '00:00:00'

    @staticmethod
    def _format(total_seconds):
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f'{h:02d}:{m:02d}:{s:02d}'


class StopwatchScreen(Screen):
    elapsed = NumericProperty(0.0)
    running = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._event = None
        self.lap_count = 0
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation='vertical', padding=dp(24), spacing=dp(16))

        header = BoxLayout(size_hint=(1, 0.12))
        back_btn = make_button('X', ACCENT_CYAN)
        back_btn.size_hint = (0.2, 1)
        back_btn.bind(on_release=lambda x: self.go_back())
        title = Label(text='[b]Stopwatch[/b]', markup=True, font_size='26sp', color=TEXT_LIGHT)
        header.add_widget(back_btn)
        header.add_widget(title)
        root.add_widget(header)

        display_card = ColoredCard(bg_color=CARD_BG, orientation='vertical', size_hint=(1, 0.3), padding=dp(10))
        self.time_label = Label(text='00:00:00.0', font_size='50sp', bold=True, color=ACCENT_PURPLE)
        display_card.add_widget(self.time_label)
        root.add_widget(display_card)

        btn_row = BoxLayout(size_hint=(1, 0.15), spacing=dp(12))
        self.start_btn = make_button('MULAI', ACCENT_GREEN)
        self.start_btn.bind(on_release=lambda x: self.start_stopwatch())
        self.lap_btn = make_button('LAP', ACCENT_PURPLE)
        self.lap_btn.bind(on_release=lambda x: self.add_lap())
        self.reset_btn = make_button('RESET', ACCENT_PINK)
        self.reset_btn.bind(on_release=lambda x: self.reset_stopwatch())
        btn_row.add_widget(self.start_btn)
        btn_row.add_widget(self.lap_btn)
        btn_row.add_widget(self.reset_btn)
        root.add_widget(btn_row)

        lap_label = Label(text='Riwayat Lap', color=TEXT_MUTED, size_hint=(1, 0.08), font_size='14sp')
        root.add_widget(lap_label)

        self.lap_list = GridLayout(cols=1, size_hint_y=None, spacing=dp(6))
        self.lap_list.bind(minimum_height=self.lap_list.setter('height'))
        scroll = ScrollView(size_hint=(1, 0.35))
        scroll.add_widget(self.lap_list)
        root.add_widget(scroll)

        self.add_widget(root)

    def go_back(self):
        self.pause_stopwatch()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'menu'

    def start_stopwatch(self):
        if not self.running:
            self.running = True
            self._event = Clock.schedule_interval(self._tick, 0.1)

    def pause_stopwatch(self):
        self.running = False
        if self._event:
            self._event.cancel()
            self._event = None

    def reset_stopwatch(self):
        self.pause_stopwatch()
        self.elapsed = 0.0
        self.time_label.text = '00:00:00.0'
        self.lap_list.clear_widgets()
        self.lap_count = 0

    def add_lap(self):
        if self.running:
            self.lap_count += 1
            lap_row = ColoredCard(bg_color=(0.16, 0.19, 0.28, 1), size_hint_y=None, height=dp(40), padding=dp(8))
            lap_row.add_widget(Label(text=f'Lap {self.lap_count}', color=ACCENT_CYAN, size_hint=(0.4, 1)))
            lap_row.add_widget(Label(text=self.time_label.text, color=TEXT_LIGHT, size_hint=(0.6, 1)))
            self.lap_list.add_widget(lap_row, index=len(self.lap_list.children))

    def _tick(self, dt):
        self.elapsed += dt
        self.time_label.text = self._format(self.elapsed)

    @staticmethod
    def _format(total_seconds):
        h = int(total_seconds // 3600)
        m = int((total_seconds % 3600) // 60)
        s = int(total_seconds % 60)
        ms = int((total_seconds * 10) % 10)
        return f'{h:02d}:{m:02d}:{s:02d}.{ms}'

class TimeStudioApp(App):
    def build(self):
        self.title = 'Time Studio - Timer & Stopwatch'
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TimerScreen(name='timer'))
        sm.add_widget(StopwatchScreen(name='stopwatch'))
        return sm


if __name__ == '__main__':
    TimeStudioApp().run()
