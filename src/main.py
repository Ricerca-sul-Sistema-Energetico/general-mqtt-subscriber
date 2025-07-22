from read_config import project_name, field_name, mqtt_config, influx_config, Logger
from factory_clients import mqtt_client, influx_client
from paho.mqtt.client import MQTTMessage
from datetime import datetime as dt
import time
import json

fields_dict = {}
device_name = ""
timestamp = dt.now()


def on_message_mqtt(client, userdata, msg: MQTTMessage):
    global fields_dict
    global device_name
    global timestamp
    Logger.info(f"MQTT message arrived from topic:{msg.topic}")
    payload_dict = json.loads(msg.payload)
    timestamp = dt.fromtimestamp(payload_dict["timestamp"])
    value = payload_dict["value"]
    Logger.info(timestamp)
    device_name = msg.topic.split("/")[-2]
    name = msg.topic.split("/")[-1]
    fields_dict[name] = value


def write_influx_data():
    global fields_dict
    if len(fields_dict) == 0:
        Logger.warning("Fields dict still empty")
        return
    Logger.info("Ready to write influx points")
    device_influx_dict = {
        "measurement": device_name,
        "time": f"{timestamp}",
        "fields": fields_dict,
        "tags": {"field": f"{field_name}", "average": "false"},
    }
    Logger.info(f"{device_influx_dict}")
    try:
        wrtite_result = influx_client.write_points([device_influx_dict])
        Logger.info(f"Finished wrtiting influx points with result: {wrtite_result} on field {field_name}")
        if wrtite_result:
            fields_dict = {}
    except Exception as e:
        Logger.info(f"Failed writing in Influx database error: {e}")


mqtt_client.on_message = on_message_mqtt
mqtt_client.connect(
    host=mqtt_config.HOST,
    port=mqtt_config.PORT,
    keepalive=mqtt_config.KEEPALIVE,
)
result, mid = mqtt_client.subscribe(f"{project_name}/{field_name}/#", 0)
Logger.info(f"Subscription result: {result}, {mid}")
mqtt_client.loop_start()

while True:
    time.sleep(10)
    if not mqtt_client.is_connected():
        mqtt_client.reconnect()

    write_influx_data()
