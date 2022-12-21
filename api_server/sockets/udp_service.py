import socket
import threading
import json
import time
from utils.logger import Logger

data_loc = {}
data_raw = {}
online_device = {}


class UdpService:

    def __init__(self, ip, port, db_connector, bm):
        self.Logger = Logger
        self.ip = ip
        self.port = port
        self.bm = bm
        # udp connection
        try:
            udp_threading = threading.Thread(target=self.server_udp)
            udp_threading.start()
            self.Logger.info('[udp] connection up!')
        except socket.error as e:
            self.Logger.error(e)
        # db connection
        try:
            self.db = db_connector.DataBaseConnector()
            self.Logger.info('[database] connection up!')
        except Exception as e:
            self.Logger.error(e)

    # set up udp server
    def server_udp(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.bind((self.ip, self.port))
        while True:
            try:
                content, dest_info = udp_socket.recvfrom(2048)
                raw_data = content.decode()
                self.decoder(raw_data)
            except Exception as e:
                self.Logger.error("[decoder] = " + str(raw_data))

    # decode raw data
    def decoder(self, raw_data):
        # data = list(map(eval, raw_data[1:(len(raw_data) - 1)].split(', ')))
        data = list(raw_data[1:(len(raw_data) - 1)].split(', '))
        if data[0] == '1':
            # receiving raw
            data[0] = int(data[0])
            data[1] = int(data[1])
            data[2] = float(data[2])
            data[3] = str(data[3][1:18])
            data[4] = int(data[4])
            data[5] = int(float(data[5]))
            self.bm.send_to_monitor(data)
            try:
                self.db.insert_raw_data(data)
            except:
                self.Logger.error('[insert_raw_data error] = ' + str(data))
            self.Logger.info('[data] = ' + str(data))
            res_raw = {
                "device": data[1],
                "vm": data[2],
                "ts": data[5]
            }
            data_raw[data[1]] = res_raw

        elif data[0] == '2':
            # receiving location
            data[0] = int(data[0])
            data[1] = int(data[1])
            data[2] = float(data[2])
            data[3] = float(data[3])
            data[4] = float(data[4])
            data[5] = float(data[5])
            data[6] = float(data[6])
            data[7] = int(data[7])
            data[8] = int(float(data[8]))
            try:
                self.db.insert_raw_val(data)
            except:
                self.Logger.error('[insert_raw_val error] = ' + str(data))
            self.Logger.info('[data] = ' + str(data))
            res_loc = {
                "device": data[1],
                "vm":    data[2],
                "loc_x": data[3],
                "loc_y": data[4],
                "val_x": abs(data[5]),
                "val_y": abs(data[6]),
                "alarm": data[7],
                "ts": data[8]
            }
            data_loc[data[1]] = res_loc
        elif data[0] == '0':
            data[0] = int(data[0])
            data[1] = int(data[1])
            data[2] = float(data[2])
            self.Logger.info('[data] = ' + str(data))
            res_online = {
                "device": data[1],
                "vm": data[2],
                "ts": int(time.time() * 1000)
            }
            online_device[data[1]] = res_online


# checking offline device
def get_loc_result():
    loc_result_ = get_online_data(data_loc)
    loc_result = {
        'loc': []
    }
    for device in loc_result_:
        loc_result['loc'].append(device)
    return json.dumps(loc_result)


# return status
def get_status():
    status = {
        "heart": get_online_data(online_device),
        "raw": get_online_data(data_raw),
        "loc": get_online_data(data_loc)
    }
    return json.dumps(status)


# return online_device
def get_online_data(online_data):
    if len(online_data) > 0:
        temp_del = []
        for off in online_data:
            # print(time.time() * 1000, online_device[off][4], (time.time() * 1000 - online_device[off][4]))
            if (time.time() * 1000 - online_data[off]['ts']) > 10 * 1000:
                temp_del.append(off)
        for d in temp_del:
            del online_data[d]

    result = []
    if len(online_data) > 0:
        for item in online_data:
            result.append(online_data[item])
    return result