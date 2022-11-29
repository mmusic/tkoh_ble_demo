from enum import Enum, unique, EnumMeta
import os
from pathlib import Path
from collections import namedtuple

# [FOLDER_PATH]
ROOT_FOLDER = Path(os.fspath(__file__)).parent.parent
CONFIG_FOLDER = f"{ROOT_FOLDER}/config"
CORE_FOLDER = f"{ROOT_FOLDER}/core"
UTILS_FOLDER = f"{ROOT_FOLDER}/utils"
LOG_FOLDER = f"{ROOT_FOLDER}/backup/log"


# note: set up which component to debug
COMPONENT_SETTING = namedtuple("COMPONENT_SETTING", ['on', 'debug'])
TO_LOAD_MODULES = {"backup.backup": False,
                   "estimator.estimator": True,
                   "sensors.sensor_manager": False,
                   "network.network": False,
                   "hci.hci": False,
                   "monitor.system_monitor": False,
                   "api.apiserver": False,
                   "sniffer.sniffer_mqtt": False,
                   "sniffer.sniffer_tcp": True,


                   "test.mock.mock_backup.mock_backup": False,
                   "test.mock.mock_estimator.mock_estimator": False,
                   "test.mock.mock_sensors.mock_sensor_manager": False,
                   "test.mock.mock_network.mock_network": False,
                   "test.mock.mock_hci.mock_hci": False,
                   "test.mock.mock_monitor.mock_system_monitor": False,

                   "utils.debug": False
                   }


# [SERVICE ID]
SERVICE_UUID = "7045de25939e4c3b96174e143f3c78fd"  # todo: TKOH

# [SERVER]
# SERVER_IP = '143.89.49.63'
# SERVER_PORT = 4000
# SERVER_USR = "hkust-mtr-service"
# SERVER_PWD = "mtrec2020"
SERVER_IP = '143.89.49.63'
SERVER_PORT = 5000
SERVER_USR = "hkust-mtr-service"
SERVER_PWD = "mtrec2020"

# [LOCAL DATABASE]
DATABASE_NAME = "on-board-program.db"
DATABASE_FILE_PATH = f"{LOG_FOLDER}/{DATABASE_NAME}"
DATABASE_TABLE_NAME = "temp"

# [NETWORK]
UPLOAD_FREQ = 2
UPLOAD_TIMEOUT = 2

# [API SERVER]
API_SERVER_IP = '192.168.10.162'
API_SERVER_PORT = 5000
API_SERVER_DEBUG = True

# [MQTT CLIENT]
MQTT_SERVER_IP = '192.168.1.252'  # tkoh  # todo: change to tkoh local ip
MQTT_SERVER_PORT = 1883
MQTT_SERVER_TOPICS = [('BL-01', 0), ('BL-02', 0), ('BL-03', 0), ('BL-04', 0), ('BL-05', 0), ('BL-06', 0), ('BL-07', 0),
                      ('BL-08', 0), ('BL-09', 0), ('BL-10', 0), ('BL-11', 0), ('BL-12', 0), ('BL-13', 0), ('BL-14', 0),
                      ('BL-15', 0), ('BL-16', 0), ('BL-17', 0), ('BL-18', 0), ('BL-19', 0), ('BL-20', 0), ('BL-21', 0),
                      ('BL-22', 0), ('BL-23', 0), ('BL-24', 0), ('BL-25', 0), ('BL-26', 0), ('BL-27', 0), ('BL-28', 0),
                      ('BL-29', 0), ('BL-30', 0), ('BL-31', 0), ('BL-32', 0), ('BL-33', 0), ('BL-34', 0), ('BL-35', 0),
                      ('BL-36', 0), ('BL-37', 0), ('BL-38', 0), ('BL-39', 0), ('BL-40', 0), ('BL-41', 0), ('BL-42', 0),
                      ('BL-43', 0),
                      ]  # note: the number at the back is qos
# MQTT_SERVER_IP = '192.168.10.112'  # lab
# MQTT_SERVER_PORT = 1884
# MQTT_SERVER_TOPICS = [('BL-01', 0), ('BL-02', 0), ('BL-03', 0), ('BL-04', 0), ('BL-05', 0), ('BL-06', 0), ('BL-07', 0),
#                       ('BL-08', 0), ('BL-09', 0), ('BL-10', 0), ('BL-11', 0), ('BL-12', 0), ('BL-13', 0), ('BL-14', 0),
#                       ('BL-15', 0), ('BL-16', 0), ('BL-17', 0), ('BL-18', 0), ('BL-19', 0), ('BL-20', 0), ('BL-21', 0),
#                       ('BL-22', 0), ('BL-23', 0), ('BL-24', 0), ('BL-25', 0), ('BL-26', 0), ('BL-27', 0), ('BL-28', 0),
#                       ('BL-29', 0), ('BL-30', 0), ('BL-31', 0), ('BL-32', 0), ('BL-33', 0), ('BL-34', 0), ('BL-35', 0),
#                       ('BL-36', 0), ('BL-37', 0), ('BL-38', 0), ('BL-39', 0), ('BL-40', 0), ('BL-41', 0), ('BL-42', 0),
#                       ('BL-43', 0),
#                       ]  # note: the number at the back is qos



# [HARDWARE INFO]
# BLE_MAC_ADDR = get_ble_mac(default_return_value=None)

# [SOFTWARE INFO]
VM = 1.0

# note: it should have a site(e.g. KOB, same name as the config/{site}.py file name) before deployment.
SENSOR_SITE = 'TKOH'

if __name__ == "__main__":
    pass
