from Adafruit_IO import MQTTClient
import sys
import time

AIO_FEED_ID = ["ai", "humi", "temp", "image", "led", "confident-score"]
AIO_USERNAME = "AI_ProjectHGL"
AIO_KEY = "aio" + "_NMuW54hPxBRRipuFGlzH4VPl5tec"
client = MQTTClient(AIO_USERNAME, AIO_KEY)

global mess
mess = ""  # Initialize mess variable before use to check duplication of published data with message

def connected(client):
    print("Connected to server ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to server ...")

def disconnected(client):
    print("Disconnected ...")
    sys.exit(1)

def message(client, feed_id, payload):
    global mess  # Using the global mess variable
    payload = payload.replace("\n", "")  # Remove carriage return in payload
    if payload != mess:  # Check if the payload duplicates the published data
        print("Receive value from server:", payload, ", feed id:", feed_id)
    mess = ""

def Adafruit_connect():
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe
    client.connect()
    client.loop_background()

def publish(feed_ID, data):
    global mess  # Using the global mess variable
    client.publish(feed_ID, data)
    print("Published data to feed:", feed_ID)
    mess = str(data)  # Store the data value in the variable mess

# Adafruit_connect()
#
# # while True:
# #     publish("Temp", 30.5)
# #     time.sleep(3)
