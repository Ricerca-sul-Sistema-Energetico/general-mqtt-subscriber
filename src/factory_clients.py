import json
from typing import Dict
from paho.mqtt.client import Client as MqttClient  # type: ignore
from read_config import (
    mqtt_config,
    influx_config,
    Logger,
    project_name,
    field_name,
)

from funcs.handlers import on_disconnect_mqtt, on_connect_mqtt
from influxdb import InfluxDBClient


try:
    if any(value is None for value in mqtt_config):
        mqtt_client = None
        Logger.info("MQTT client is None for this project")
    else:
        mqtt_client = MqttClient(
            client_id=f"{project_name}_{field_name}_{mqtt_config.TYPE}",
            clean_session=True,
        )
        mqtt_client.username_pw_set(username=mqtt_config.USER, password=mqtt_config.PASSWORD)

        mqtt_client.on_connect = on_connect_mqtt
        mqtt_client.on_disconnect = on_disconnect_mqtt


except Exception as e:
    Logger.error(f"Could not connect MQTT client. Info: {e}")
    Logger.info("Influx client is None for this project")


try:
    if any(value is None for value in influx_config):
        influx_client = None
        Logger.info("Influx client is None for this project")

    else:
        Logger.info("Ready to istantiate influx client")
        influx_client = InfluxDBClient(
            host=influx_config.HOST,
            port=influx_config.PORT,
            username=influx_config.USER,
            password=influx_config.PASSWORD,
        )
        lst = influx_client.get_list_database()
        check = next((item for item in lst if item["name"] == influx_config.DATABASE), None)
        if len(lst) == 0 or check is None:
            influx_client.create_database(influx_config.DATABASE)
        influx_client.switch_database(influx_config.DATABASE)
        Logger.info(f"Influx client created, database selected: {influx_client._database}")
except Exception as e:
    Logger.error(f"Could not connect influxdb client. Info: {e}")
