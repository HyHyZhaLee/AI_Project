from ai_detector import *
from adafruit_MQTT import *

# Uploading image to server
class Task1:
    def __init__(self):
        self.ai_result = ""
        self.confident = ""
        self.image = ""
        print("Init task 1: Publishing image and AI result")

    def run(self, IP=0):
        self.ai_result, self.confident, self.image = ai_detector(IP)

    def publishImage(self):
        publish("image", self.image)

    def publishResult(self):
        publish("ai", self.ai_result)
        publish("confident-score", self.confident)


