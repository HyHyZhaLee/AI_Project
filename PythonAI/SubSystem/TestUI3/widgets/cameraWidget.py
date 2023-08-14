from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock

from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import base64
import requests

kv = """
<CameraWidget>:
    orientation:'vertical'
    padding: dp(8)
    spacing: dp(16)
    Image: 
        source:'./assets/imgs/NoCamera.png'
"""
Builder.load_string(kv)
class CameraWidget(MDBoxLayout):
    pass
