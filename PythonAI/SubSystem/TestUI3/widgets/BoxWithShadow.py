from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ColorProperty, ListProperty, StringProperty
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp, sp
from kivy.utils import rgba

kv = """
<BoxWithShadow>:
    canvas.before:
        # BoxShadow statements
        Color:
            rgba: 0, 0, 0, 0.65
        BoxShadow:
            pos: self.pos
            size: self.size
            offset: 0, 3
            blur_radius: 20
            spread_radius: -10, -10
            border_radius: 16,16,16,16
    canvas:
        # target element statements
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [18,18,18,18]  # Đặt bán kính bo tròn ở đây
"""
Builder.load_string(kv)
class BoxWithShadow(ButtonBehavior, BoxLayout):
    pass