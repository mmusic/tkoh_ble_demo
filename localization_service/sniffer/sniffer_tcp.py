import os
from sniffer.beacon_parser import TKOHBeaconParser
from config.common import MQTT_SERVER_TOPICS, MQTT_SERVER_PORT, MQTT_SERVER_IP
from config.TKOH import SOURCE_INFO_DICT
from common.component import Component
from common.data_type import *
from common.event import *
from pprint import pprint
import re
from threading import Thread
from multiprocessing.connection import Listener

address = ('localhost', 6060)


class Sniffer(Component):
    def __init__(self):
        super().__init__()

        self.add_event_publisher(SensorEvent._event_type)
        self.add_event_publisher(LogEvent._event_type)
        self.add_event_publisher(BeaconPowerEvent._event_type)

        self.server = Listener(address)

    def start(self):
        Thread(target=self.on_receive_sensor_data_from_socket).start()
        pid = str(os.getpid())
        # self.publish(LogEvent(identifier=pid, value=LogMessage(level='info', msg=f"subscribe topics: {self.server_topic}")))
        self.publish(LogEvent(identifier=pid, value=LogMessage(level='info', msg=f"server: {address}")))

    def on_receive_sensor_data_from_socket(self):
        # note: can only handle single client
        while True:
            conn = self.server.accept()
            with conn:
                while True:
                    try:
                        data = conn.recv()
                    except Exception as err:
                        break
                    try:
                        self.on_message(msg=data)
                    except Exception as err:
                        self.publish(LogEvent(identifier=str(os.getpid()),
                                              value=LogMessage(level='error', msg=f"Sniffer.on_message error: {err}")))

    def on_message(self, msg):
        source_ident = msg['topic']
        data = msg['data']
        #ts = msg['timestamp']
        ts = time.time()
        #print(f'receive data ts from tcp = {ts}')
        # print(time.time(), source_ident, decode_msg)

        for pack in data:
            pack = pack.lower()
            if len(pack) == 90:
                # print(pack)
                try:
                    beacon_value = TKOHBeaconParser.get_beacon_value(pack, mac=None, rssi=None)
                    # print(beacon_value)
                except Exception as err:
                    continue
                else:
                    try:
                        if beacon_value.battery is None:
                            e = SensorEvent(identifier=source_ident,
                                            value=BeaconDataPackage(target_identifier=f'{beacon_value.uuid}{beacon_value.major}{beacon_value.minor}',
                                                                    value=beacon_value,
                                                                    timestamp=ts,
                                                                    source=SourceInfo(source_identifier=source_ident,
                                                                                      source_pos=Position(x=SOURCE_INFO_DICT[source_ident].x,
                                                                                                          y=SOURCE_INFO_DICT[source_ident].y,
                                                                                                          z=SOURCE_INFO_DICT[source_ident].z,
                                                                                                          timestamp=-1,
                                                                                                          pos_type=SOURCE_INFO_DICT[source_ident].type,
                                                                                                          )
                                                                                      ),
                                                                    ))
                            self.publish(e)  # using topic name as sniffer identifier
                        else:
                            self.publish(BeaconPowerEvent(timestamp=ts,
                                                          identifier=beacon_value.beacon_mac,
                                                          value=beacon_value,
                                                          source_identifier=source_ident,))
                    except Exception as err:
                        print(err)
