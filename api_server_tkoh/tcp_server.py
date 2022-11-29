from collections import defaultdict
import logging
from sockets.tcp import TCPServer
import json
import time
from threading import Thread, Lock
import requests
from utils.security import decrypt
from typing import Dict, Any, List, Tuple, Union
import traceback
import math
from functools import reduce
from config import *

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def dispatch_pi_msg(json_loadable_msg: bytes, ip_addr: Tuple[str, int]) -> Union[Dict, None]:
    def __eval_str(s):
        res = {}
        msg = eval(s)
        for k, v in msg.items():
            try:
                val = eval(v)
                # note: using this trick to skip some weird situation, e.g. when evaluate the event {'event_type': 'id_request'}
                if callable(val):
                    val = v
            except:
                val = v
            res[k] = val
        return res

    MSG_HANDLE_API = {'beacon':        ['update_beacon_status'],
                      # 'wifi':          [],
                      # 'imu':           ['update_imu_status'],
                      # 'log_msg':       ['update_daily_log'],
                      # 'system_status': ['update_sensor_running_status'],
                      'result_data':   ['update_target_loc'],
                      # 'id_request':    ['id_request'],
                      'beacon_power':    ['update_beacon_battery'],
                      }
    SENSOR_TYPE_MAPPING = {'1': 'imu', '2': 'wifi', '3': 'beacon'}

    msg_dict = json.loads(json_loadable_msg)
    # print(f"receive byte msg: {msg_dict}")
    responses = []
    for str_idx, encrypted_str in msg_dict.items():
        try:
            event = json.loads(decrypt(bytes(encrypted_str, encoding='utf-8')))
        except Exception as e:
            logging.error(f"unable to load msg", e)
            continue

        if isinstance(event, dict):
            pass
        elif isinstance(event, str):
            event = __eval_str(event)
        else:
            logging.error(f"receive event is complete, but it's not a string or dict", event)
            continue

        print(f"receive event: {event}")

        if '_event_type' in event:
            event_type = event['_event_type']
            if event_type == 'sensor_data':
                sensor_type_str = str(event['_value']['_data_type'])
                if sensor_type_str in SENSOR_TYPE_MAPPING:
                    sensor_name = SENSOR_TYPE_MAPPING[sensor_type_str]
                    redirect_api_names = MSG_HANDLE_API[sensor_name]
                else:
                    logging.warning(f"receive undefined event from {ip_addr}: {event}")
                    continue
            elif event_type in MSG_HANDLE_API:
                redirect_api_names = MSG_HANDLE_API[event_type]
            else:
                logging.warning(f"receive undefined event from {ip_addr}: {event}")
                continue

            try:
                for api_name in redirect_api_names:
                    # print(api_name)
                    response = requests.post(f'http://{SERVER_IP}:{FLASK_PORT}/{api_name}',
                                             json=event,
                                             auth=(INTERNAL_REQUEST_USERNAME, INTERNAL_REQUEST_PSW))
                    if response.status_code == 200 and 'event_type' in response.json():
                        assert type(response.json()) is dict
                        responses.append(response.json())
                        # print(f'[debug] server receive id_request event and receive response = {response.json()}')
            except Exception as e:
                logging.error(f"unable to send msg to flask")
                
        else:
            logging.error(f"event has no 'event_type' key", event)


def run_tcp_server(server_ip, server_port):
    def __handle_client(tcp_server, msgs, addr):
        try:
            responses = dispatch_pi_msg(msgs, addr)
        except Exception as e:
            print(e)
            print(f"receive weird msg = {msgs}")

    tcp_server = TCPServer(ip=server_ip, port=server_port)
    tcp_server.start()
    while True:
        try:
            msgs, addr = tcp_server.receive()
            assert msgs is not None
            Thread(target=__handle_client, args=(tcp_server, msgs, addr)).start()
        except Exception as e:
            # note: don't close the connection even if the msg is weird, potential bug
            print(traceback.format_exc())


if __name__ == '__main__':
    Thread(target=run_tcp_server, args=(SERVER_IP, TCP_PORT)).start()
