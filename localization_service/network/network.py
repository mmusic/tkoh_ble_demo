from common.component import Component
import os
from config.common import SERVER_IP, SERVER_PORT, UPLOAD_FREQ, UPLOAD_TIMEOUT, VM
from config.common import API_SERVER_IP, API_SERVER_PORT
from common.event import *
from utils.security import encrypt, decrypt
from threading import Thread, Lock
import json
import time
from queue import Queue
from .tcp import TCPClient
from typing import Union
import requests


class Network(Component):
    def __init__(self):
        super().__init__()
        # fixme: bug, not able to reconnect, seems that not able to change network_status

        # self.add_event_listener("system_status", self.__update_network_status)
        #
        # self.add_event_listener("system_status", lambda e: self.__safe_upload(_add_upload_sensor_identifier(_filter_system_status(e))))  # todo: changing event name is hard to do refactor, not good
        # self.add_event_listener(SensorEvent._event_type, lambda e: self.__safe_upload(_filter_sensor_data(_add_upload_vm(e))))
        self.add_event_listener(ResultEvent._event_type, lambda e: self.__safe_upload(_add_upload_vm(e)))
        self.add_event_listener(LogEvent._event_type, lambda e: self.__safe_upload(_filter_log_data(e)))
        self.add_event_listener(BeaconPowerEvent._event_type, lambda e: self.__safe_upload(e))

        self.__safe_buffer_lock = Lock()
        self.__unsafe_buffer_lock = Lock()
        self.__safe_uploader = TCPClient(SERVER_IP, SERVER_PORT, with_ssl=True)
        # self.__unsafe_uploader = UDPClient(SERVER_IP, SERVER_PORT, with_ssl=True)
        self.__safe_buffer = Queue()  # insert type str
        self.__unsafe_buffer = Queue()
        self.__network_status = True

    def start(self):
        Thread(target=self.__safe_buffer_poll).start()
        # Thread(target=self.__unsafe_buffer_poll).start()
        # Thread(target=self.__redirect_remote_requests).start()  # todo: test

    def notify_api_server_result(self, e: ResultEvent):
        try:
            requests.post(url=f"http://{API_SERVER_IP}:{API_SERVER_PORT}/postTargetLatestLocation/",
                          json={'tmac': e.identifier,
                                'x': e.value.x,
                                'y': e.value.y,
                                'z': int(e.value.z),
                                'timestamp': e.value.timestamp}
                          )
        except Exception as err:
            self.publish(LogEvent(identifier=str(os.getpid()),
                                  value=LogMessage(level='warn',
                                                   msg=f'unable to post data={e} to api server due to error: {err}')))

    def __safe_buffer_poll(self):
        while True:
            if not self.__safe_buffer.empty():
                data = []
                # self.__safe_buffer_lock.acquire()
                while not self.__safe_buffer.empty():
                    data.append(self.__safe_buffer.get())
                # self.__safe_buffer_lock.release()

                if self.__network_status:
                    resend_ids = []
                    packet_dict = {}
                    for i, d in enumerate(data):
                        packet_dict[i] = d
                        if isinstance(d, ResendData):
                            resend_ids.append(d.idx)

                    packet = json.dumps(packet_dict).encode('utf-8')
                    # print(packet)
                    send_success_flag = self.__safe_uploader.send(packet, timeout=UPLOAD_TIMEOUT)

                    # if send_success_flag:
                    #     if len(resend_ids) > 0:
                    #         self.publish(event=Event(event_type="resend_success", ids=resend_ids))
                    # else:
                    #     self.__network_status = False

                # if not self.__network_status:
                #     data_list_backup = []
                #     for d in data:
                #         if not isinstance(d, ResendData):
                #             data_list_backup.append((d, ))  # note: make it compatible with db insertion
                #     self.publish(event=Event("data_backup", content=data_list_backup))
            time.sleep(UPLOAD_FREQ)  # note: UPLOAD_FREQ should adjust according to the traffic, seems 2 sec is good.

    # def __unsafe_buffer_poll(self):
    #     while True:
    #         if not self.__unsafe_buffer.empty():
    #             self.__unsafe_buffer_lock.acquire()
    #             d = self.__unsafe_buffer.get()
    #             self.__unsafe_buffer_lock.release()
    #             packet = json.dumps({0: d}).encode(encoding='utf-8')
    #             self.__unsafe_uploader.send(packet)
    #         time.sleep(UPLOAD_FREQ)

    def __redirect_remote_requests(self):
        pass
        # while True:
        #     msg = self.__safe_uploader.receive()  # blocking operation
        #     if msg == b'':
        #         time.sleep(10)  # note: assuming that remote server will never close the socket.
        #         continue
        #     print('[debug] receive msg: ')
        #     print(msg)
        #     # todo: no encryption for now
        #     msg_dict = json.loads(msg)
        #     print(f"[debug] receive {msg_dict}")
        #     try:
        #         assert msg_dict['event_type'] == 'remote_request'
        #         self.publish(Event(event_type='remote_request', data=msg_dict['data']))
        #     except Exception as e:
        #         print("[debug] error in __redirect_remote_requests")
        #         self.publish(LogEvent(level='warn', msg=f"Incorrect remote data format = {msg_dict}"))

    @staticmethod
    def pack_single_event(single_event: Event) -> str:
        # note: all encrypt and compress is done here
        # todo: need an effective compress algorithm
        d = json.dumps(str(single_event)).encode(encoding='utf-8')
        encrypted_d = encrypt(d)
        res = encrypted_d.decode(encoding='utf-8')
        return res

    @staticmethod
    def unpack_single_event(single_event_msg: str) -> DictStringify:
        # todo: the mechanism of current module loading not allows import network.py from the outside.
        msg = json.loads(decrypt(bytes(single_event_msg, encoding='utf-8')))
        return msg

    def __safe_upload(self, e: Union[Event, None]):
        # if hasattr(e, 'event_type'):
        #     self.publish(LogEvent(identifier=str(os.getpid()),
        #                           value=LogMessage(level='info',
        #                                            msg=f"network receive {e.event_type} at {time.time()}, data generated time = {e.timestamp}")))
        if e is None:
            return
        try:
            packed_data = self.pack_single_event(e)
        except Exception as err:
            self.publish(LogEvent(identifier=str(os.getpid()),
                                  value=LogMessage(level='warn', msg=f'in Networked.__safe_upload, unable to pack event: {err}, event = {e}')))
            return
        self.__safe_buffer_lock.acquire()
        self.__safe_buffer.put(packed_data)
        self.__safe_buffer_lock.release()

    def __unsafe_upload(self, e: Union[Event, None]):
        if e is None:
            return
        try:
            packed_data = self.pack_single_event(e)
        except Exception as e:
            return
        self.__unsafe_buffer_lock.acquire()
        self.__unsafe_buffer.put(packed_data)
        self.__unsafe_buffer_lock.release()

    def __resend_data(self, e: Event):
        if hasattr(e, 'data') and hasattr(e, 'idx'):
            self.__safe_buffer_lock.acquire()
            self.__safe_buffer.put(ResendData(e.data, e.idx))
            self.__safe_buffer_lock.release()

    # def __update_network_status(self, e: SystemStatusEvent):  # todo
    #     if hasattr(e, 'network_good'):
    #         self.__network_status = e.network_good


class ResendData:
    def __init__(self, d, idx):
        self.data = d
        self.idx = idx


# def _filter_system_status(e: Event) -> Union[Event, None]:
#     # todo: filter out system status not required by server
#     return e


def _filter_sensor_data(e: SensorEvent) -> Union[SensorEvent, None]:
    return e
    # if e.value.data_type == '3':  # beacon
    #     mac, rssi, manufacturer_data, other_ble_scan_info = e.value
    #     if manufacturer_data is None or not MTR_SERVICE_MAJOR_MINOR.is_mtr_beacon(manufacturer_data):
    #         return None
    #     else:
    #         try:
    #             major_minor = MTR_SERVICE_MAJOR_MINOR.get_mtr_service_major_minor_from_manufacturer_data(manufacturer_data)
    #         except Exception as err:
    #             return None
    #         else:
    #             e = SensorEvent(data_type=e.data_type, timestamp=e.timestamp, values=[str(major_minor), mac, rssi])
    # return e


def _filter_log_data(e: LogEvent) -> Union[LogEvent, None]:
    level = e.value.level.lower()  # todo: can't auto-complete second degree object
    if level == 'warn' or level == 'error':
        return e
    return None


# def _add_upload_sensor_identifier(e: Union[Uploadable, None]) -> Union[Uploadable, None]:
#     pass


def _add_upload_vm(e: Event) -> Union[Event, None]:
    if e is not None:
        e.vm = VM
        return e
    return None
