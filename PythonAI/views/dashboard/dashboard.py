from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from app_function.Camera import *
from app_function.adafruit_MQTT import *

Builder.load_file('views/dashboard/dashboard.kv')

class Dashboard(MDBoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.recent_cam = None
        self.capture = None

    def access_ids(self):
        for id_name in self.ids.keys():
            print("ID:", id_name)

    def connect_camera(self, ip=None):
        if self.recent_cam:
            self.recent_cam.camera.release()
            cv2.destroyAllWindows()

        if ip is None or ip == "":
            self.ids.terminal.print_terminal("Connecting to webcam...")
            self.recent_cam = Camera(0)
        else:
            self.ids.terminal.print_terminal(f"Connecting to Camera IP: {ip}")
            self.recent_cam = Camera(ip)

        self.capture = self.recent_cam.camera
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)
        Clock.schedule_interval(self.recent_cam.publishImage, 3)
        Clock.schedule_interval(self.recent_cam.publishResult, 3)

    def btn_connect_on_press(self):
        self.ids.btn_connect.canvas.before.children[0].rgb = (0.2, 0.5, 0.7, 1)
        self.ids.terminal.print_terminal("Connecting to webcam..." if self.ids.IP.text == "" else f"Connecting to Camera IP: {self.ids.IP.text}")

    def btn_connect_on_release(self):
        self.ids.btn_connect.canvas.before.children[0].rgb = (11 / 255, 205 / 255, 215 / 255)
        self.connect_camera(self.ids.IP.text)

    def btn_webcam_on_press(self):
        self.ids.btn_webcam.canvas.before.children[0].rgb = (0.2, 0.5, 0.7, 1)
        self.ids.terminal.print_terminal("Connecting to webcam...")

    def btn_webcam_on_release(self):
        self.ids.btn_webcam.canvas.before.children[0].rgb = (11 / 255, 205 / 255, 215 / 255)
        self.connect_camera()

    def load_video(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.cameraView.texture = texture
