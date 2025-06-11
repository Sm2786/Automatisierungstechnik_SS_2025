import paho.mqtt.client as mqtt
from tinydb import TinyDB, Query
import os
import sys
from database import db_connector_temp, db_connector_blue, db_connector_red, db_connector_green, db_connector_ground_truth, db_connector_drop_osci,db_connector_weight        

broker = "158.180.44.197"
port = 1883
topic = "iot1/#"
payload = "on"

# create function for callback
def on_message(client, userdata, message):
    if message.topic == "iot1/teaching_factory/temperature":
        db_connector_temp.insert({"temperature": message.payload.decode()})
    elif message.topic == "iot1/teaching_factory/dispenser_blue":
        db_connector_blue.insert({"dispenser_blue": message.payload.decode()})
    elif message.topic == "iot1/teaching_factory/dispenser_red":
        db_connector_red.insert({"dispenser_red": message.payload.decode()})
    elif message.topic == "iot1/teaching_factory/dispenser_green":
        db_connector_green.insert({"dispenser_green": message.payload.decode()})
    elif message.topic == "iot1/teaching_factory/ground_truth":
        db_connector_ground_truth.insert({"ground_truth": message.payload.decode()})
    elif message.topic == "iot1/teaching_factory/drop_oscillation":
        db_connector_drop_osci.insert({"drop_oscillation": message.payload.decode()})
    elif message.topic == "iot1/teaching_factory/scale/final_weight":
        db_connector_weight.insert({"final_weight": message.payload.decode()})

    print("message received:")
    print("topic: ", message.topic)
    print("message: ", message.payload.decode())
    print("\n")

# create client object
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("bobm", "letmein")              

# assign function to callback
mqttc.on_message = on_message                         

# establish connection
mqttc.connect(broker,port)                                 

# subscribe
mqttc.subscribe(topic, qos=0)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
#mqttc.loop_forever()

while True:
   mqttc.loop(0.5)