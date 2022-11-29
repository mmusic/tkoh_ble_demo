import paho.mqtt.client as mqtt
import time
import json
import datetime
import csv

from multiprocessing.connection import Client
from array import array

import socket
import zlib

f = open('survey.csv', 'a')
f_csv = csv.writer(f)

T_SRV = '143.89.49.63'
T_PORT = 4440
pkg_window = 50
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect((T_SRV, T_PORT))
except Exception as e:
    print('e:', e)
    # pass

class MqttClient:
    def __init__(self, server_ip, server_port, server_topic):
        self.address = ('localhost', 6060)  # family is deduced to be 'AF_INET'
        self.client_conn_flag = False
        try:
            self.client_conn = Client(self.address)
            self.client_conn_flag = True
        except:
            print('error')
            # pass
        self.topic = []
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_topic = server_topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        # Connect to Mqtt server
        self.client.connect(self.server_ip, self.server_port, 600)
        # Subscribe multi topic
        # self.client.publish("data/send", payload='param', qos=2)
        self.t1 = time.time()
        for topic in self.server_topic:
            self.client.subscribe(topic, qos=0)
        self.client.loop_forever()



    def on_disconnect(self, userdata, rc):
        print('disconnect')

    def on_log(self, obj, level, string):
        print(string)

    def on_connect(self, mqtt_client, obj, flags, rc):
        # TODO add logger
        print("Connected with result code " + str(rc))

    def on_message(self, mqtt_client, userdata, msg):
        arr_time = time.time()
        #print(msg.payload)
        res = json.loads(msg.payload)['raw']
        data = {
            'topic': msg.topic,
            'data': '',
            'timestamp': arr_time
        }
        beacon_list = res.split(',')
        # print(msg.topic, len(beacon_list), round(t_arr, 2))
        # print('----', msg.payload)
        new_pf = []
        beacons_90 = []
        for beacon in beacon_list:
            #if msg.topic == 'BL-02':
                #print(msg.topic, time.time())
            # if len(beacon) == 90:
            if 'f000aab004514'.upper() in beacon or '771f4541e1be43'.upper() in beacon:
                beacons_90.append(beacon)
                rssi = int(beacon[88:90], 16) - 0x100
                uuid = beacon[46:86]
                # print(msg.topic, rssi, uuid, time.time())
                # new_pf.append([msg.topic, rssi, uuid, time.time()])
                # if '7045de25939e4'.upper() in beacon:
                #     new_pf.append([msg.topic, rssi, uuid, time.time()])
                    # beacons_90.append(beacon)
                    # print(msg.topic,rssi)
                # print(msg.topic,rssi)
                # print(msg.topic, beacon, len(beacon), datetime.datetime.now(), msg.qos, rssi, len(beacon_list))
            if '7045DE25'.upper() in beacon:
                rssi = int(beacon[88:90], 16) - 0x100
                uuid = beacon[46:86]
                new_pf.append([msg.topic, rssi, uuid, time.time()])
                print(msg.topic, rssi, time.time(), beacon)
                f_csv.writerow([msg.topic, rssi, time.time(), beacon])
                f.flush()
        data['data'] = beacons_90

        if len(data['data']):
            # print(data)
            try:
                self.client_conn.send(data)
                print(data)
            except:
                self.client_conn_flag = False
            if not self.client_conn_flag:
                try:
                    self.client_conn = Client(self.address)
                    self.client_conn_flag = True
                except:
                    pass
        if len(new_pf):

            b = json.dumps(new_pf).encode('utf-8')
            # print(b)
            compressed_data = zlib.compress(b)
            # compressed_data += b'/'
            try:
                sock.sendall(compressed_data)
            except Exception as e:
                print(e)
                try:
                #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #     sock.settimeout(2)
                    sock.connect((T_SRV, T_PORT))
                except Exception as e:
                    print('e:', e)


if __name__ == "__main__":
    # make sure that sgwireless has open the mqtt server, otherwise we won't be able to receive any data
    BL_TOPIC = []
    for i in range(43):
        index = i + 1
        if index < 10:
            index = '0' + str(index)
        BL_TOPIC.append('BL-' + str(index))
    mqtt_client = MqttClient(server_ip='192.168.1.252', server_port=1883, server_topic=BL_TOPIC)  # loop forever in this line
