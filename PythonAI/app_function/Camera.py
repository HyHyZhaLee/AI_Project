from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import base64
import requests


class Camera:
    def __init__(self, IP):
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        self.model = load_model("app_function/keras_model.h5", compile=False)

        # Load the labels
        self.class_names = open("app_function/labels.txt", "r").readlines()

        # CAMERA can be 0 or 1 based on default camera of your computer
        # An ip of your camera can be used as well
        self.IP = IP
        if IP == 0 or IP == 1:
            self.camera = cv2.VideoCapture(0)
        else:
            port = 81
            # URL for streaming
            stream_url = 'http://{}:{}/stream'.format(IP, port)
            # Tạo một đối tượng VideoCapture với URL streaming
            self.camera = cv2.VideoCapture(stream_url)

    def ai_detector(self):
        # Grab the web camera's image.
        ret, image = self.camera.read()
        res, frame = cv2.imencode('.jpg', image)
        data = base64.b64encode(frame)

        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Show the image in a window
        # cv2.imshow("Webcam Image", image)

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        prediction = self.model.predict(image)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        # print("Class:", class_name[2:], end="")
        # print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        return class_name[2:], str(np.round(confidence_score * 100))[:-2] + "%", data

    def adjust_led_intensity(self, intensity):
        # The IP address of the ESP32-CAM
        ip_address = self.IP

        # Create LED control URL with new brightness value
        url = 'http://{}/control?var=led_intensity&val={}'.format(ip_address, intensity)

        # Send HTTP GET request to adjust LED brightness
        response = requests.get(url)

        # Check if the request was successful or not
        if response.status_code == 200:
            print('LED brightness has been adjusted successfully.')
        else:
            print('LED brightness cannot be adjusted.')
