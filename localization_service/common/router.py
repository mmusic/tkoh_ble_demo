from threading import Thread
from multiprocessing import Lock
from queue import Queue, Empty
from common.event import *
from common.data_type import *
from collections import defaultdict
from os import getpid
import time
import traceback


# todo: Router should support IPC
class Router:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if Router._instance is None:
            Router._instance = super().__new__(cls, *args, **kwargs)
            Router._instance._init_flag = False
        return Router._instance

    def __init__(self):
        if not self._init_flag:
            self.__listeners = defaultdict(list)
            self.__publishers = {}
            self.__msg_q = Queue()
            self.__msg_q_lock = Lock()
            self.__listeners_lock = Lock()
            self._init_flag = True

    def loop_forever(self, daemon=False):
        def __loop():
            tmp_q = Queue()
            while 1:
                if not self.__msg_q.empty():
                    # self.__msg_q_lock.acquire()
                    # while not self.__msg_q.empty():
                    tmp_q.put(self.__msg_q.get())
                    # self.__msg_q_lock.release()
                while not tmp_q.empty():
                    # print(tmp_q.qsize())
                    msg = tmp_q.get()
                    for callback in self.__listeners[msg.event_type]:  # todo: may need a lock, because of self.register_listener()
                        try:
                            callback(msg)
                        except Exception as e:
                            self.unregister_listener(msg.event_type, callback)  # todo: seems to affect for loop, do a test
                            self.dispatch_event(LogEvent(identifier=str(getpid()),
                                                         value=LogMessage(level='error',
                                                                          msg=f"Unregister function due to error: {traceback.format_exc()}")))
                    # time.sleep(1)
                time.sleep(0.001)
        Thread(target=__loop).start()
        Thread(target=self.__self_examination).start()

    def register_listener(self, event_type, callback):
        self.__listeners[event_type].append(callback)
        # print(f"listener list in router = {self.__listeners}")

    def register_publisher(self, event_type):
        if event_type not in self.__publishers:
            self.__publishers[event_type] = True
        # print(f"publisher list in router = {self.__publishers}")

    def unregister_listener(self, event_type, callback):
        self.__listeners_lock.acquire()
        callback_list = self.__listeners[event_type]
        callback_list.remove(callback)
        self.__listeners_lock.release()
        # print(f"updated listener list in router = {self.__listeners}")

    def unregister_publisher(self, event_type):
        # todo: should be called from outside?
        pass

    def dispatch_event(self, event: Event):
        if event.event_type not in self.__publishers:
            return  # todo: maybe write log?
        self.__msg_q_lock.acquire()
        self.__msg_q.put(event)
        # print(f"in router {event}")
        self.__msg_q_lock.release()

    def __self_examination(self):
        while 1:
            print(f"------------------------router msg pool size = {self.__msg_q.qsize()}")
            time.sleep(10)
