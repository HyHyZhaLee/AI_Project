from ai_detector import *
from adafruit_MQTT import *

# Uploading image to server
class Task1:
    def __init__(self, camera):
        self.camera = camera
        self.ai_result = ""
        self.confident = ""
        self.image = ""
        if camera.IP == 0 or camera.IP == 1:
            print("Init task 1: Publishing image and AI result with default camera")
        else:
            print("Init task 1: Publishing image and AI result with IP:", camera.IP)

    def run(self):
        self.ai_result, self.confident, self.image = self.camera.ai_detector()

    def publishImage(self):
        publish("image", self.image)

    def publishResult(self):
        publish("ai", self.ai_result)
        publish("confident-score", self.confident)
