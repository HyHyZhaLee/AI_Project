from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.text import LabelBase

kv = """
<Gauge>:
    size_hint: None, None
    size: (root.radius*2, root.radius*2)
    pos_hint: {"center_x": .5, "center_y": .5}
    canvas.before:
        Color:
            rgba: root.bar_color + [0.3]
        Line:
            width: root.bar_width
            ellipse: (self.x, self.y, self.width, self.height, 225, 495)
    canvas.after:
        Color:
            rgb: root.bar_color
        Line:
            width: root.bar_width
            ellipse: (self.x, self.y, self.width, self.height, 225, 225+self.percent)
    MDLabel:
        text: '%s'%root.content
        font_size: root.width/4
        pos_hint: {"center_x":0.5, "center_y":0.5}
        halign: "center"
        color: root.bar_color + [0.7]
"""

Builder.load_string(kv)

class Gauge(BoxLayout):
    radius = NumericProperty(100)
    bar_color = ListProperty([1, 0, 100/255])
    bar_width = NumericProperty(10)
    min_value = NumericProperty(0)
    max_value = NumericProperty(100)
    value = NumericProperty(50)
    percent = NumericProperty(0)
    content = StringProperty("0%")
    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
        self.percent = 270/(self.max_value - self.min_value) * (self.value-self.min_value)
    def re_draw(self):
        with self.canvas:
            self.canvas.clear()
            self._refresh_text()
        #TODO


class GaugeWithName(BoxLayout):
    pass