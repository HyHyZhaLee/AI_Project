from ai_detector import *
from adafruit_MQTT import *
from softwaretimer import *

# Uploading image to server
class Task1:
    def __init__(self):
        print("Init task 1: Publishing image")
        return

    def run(self, IP=0):
        ai_result, confident, image = ai_detector(IP)
        publish("image", image)


class Task2:
    def __init__(self):
        print("Init task 2: Publishing AI result and confident score")
        return

    def run(self, IP=0):
        ai_result, confident, image = ai_detector(IP)
        publish("ai", ai_result)
        publish("confident-score", confident)
