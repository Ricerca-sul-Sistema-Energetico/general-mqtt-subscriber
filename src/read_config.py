import os
import logging
from collections import namedtuple
from dotenv import dotenv_values
from typing import List


def get_logger(logger_name: str, level: str | None = "DEBUG"):
    """
    :param logger_name: the name of the module (or method) where the logger was executed
    :param level: the logger level
    :return: the logger object
    """
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler()  # handler for output messages on stdout
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


MqttConfig = namedtuple("MqttConfig", "USER, PASSWORD, HOST, PORT, KEEPALIVE, TYPE")
InfluxConfig = namedtuple("InfluxConfig", "USER, PASSWORD, HOST, PORT, DATABASE")

env_values = dotenv_values()


project_name: str = env_values.get("PROJECT_NAME", None)  # type: ignore
field_name: str = env_values.get("FIELD_NAME", None)  # type: ignore

mqtt_config = MqttConfig(
    HOST=env_values.get("MQTT_HOST", None),
    PORT=int(env_values.get("MQTT_PORT", 1883)),  # type: ignore
    USER=env_values.get("MQTT_USER", None),
    PASSWORD=env_values.get("MQTT_PWD", None),
    KEEPALIVE=int(env_values.get("MQTT_KEEPALIVE", 60)),  # type: ignore
    TYPE=env_values.get("MQTT_TYPE", "subscriber"),
)

influx_config = InfluxConfig(
    HOST=env_values.get("INFLUX_HOST", None),
    PORT=int(env_values.get("INFLUX_PORT", 8086)),  # type: ignore
    DATABASE=(env_values.get("INFLUX_DATABASE", None)),  # type: ignore
    USER=env_values.get("INFLUX_USER", None),
    PASSWORD=env_values.get("INFLUX_PWD", None),
)

Logger = get_logger(logger_name="MQTT subscriber", level=env_values.get("LOG_LEVEL", "DEBUG"))
Logger.info(" Launching modbus application ...")
