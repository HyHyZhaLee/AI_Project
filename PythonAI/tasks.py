from ai_detector import *
from adafruit_MQTT import *

# Uploading image to server
class Task1:
    def __init__(self, IP=0):
        self.IP = IP
        self.ai_result = ""
        self.confident = ""
        self.image = ""
        if IP == 0 or IP == 1:
            print("Init task 1: Publishing image and AI result with default camera")
        else:
            print("Init task 1: Publishing image and AI result with IP:", IP)

    def run(self):
        self.ai_result, self.confident, self.image = ai_detector(self.IP)

    def publishImage(self):
        publish("image", self.image)

    def publishResult(self):
        publish("ai", self.ai_result)
        publish("confident-score", self.confident)


