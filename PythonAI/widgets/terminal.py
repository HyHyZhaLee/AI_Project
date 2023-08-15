from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

kv = """
<Terminal>:
    orientation: 'vertical'
    spacing: dp(5)
    padding: dp(10)

    ScrollView:
       
        id: terminal_scrollview

        MDList:
            id: terminal_list

    MDSeparator:

    MDTextField:
        id: input_field
        hint_text: 'Enter a command'
        multiline: False
        on_text_validate: root.handle_input(self.text)
"""

Builder.load_string(kv)
class Terminal(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def print_terminal(self, message):
        label = MDLabel(text=message, size_hint_y=None, text_size=(self.width, None))
        label.bind(texture_size=label.setter('size'))
        label.height = label.texture_size[1]  # Đảm bảo chiều cao của label tự động điều chỉnh
        label.padding_y = dp(5)  # Đặt khoảng cách giữa các dòng
        self.ids.terminal_list.add_widget(label)
        self.ids.terminal_scrollview.scroll_y = 0
        self.ids.input_field.focus = True
        self.ids.terminal_scrollview.scroll_y = 1

    def handle_input(self, command):
        self.print_terminal("User entered: " + command)
        self.ids.input_field.text = ""