from kivy.core.image import Texture
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock

import cv2
import numpy as np

kv = """
<CameraWidget>:
    orientation: 'vertical'
    padding: dp(8)
    spacing: dp(16)
    Image:
        id: camera_image
        source: './assets/imgs/NoCamera.png'
"""

Builder.load_string(kv)

class CameraWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)

    def load_video(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.camera_image.texture = texture

