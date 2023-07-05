from ai_detector import *
from adafruit_MQTT import *

#Uploading image to server
class Task1:
    def __init__(self):
        print("Init task 1")
        return

    def Task1_Run(self):
        ai_result, image = ai_detector(0)
        publish("ai", ai_result)
        publish("image", image)