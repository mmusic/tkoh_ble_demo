import flask
from flask import make_response, request, jsonify
import utils.db_connector as db_connector
from collections import defaultdict
import logging
from sockets.tcp import TCPServer
import json
import time
from threading import Thread, Lock
import requests
from utils.security import decrypt
import sqlite3
from typing import Dict, Any, List, Tuple, Union
import traceback
import math
from functools import reduce
from config import *

app = flask.Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

METER_TO_LAT_LON_SCALE_FACTOR = 1 / 111_194.926644

def _particle_within_range(pos: Tuple[float, float, float],
                           polygon: List[Tuple[float, float, float]]) -> bool:
    # todo: not 3d checking
    # todo: should at least consider polygon in different floors
    floor = pos[2]
    if floor != polygon[0][2]:
        return False

    res = False

    p1, p2, p3, p4 = polygon
    p1_p2_cross_product_p1_p = (p1[0] - p2[0]) * (p1[1] - pos[1]) - (p1[1] - p2[1]) * (p1[0] - pos[0])
    p3_p4_cross_product_p3_p = (p3[0] - p4[0]) * (p3[1] - pos[1]) - (p3[1] - p4[1]) * (p3[0] - pos[0])

    p1_p4_cross_product_p1_p = (p1[0] - p4[0]) * (p1[1] - pos[1]) - (p1[1] - p4[1]) * (p1[0] - pos[0])
    p3_p2_cross_product_p3_p = (p3[0] - p2[0]) * (p3[1] - pos[1]) - (p3[1] - p2[1]) * (p3[0] - pos[0])
    res |= (p1_p2_cross_product_p1_p * p3_p4_cross_product_p3_p >= 0) and (p1_p4_cross_product_p1_p * p3_p2_cross_product_p3_p >= 0)
    return res


class MOCKDATABASE:
    class Collection:
        def __init__(self, db_file_path, table_name):
            self.db_file_path = db_file_path
            self.table_name = table_name
            self.__create_table(self.table_name)

        def insert_one(self, json_data: Dict[str, Any]) -> int:
            __db_conn = sqlite3.connect(database=self.db_file_path)
            c = __db_conn.cursor()
            c.execute(f'INSERT INTO {self.table_name} (data) VALUES (?)', (json.dumps(json_data), ))
            lastrowid = c.lastrowid
            __db_conn.commit()
            __db_conn.close()
            return lastrowid

        def insert_many(self, json_data_list: List[Dict[str, Any]]):
            __db_conn = sqlite3.connect(database=self.db_file_path)
            ids = []
            c = __db_conn.cursor()
            for json_data in json_data_list:
                c.execute(f'INSERT INTO {self.table_name} (data, ) VALUES (?,)', (json.dumps(json_data), ))
                ids.append(c.lastrowid)
            __db_conn.commit()
            __db_conn.close()
            return ids

        def find_one(self, json_data=None) -> Dict[str, Any]:
            pass

        def find(self, json_data=None) -> List[Dict[str, Any]]:
            pass

        def __create_table(self, table_name):
            # print(table_name)
            __db_conn = sqlite3.connect(database=self.db_file_path)
            c = __db_conn.cursor()
            sql_create_temp_table = f" CREATE TABLE IF NOT EXISTS {table_name} ( \
                                            id integer PRIMARY KEY autoincrement,\
                                            data json NOT NULL \
                                        ); "
            c.execute(sql_create_temp_table)
            __db_conn.commit()
            __db_conn.close()

        def __str__(self):
            return self.table_name

    def __init__(self, file_path):
        self.db_file_path = file_path
        self.__db_conn = sqlite3.connect(database=file_path)
        self.__db_table_list = [self.Collection(self.db_file_path, name) for name in self.list_collection_names()]

    def list_collection_names(self) -> list:
        c = self.__db_conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_list = c.fetchall()
        # print(table_list)
        return [name_tuple[0] for name_tuple in table_list if name_tuple[0] != 'sqlite_sequence']

    def __getitem__(self, item):
        for table in self.__db_table_list:
            if str(table) == item:
                return table
        # print(f"create table {item}")
        new_table = self.Collection(self.db_file_path, item)
        self.__db_table_list.append(new_table)
        return new_table


class Cache:
    __data_loc = defaultdict(dict)  # note: {sensor_ble_mac:{vm,hci_status(arr),loc_x,loc_y,loc_z,vel_x,vel_y,vel_z,alarm_flag,location_ts,heartbeat_ts}}
    __data_raw = defaultdict(dict)  # note: {major_minor: {vm, mac, ts, rssi, sensor_ble_mac}}
    __data_battery = defaultdict(dict)  # note: {major_minor: {vm, mac, ts, rssi, sensor_ble_mac}}
    __data_battery_id = defaultdict(dict)  # note: {major_minor: {vm, mac, ts, rssi, sensor_ble_mac}}baeet
    __beacons = defaultdict(dict)
    try:
        __db_conn = db_connector.DataBaseConnector(**DB_CONNECT_INFO)
        # ble_mac_registration_table = {}
        # for idx, sensor, site, label, ts_create in __db_conn.query_full_table('sensor', 'id', 'sensor', 'site', 'label', 'ts_create'):
        #     ble_mac_registration_table[sensor] = {'id': idx,
        #                                           'sensor': sensor,
        #                                           'site': site,
        #                                           'label': label,
        #                                           'ts_create': ts_create, }
    except:
        logging.error(traceback.format_exc())
        logging.error("Unable to connect to database, terminate the whole API Server")
        exit(0)

    # for local test
    # __mock_db = MOCKDATABASE("./logs/mtr-server.db")

    __loc_lock = Lock()
    __raw_lock = Lock()
    __data_battery_lock = Lock()
    __registration_table_lock = Lock()
    __history_vel_norm = {}

    @classmethod
    def init(cls):
        s_ts = int(time.time() - 1 * 24 *60 * 60)
        print('all_targets_last_seen_status')
        for target_identifier, vm, pos_x, pos_y, pos_z, ts in cls.__db_conn.all_targets_last_seen_status(s_ts):
            for polygon_idx, polygon in MAPS.items():
                if _particle_within_range((pos_x / METER_TO_LAT_LON_SCALE_FACTOR, pos_y / METER_TO_LAT_LON_SCALE_FACTOR, pos_z), polygon):
                    cls.__data_loc[target_identifier] = {'loc_x': pos_x, 'loc_y': pos_y, 'loc_z': pos_z, 'location_ts': ts, 'vm': vm, 'zone': polygon_idx}
        print('all_targets_last_seen_battery')
        # for beacon, battery, ts, in cls.__db_conn.all_targets_last_seen_battery(s_ts):
        #     cls.__data_battery[beacon] = {'battery': battery, 'ts': ts}
        print(time.time() - s_ts + 0.5 * 24 *60 * 60)
        for idx, major, minor, uuid, beacon, vendor in cls.__db_conn.all_beacons():
            _major = hex(major)[2:]
            if len(_major) < 4:
                count_0 = 4 - len(_major)
                for i in range(count_0):
                    _major = '0' + _major
            _minor = hex(minor)[2:]
            if len(_minor) < 4:
                count_0 = 4 - len(_minor)
                for i in range(count_0):
                    _minor = '0' + _minor
            beacon_identify = uuid.lower() + _major + _minor
            if beacon == '0':
                _beacon_identify = _major + _minor
            else:
                _beacon_identify = beacon.lower()
            cls.__data_battery_id[_beacon_identify] = {'beacon_identify': beacon_identify}

    # @classmethod
    # def keep_update_sensor_registration_table(cls):
    #     pass
    #     # while True:
    #     #     new_table = {}
    #     #     for idx, sensor, site, label, ts_create in cls.__db_conn.query_full_table('sensor', 'id', 'sensor', 'site', 'label', 'ts_create'):
    #     #         new_table[sensor] = {'id': idx,
    #     #                              'sensor': sensor,
    #     #                              'site': site,
    #     #                              'label': label,
    #     #                              'ts_create': ts_create, }
    #     #         cls.ble_mac_registration_table.update(new_table)
    #     #         time.sleep(60)

    # todo
    @classmethod
    def update_beacon_status(cls, data, *args, **kwargs):
        # todo: insert beacon data
        # store and refresh
        if data['_value']['_value']['_rssi']:
            # pass
            sensor_label = data['_identifier']
            signal_receive_ts = data['_timestamp']
            vm = float(data['vm'])
            beacon_mac = data['_value']['_value']['_beacon_mac']
            rssi = int(data['_value']['_value']['_rssi'])

            major = data['_value']['_value']['_major']
            minor = data['_value']['_value']['_minor']
            uuid = data['_value']['_value']['_uuid']

        # with cls.__raw_lock:
        #     beacon_info = cls.__data_raw[beacon_major_minor]
        #     beacon_info['sensor_ble_mac'] = ble_mac
        #     beacon_info['vm'] = vm
        #     beacon_info['mac'] = beacon_mac
        #     beacon_info['ts'] = signal_receive_ts
        #     beacon_info['rssi'] = rssi

        # beacon_signal_table = cls.__mock_db['beacon_signal']
        # beacon_signal_table.insert_one(data)
        # cls.__db_conn.insert_beacon_scan_data(vm=vm,
        #                                       beacon=beacon_mac,
        #                                       major=major,
        #                                       minor=minor,
        #                                       rssi=rssi,
        #                                       ts=signal_receive_ts,
        #                                       sensor_label=sensor_label,
        #                                       uuid=uuid,
        #                                       )

    @classmethod
    def update_sensor_location(cls, data, *args, **kwargs):
        # store and refresh
        # print(data)
        ble_mac = data['_identifier']
        location_ts = float(data['_timestamp'])
        vm = float(data['vm'])
        loc_x, loc_y, loc_z = float(data['_value']['_x']), float(data['_value']['_y']), int(data['_value']['_z'])

        # if '06360070' in ble_mac:
        #     print(data)

        with cls.__loc_lock:
            for polygon_idx, polygon in MAPS.items():
                p1, p2, p3, p4 = polygon
                floor = p1[2]
                sensor_location = cls.__data_loc[ble_mac]
                sensor_location['location_ts'] = location_ts
                if int(floor) == int(loc_z) and _particle_within_range((loc_x, loc_y, loc_z), polygon):
                    # note: from meter to lat_long
                    loc_x = loc_x * METER_TO_LAT_LON_SCALE_FACTOR
                    loc_y = loc_y * METER_TO_LAT_LON_SCALE_FACTOR
                    sensor_location['vm'] = vm
                    sensor_location['loc_x'] = loc_x  
                    sensor_location['loc_y'] = loc_y
                    sensor_location['loc_z'] = loc_z    # sensor_location['vel_x'] = vel_x
                    sensor_location['zone'] = polygon_idx  # sensor_location['vel_x'] = vel_x
                    # sensor_location['vel_y'] = vel_y
                    # sensor_location['vel_z'] = vel_z
                    # sensor_location['alarm_flag'] = alarm_flag
                    # cur_vel_norm = math.sqrt(vel_x ** 2 + vel_y ** 2 + vel_z ** 2)
                    # cls.__update_history_vel_cache(ble_mac, round(cur_vel_norm, 2))
                    break

        # sensor_location_table = cls.__mock_db['sensor_location']
        # sensor_location_table.insert_one(data)
        # cls.__db_conn.insert_sensor_loc(ts=location_ts,
        #                                 vm=vm,
        #                                 pos_x=loc_x,
        #                                 pos_y=loc_y,
        #                                 pos_z=loc_z,
        #                                 sensor=ble_mac,
        #                                 )

    @classmethod
    def update_beacon_battery(cls, data, *args, **kwargs):
        # store and refresh

        battery_ts = float(data['_timestamp'])
        battery = data['_value']['_battery']
        sensor_label = data['_source_identifier']

        if data['_value']['_major'] is not None and data['_value']['_minor'] is not None:
            ble_mac = data['_value']['_major'] + data['_value']['_minor']
        else:
            ble_mac = data['_identifier']
        try:
            # print('battery', sensor_label, battery, ble_mac)
            beacon = cls.__data_battery_id[ble_mac]['beacon_identify']
            beacon_battery = cls.__data_battery[beacon]

            with cls.__data_battery_lock:
                beacon_battery['ts'] = battery_ts
                beacon_battery['battery'] = battery

            cls.__db_conn.insert_beacon_battery(ts=battery_ts,
                                                battery=battery,
                                                beacon=beacon,
                                                sensor_label=sensor_label)
        except Exception as e:
            # no registerd beacon
            # print(e)
            pass



    @classmethod
    def __update_history_vel_cache(cls, ble_mac, vel_norm):
        if ble_mac not in cls.__history_vel_norm:
            cls.__history_vel_norm[ble_mac] = [0.] * 10
        cls.__history_vel_norm[ble_mac].append(vel_norm)
        cls.__history_vel_norm[ble_mac].pop(0)


    # @classmethod
    # def store_logs(cls, log_msg):
    #     ts = log_msg['timestamp']
    #     level = log_msg['level']
    #     msg = log_msg['msg']
    #     # logs_table = cls.__mock_db['logs']
    #     # logs_table.insert_one(log_msg)
    #     cls.__db_conn.insert_log(ts=ts,
    #                              src_type='sensor',
    #                              content=str(log_msg),
    #                              level=level,
    #                              )

    @classmethod
    def get_latest_target_status(cls, *args, **kwargs):
        res = []
        with cls.__loc_lock:
            for target_identifier, v in cls.__data_loc.items():
                try:
                    res.append({"target": target_identifier,
                            "loc_x": v['loc_x'],
                            "loc_y": v['loc_y'],
                            "loc_z": int(v['loc_z']),
                            "ts": int(v['location_ts']),
                            "zone": int(v['zone'])},)
                except Exception as e:
                    pass
                
            return res

    @classmethod
    def get_latest_target_battery(cls, *args, **kwargs):
        res = []
        with cls.__data_battery_lock:
            for target_identifier, v in cls.__data_battery.items():
                res.append({"target": target_identifier,
                            "battery": v['battery'],
                            "ts": int(v['ts'])}, )
            return res

    @classmethod
    def get_history_target_status(cls, target_identifier, s_ts, e_ts):
        res = []
        for target_identifier, loc_x, loc_y, loc_z, ts in cls.__db_conn.query_history_target_status(target_identifier, s_ts, e_ts):
            for polygon_idx, polygon in MAPS.items():
                if _particle_within_range((loc_x / METER_TO_LAT_LON_SCALE_FACTOR, loc_y / METER_TO_LAT_LON_SCALE_FACTOR, loc_z), polygon):
                    res.append({"target": target_identifier,
                                "loc_x": loc_x,
                                "loc_y": loc_y,
                                "loc_z": loc_z,
                                "ts": ts,
                                "zone": polygon_idx}, )
        return res

@app.route('/latest_sensor_status', methods=['get', 'post'])
def latest_sensor_status():
    result = Cache.get_latest_target_status()
    # logger.error(f'latest_sensor_status: {result}')
    res = make_response(jsonify(result))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return res

@app.route('/latest_sensor_battery', methods=['get', 'post'])
def latest_sensor_battery():
    result = Cache.get_latest_target_battery()
    # logger.error(f'latest_sensor_status: {result}')
    res = make_response(jsonify(result))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return res

@app.route('/history/<string:target_id>/<int:s_ts>/<int:e_ts>')
def hisotry_sensor_status(target_id, s_ts, e_ts):
    result = Cache.get_history_target_status(str(target_id), s_ts, e_ts)
    logger.error(f'hisotry_sensor_status: {result}')
    res = make_response(jsonify(result))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with, content-type'
    return res


@app.route('/update_target_loc', methods=['get', 'post'])
def update_target_loc():
    if request.authorization is not None and request.authorization['username'] == INTERNAL_REQUEST_USERNAME and request.authorization['password'] == INTERNAL_REQUEST_PSW:
        data = request.get_json()
        # print(f"receive sensor result: {data}")
        Cache.update_sensor_location(data)
        response = make_response(jsonify({"message": "success"}), 200)
        return response
    else:
        response = make_response(jsonify({"message": "fail"}), 200)
    return response


@app.route('/update_beacon_status', methods=['get', 'post'])
def update_beacon_status():
    if request.authorization is not None and request.authorization['username'] == INTERNAL_REQUEST_USERNAME and request.authorization['password'] == INTERNAL_REQUEST_PSW:
        beacon_data = request.get_json()
        # print(f"receive beacon_data: {beacon_data}")
        Cache.update_beacon_status(beacon_data)
        response = make_response(jsonify({"message": "success"}), 200)
    else:
        response = make_response(jsonify({"message": "fail"}), 200)
    return response

@app.route('/update_beacon_battery', methods=['get', 'post'])
def update_beacon_battery():
    if request.authorization is not None and request.authorization['username'] == INTERNAL_REQUEST_USERNAME and request.authorization['password'] == INTERNAL_REQUEST_PSW:
        beacon_power = request.get_json()
        # print(f"receive beacon_data: {beacon_power}")
        Cache.update_beacon_battery(beacon_power)
        response = make_response(jsonify({"message": "success"}), 200)
    else:
        response = make_response(jsonify({"message": "fail"}), 200)
    return response


# @app.route('/update_daily_log', methods=['get', 'post'])
# def update_daily_log():
#     if request.authorization is not None and request.authorization['username'] == INTERNAL_REQUEST_USERNAME and request.authorization['password'] == INTERNAL_REQUEST_PSW:
#         l = request.get_json()
#         print(f"receive log: {l}")
#         Cache.store_logs(l)
#         response = make_response(jsonify({"message": "success"}), 200)
#     else:
#         response = make_response(jsonify({"message": "fail"}), 200)
#     return response


def __mock_callback(callback, daemon=False):
    from utils.security import encrypt

    def __wrap(data: dict) -> dict:
        return {'0': (encrypt(json.dumps(str(data)).encode())).decode()}

    def __loop():
        import random
        time.sleep(2)
        mock_ip_addr = ('255.255.255.255', 255)
        idx = 0
        x_pos = 0
        x_pos1 = -30
        while True:
            alarm_flag = random.randint(0, 1)
            x_pos = (x_pos + 1) % 50
            x_pos1 = (x_pos1 + 1) % 50
            y_pos = random.randint(0, 3)
            x_vel, y_vel = random.randint(0, 20) / 10, random.randint(0, 20) / 10
            idx = (idx + 1) % 6
            mock_log_event = json.dumps(__wrap({'ble_mac': '00:00:00:00:00:00', 'vm': 1.0, 'event_type': 'log_msg', 'level': 'warn', 'msg': 'mock log_msg event', 'timestamp': str(time.time())})).encode()
            callback(mock_log_event, mock_ip_addr)
            mock_log_event = json.dumps(__wrap({'ble_mac': '11:11:11:11:11:11', 'vm': 1.0, 'event_type': 'log_msg', 'level': 'warn', 'msg': 'mock log_msg event', 'timestamp': str(time.time())})).encode()
            callback(mock_log_event, mock_ip_addr)
            mock_log_event = json.dumps(__wrap({'ble_mac': '22:22:22:22:22:22', 'vm': 1.0, 'event_type': 'log_msg', 'level': 'warn', 'msg': 'mock log_msg event', 'timestamp': str(time.time())})).encode()
            callback(mock_log_event, mock_ip_addr)
            time.sleep(0.5)
            mock_beacon_event = json.dumps(__wrap({'ble_mac': '11:11:11:11:11:11', 'vm': 1.0, 'event_type': 'sensor_data', 'sensor_type': '3', 'timestamp': str(time.time()), 'values': str(['100111000' + f"{random.randint(1, 9)}", 'xx:10:xx:bb:cc:dd', -88 + random.randint(0, 20)])})).encode()
            callback(mock_beacon_event, mock_ip_addr)
            mock_beacon_event = json.dumps(__wrap({'ble_mac': '00:00:00:00:00:00', 'vm': 1.0, 'event_type': 'sensor_data', 'sensor_type': '3', 'timestamp': str(time.time()), 'values': str(['100111000' + f"{random.randint(1, 9)}", 'yy:22:cc:zz:vv:bb', -88 + random.randint(0, 20)])})).encode()
            callback(mock_beacon_event, mock_ip_addr)
            mock_beacon_event = json.dumps(__wrap({'ble_mac': '33:33:33:33:33:33', 'vm': 1.0, 'event_type': 'sensor_data', 'sensor_type': '3', 'timestamp': str(time.time()), 'values': str(['100111000' + f"{random.randint(1, 9)}", 'yy:22:cc:zz:vv:bb', -88 + random.randint(0, 20)])})).encode()
            callback(mock_beacon_event, mock_ip_addr)
            mock_beacon_event = json.dumps(__wrap({'ble_mac': '44:44:44:44:44:44', 'vm': 1.0, 'event_type': 'sensor_data', 'sensor_type': '3', 'timestamp': str(time.time()), 'values': str(['100111000' f"{random.randint(1, 9)}", 'yy:22:cc:zz:vv:bb', -88 + random.randint(0, 20)])})).encode()
            callback(mock_beacon_event, mock_ip_addr)
            time.sleep(0.5)
            mock_result_event = json.dumps(__wrap({'ble_mac': '00:00:00:00:00:00', 'vm': 1.0, 'event_type': 'result_data', 'timestamp': str(time.time()), 'values': [x_pos + 1, y_pos, 0, x_vel, y_vel, 0, alarm_flag]})).encode()
            callback(mock_result_event, mock_ip_addr)
            mock_result_event = json.dumps(__wrap({'ble_mac': '11:11:11:11:11:11', 'vm': 1.0, 'event_type': 'result_data', 'timestamp': str(time.time()), 'values': [x_pos1  +1, y_pos, 0, x_vel, y_vel, 0, alarm_flag]})).encode()
            callback(mock_result_event, mock_ip_addr)
            mock_result_event = json.dumps(__wrap({'ble_mac': '22:22:22:22:22:22', 'vm': 1.0, 'event_type': 'result_data', 'timestamp': str(time.time()), 'values': [x_pos  +2, y_pos, 0, x_vel, y_vel, 0, alarm_flag]})).encode()
            callback(mock_result_event, mock_ip_addr)
            mock_result_event = json.dumps(__wrap({'ble_mac': '33:33:33:33:33:33', 'vm': 1.0, 'event_type': 'result_data', 'timestamp': str(time.time()), 'values': [x_pos  -2, y_pos, 0, x_vel, y_vel, 0, alarm_flag]})).encode()
            callback(mock_result_event, mock_ip_addr)
            mock_result_event = json.dumps(__wrap({'ble_mac': '44:44:44:44:44:44', 'vm': 1.0, 'event_type': 'result_data', 'timestamp': str(time.time()), 'values': [x_pos  +3, y_pos, 0, x_vel, y_vel, 0, alarm_flag]})).encode()
            callback(mock_result_event, mock_ip_addr)
            time.sleep(0.5)
            # hci_value = [1 if i == idx else 0 for i in range(6)]
            mock_system_status = json.dumps(__wrap({'ble_mac': '00:00:00:00:00:00', 'vm': 1.0, 'event_type': 'system_status', 'timestamp': str(time.time()), 'values': [1 if i == idx else 0 for i in range(6)]})).encode()
            callback(mock_system_status, mock_ip_addr)
            mock_system_status = json.dumps(__wrap({'ble_mac': '22:22:22:22:22:22', 'vm': 1.0, 'event_type': 'system_status', 'timestamp': str(time.time()), 'values': [1 if i == idx else 0 for i in range(6)]})).encode()
            callback(mock_system_status, mock_ip_addr)
            mock_system_status = json.dumps(__wrap({'ble_mac': '33:33:33:33:33:33', 'vm': 1.0, 'event_type': 'system_status', 'timestamp': str(time.time()), 'values': [1 if i == idx else 0 for i in range(6)]})).encode()
            callback(mock_system_status, mock_ip_addr)
            mock_system_status = json.dumps(__wrap({'ble_mac': '44:44:44:44:44:44', 'vm': 1.0, 'event_type': 'system_status', 'timestamp': str(time.time()), 'values': [1 if i == idx else 0 for i in range(6)]})).encode()
            callback(mock_system_status, mock_ip_addr)
            mock_system_status = json.dumps(__wrap({'ble_mac': '11:11:11:11:11:11', 'vm': 1.0, 'event_type': 'system_status', 'timestamp': str(time.time()), 'values': [1 if i == idx else 0 for i in range(6)]})).encode()
            callback(mock_system_status, mock_ip_addr)
    if daemon:
        Thread(target=__loop).start()
    else:
        __loop()


def __mock_api_request(daemon=False):
    def __loop():
        time.sleep(2)
        while True:
            response = requests.request(method='get', url=f'http://{SERVER_IP}:{FLASK_PORT}/latest_sensor_status')
            print(f"request from __mock_api_request latest_sensor_status {response.json()}")
            response = requests.request(method='get', url=f'http://{SERVER_IP}:{FLASK_PORT}/latest_beacon_status')
            print(f"request from __mock_api_request latest_beacon_status {response.json()}")
            time.sleep(0.5)
    if daemon:
        Thread(target=__loop).start()
    else:
        __loop()


if __name__ == '__main__':
    Cache.init()
    app.run(port=FLASK_PORT, debug=True, host=SERVER_IP)
