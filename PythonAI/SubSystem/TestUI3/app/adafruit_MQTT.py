from Adafruit_IO import MQTTClient
import sys

AIO_FEED_ID = ["ai", "humi", "temp", "image", "led", "confident-score"]
AIO_USERNAME = "AI_ProjectHGL"
AIO_KEY = "key_ppFS7373j0IuEZfAlPIJ9MrOVMWN"
AIO_KEY = AIO_KEY.replace(AIO_KEY[:3], "aio")
client = MQTTClient(AIO_USERNAME, AIO_KEY)

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
    payload = payload.replace("\n", "")  # Remove carriage return in payload
    print("Receive value from server:", payload, ", feed id:", feed_id)
def Adafruit_connect():
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe
    client.connect()
    client.loop_background()

def publish(feed_ID, data):
    client.publish(feed_ID, data)