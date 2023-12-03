print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
import random

BROKER_ADDRESS = "192.168.103.221"
PORT = 1883
DEVICE_ID="9319ec10-8c61-11ee-a031-1bfbce5814c5"
# DEVICE_ACCESS_TOKEN = "LY0bXYpJnjutBESSG9JS"
DEVICE_ACCESS_TOKEN = "TuiFY2CygjMRHnsmldIz"
# DEVICE_ACCESS_TOKEN = "4R0O8IYTYG2LRBhn91DB"




def subscribed(client, userdata, mid, granted_qos):
    # print("Subscribed...")
    pass


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:        
        client.subscribe("v1/devices/me/rpc/request/+")
        
        
        
        print("Thingsboard connected successfully!!")
        
        
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(DEVICE_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

flame = 0
smoke = 0


while True:
    try:
        flame = random.randrange(1,5000)
        smoke = random.randrange(1,500)
        collect_data = {
            'FLAME':flame,
            'SMOKE':smoke
        }
        print(collect_data)
        client.publish(f'v1/devices/me/telemetry', json.dumps(collect_data), 1)
        time.sleep(20)
    except KeyboardInterrupt:
        break