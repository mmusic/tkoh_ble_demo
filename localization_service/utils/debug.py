from common.component import Component
from common.event import *
import time
from threading import Thread
import os


# note: used to redirect to stdout, in principle, all the events traffic should be listened by Debug class
class Debug(Component):
    def __init__(self):
        super().__init__()
        #self.add_event_listener(SensorEvent._event_type, self.print_data)  # from SensorManager
        #self.add_event_listener(BeaconPowerEvent._event_type, self.print_data)
        self.add_event_listener(LogEvent._event_type, self.print_data)  # todo: from all components, except for router?
        # self.add_event_listener("data_backup", self.print_data)  # from Network
        # self.add_event_listener("resend_success", self.print_data)  # from Network
        # self.add_event_listener("resend_data", self.print_data)  # from BackUpSystem
        # self.add_event_listener(ResultEvent._event_type, self.print_data)  # from Estimator
        # self.add_event_listener("system_status", self.print_data)  # from SystemMonitor
        # self.add_event_listener("sensor_pause", self.print_data)  # todo: from Network or hci
        # self.add_event_listener(RemoteRequestIdEvent._event_type, self.print_data)

        # self.add_event_publisher("alive")
        # self.add_event_listener("alive", self.print_data)

        # self.add_event_publisher(ResultEvent._event_type)

    def start(self):
        pass
        #Thread(target=self.notice_alive).start()
        # Thread(target=self.generate_result_event).start()
        # Thread(target=self.generate_raw_data).start()

    def print_data(self, e: Event):
        print(f"{time.time()} {e} debugmodule recvtime")

    def notice_alive(self):
        while True:
            self.publish(DebugEvent(event_type="alive", identifier=None, value=None))
            time.sleep(20)

    def generate_result_event(self):
        while True:
            self.publish(ResultEvent(identifier='771f4541e1be43aaa8835a3ed4e2e15b06360039',
                                     value=Position(x=10,
                                                    y=20,
                                                    z=1,
                                                    timestamp=time.time(),
                                                    pos_type=1)))
            time.sleep(1)

    def generate_raw_data(self):
        e1 = SensorEvent(identifier='BL-12',
                        value=BeaconDataPackage(target_identifier='974c0089517c',
                                                value=BeaconValue(beacon_mac='974c0089517c',
                                                                  rssi=-53,
                                                                  major='8900',
                                                                  minor='4c97',
                                                                  uuid='f000aab004514000b000000000000000',
                                                                  battery=None,
                                                                  tx_power=None,
                                                                  ),
                                                timestamp=1615133237.7326496,
                                                source=SourceInfo(source_identifier='BL-12',
                                                                  source_pos=Position(x=35.67,
                                                                                      y=11.29,
                                                                                      z=2.0,
                                                                                      timestamp=-1,
                                                                                      pos_type='non-lon-lat',
                                                                                      )
                                                                  ),
                                                ))
        e2 = SensorEvent(identifier='BL-12',
                         value=BeaconDataPackage(target_identifier='70f729eef30c',
                                                 value=BeaconValue(beacon_mac='70f729eef30c',
                                                                   rssi=-61,
                                                                   major='0636',
                                                                   minor='0084',
                                                                   uuid='771f4541e1be43aaa8835a3ed4e2e15b',
                                                                   battery=None,
                                                                   tx_power=None,
                                                                   ),
                                                 timestamp=1615133162.5906456,
                                                 source=SourceInfo(source_identifier='BL-12',
                                                                   source_pos=Position(x=35.67,
                                                                                       y=11.29,
                                                                                       z=2.0,
                                                                                       timestamp=-1,
                                                                                       pos_type='non-lon-lat',
                                                                                       )
                                                                   ),
                                                 ))
        e3 = SensorEvent(identifier='BL-12',
                         value=BeaconDataPackage(target_identifier='134a34eef30c',
                                                 value=BeaconValue(beacon_mac='134a34eef30c',
                                                                   rssi=-62,
                                                                   major='0636',
                                                                   minor='0068',
                                                                   uuid='771f4541e1be43aaa8835a3ed4e2e15b',
                                                                   battery=None,
                                                                   tx_power=None,
                                                                   ),
                                                 timestamp=1615133162.5906456,
                                                 source=SourceInfo(source_identifier='BL-12',
                                                                   source_pos=Position(x=35.67,
                                                                                       y=11.29,
                                                                                       z=2.0,
                                                                                       timestamp=-1,
                                                                                       pos_type='non-lon-lat',
                                                                                       )
                                                                   ),
                                                 ))
        data_list = [e1, e2, e3]
        while True:
            for d in data_list:
                self.publish(d)
            time.sleep(4)



