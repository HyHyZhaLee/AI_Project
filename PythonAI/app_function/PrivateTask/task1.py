from app_function.adafruit_MQTT import *

# Uploading image to server
class Task1:
    def __init__(self):
        print("Init task 1: Connect to adafruit server")
    def run(self):
        Adafruit_connect()