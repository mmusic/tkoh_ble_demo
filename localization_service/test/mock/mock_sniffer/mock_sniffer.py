# import paho.mqtt.client as mqtt
# import os
# from sniffer.beacon_parser import TKOHBeaconParser
# from config.common import MQTT_SERVER_TOPICS, MQTT_SERVER_PORT, MQTT_SERVER_IP
# from config.TKOH import SOURCE_INFO_DICT
# from common.component import Component
# from common.data_type import *
# from common.event import *
# from pprint import pprint
# import re
# from threading import Thread
#
#
# class Sniffer(Component):
#     def __init__(self):
#         super().__init__()
#
#         self.add_event_publisher(SensorEvent.event_type)
#         self.add_event_publisher(LogEvent.event_type)
#         self.add_event_publisher(BeaconPowerEvent.event_type)
#
#         self.server_ip = MQTT_SERVER_IP
#         self.server_port = MQTT_SERVER_PORT
#         self.server_topic = MQTT_SERVER_TOPICS
#
#         self.client = mqtt.Client()
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#         self.client.connect(self.server_ip, self.server_port, 600)  # blocking
#         self.client.subscribe(self.server_topic)
#
#     def start(self):
#         pid = str(os.getpid())
#         self.publish(LogEvent(identifier=pid, value=LogMessage(level='info', msg=f"subscribe topics: {self.server_topic}")))
#         self.publish(LogEvent(identifier=pid, value=LogMessage(level='info', msg=f"server: {self.server_ip}:{self.server_port}")))
#         self.client.loop_start()  # non-blocking
#
#     def on_connect(self, mqtt_client, obj, flags, rc):
#         # TODO add logger
#         print("Connected with result code " + str(rc))
#
#     def on_message(self, mqtt_client, userdata, msg):
#         decode_msg = eval(bytes(msg.payload).decode('utf-8'))
#         mqtt_client_recv_ts = time.time()
#         # print(time.time(), msg.topic, decode_msg)
#
#         packs = decode_msg['raw'].split(',')
#
#         for pack in packs:
#             pack = pack.lower()
#             if len(pack) == 90:
#                 try:
#                     beacon_value = TKOHBeaconParser.get_beacon_value(pack, mac=None, rssi=None)
#                 except Exception as e:
#                     continue
#                 else:
#                     if beacon_value.battery is None:
#                         try:
#                             self.publish(SensorEvent(identifier=msg.topic,
#                                                      value=BeaconDataPackage(target_identifier=beacon_value.beacon_mac,
#                                                                              value=beacon_value,
#                                                                              timestamp=mqtt_client_recv_ts,
#                                                                              source=SourceInfo(source_identifier=msg.topic,
#                                                                                                source_pos=Position(x=SOURCE_INFO_DICT[msg.topic].x,
#                                                                                                                    y=SOURCE_INFO_DICT[msg.topic].y,
#                                                                                                                    z=SOURCE_INFO_DICT[msg.topic].z,
#                                                                                                                    timestamp=-1,
#                                                                                                                    pos_type=SOURCE_INFO_DICT[msg.topic].type,
#                                                                                                                    )
#                                                                                                ),
#                                                                              )))  # using topic name as sniffer identifier
#                         except Exception as e:
#                             print(e)
#                     else:
#                         self.publish(Event(event_type="beacon_power",
#                                            timestamp=mqtt_client_recv_ts,
#                                            identifier=beacon_value.beacon_mac,
#                                            value=beacon_value,
#                                            ))
#
