from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import cv2
import numpy as np
from kivymd.uix.boxlayout import MDBoxLayout
from adafruit_MQTT import *
Builder.load_file('views/dashboard/dashboard.kv')

class Dashboard(MDBoxLayout):

    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def access_ids(self):
        for id_name in self.ids.keys():
            print("ID:", id_name)

    def btn_connect_on_press(self):
        button = self.ids.btn_connect
        button.canvas.before.children[0].rgb = (0.2, 0.5, 0.7, 1)
        self.ids.terminal.print_terminal("Connecting to camera...")

    def btn_connect_on_release(self):
        button = self.ids.btn_connect
        button.canvas.before.children[0].rgb = (11 / 255, 205 / 255, 215 / 255)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)

    def btn_webcam_on_press(self):
        button = self.ids.btn_webcam
        button.canvas.before.children[0].rgb = (0.2, 0.5, 0.7, 1)
        self.ids.terminal.print_terminal("Connecting to camera...")
    def btn_webcam_on_release(self):
        button = self.ids.btn_webcam
        button.canvas.before.children[0].rgb = (11 / 255, 205 / 255, 215 / 255)

    def load_video(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.cameraView.texture = texture