from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from app_function.Camera import *
from app_function.adafruit_MQTT import *
Builder.load_file('views/dashboard/dashboard.kv')

recent_cam = Camera(0)

class Dashboard(MDBoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def access_ids(self):
        for id_name in self.ids.keys():
            print("ID:", id_name)

    def btn_connect_on_press(self):
        button = self.ids.btn_connect
        button.canvas.before.children[0].rgb = (0.2, 0.5, 0.7, 1)
        if self.ids.IP.text == "":
            self.ids.terminal.print_terminal("Connecting to webcam...")
        else:
            self.ids.terminal.print_terminal("Connecting to Camera IP:... " + self.ids.IP.text)

    def btn_connect_on_release(self):
        button = self.ids.btn_connect
        button.canvas.before.children[0].rgb = (11 / 255, 205 / 255, 215 / 255)

        global recent_cam
        recent_cam.camera.release()
        cv2.destroyAllWindows()
        if self.ids.IP.text == "":
            recent_cam = Camera(0)
            self.capture = recent_cam.camera
        else:
            recent_cam = Camera(self.ids.IP.text)
            self.capture = recent_cam.camera
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)


    def btn_webcam_on_press(self):
        button = self.ids.btn_webcam
        button.canvas.before.children[0].rgb = (0.2, 0.5, 0.7, 1)
        self.ids.terminal.print_terminal("Connecting to webcam...")

    def btn_webcam_on_release(self):
        button = self.ids.btn_webcam
        button.canvas.before.children[0].rgb = (11 / 255, 205 / 255, 215 / 255)
        global recent_cam
        recent_cam.camera.release()
        cv2.destroyAllWindows()
        recent_cam = Camera(0)
        self.capture = recent_cam.camera
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)

    def load_video(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.cameraView.texture = texture

    def ai_run(self):
        global recent_cam
        global ai, confident, image
        ai, confident, image = recent_cam.ai_detector()
    def publishImage(self):
        global image
        publish("image", image)

    def publishResult(self):
        global ai
        global confident
        publish("ai", ai)
        publish("confident-score", confident)