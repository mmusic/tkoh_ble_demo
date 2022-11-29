from common.component import Component
from common.event import Event, LogEvent
from config.common import DATABASE_FILE_PATH, DATABASE_NAME, DATABASE_TABLE_NAME
from threading import Thread, Lock
import sqlite3
from queue import Queue
import time
from typing import Iterable


class BackUpSystem(Component):
    def __init__(self):
        super().__init__()
        self.add_event_publisher("resend_data")
        self.add_event_listener("data_backup", self.__on_data_backup)
        self.add_event_listener("resend_success", self.__on_resend_success)
        self.add_event_publisher("log_msg")
        self.__db = None
        self.__table_name = DATABASE_TABLE_NAME
        self.__resend_q_lock = Lock()
        self.__resend_success_queue = Queue()
        self.__backup_q_lock = Lock()
        self.__backup_queue = Queue()

    def start(self):
        Thread(target=self.__poll).start()
        Thread(target=self.__resend).start()

    def __resend(self):
        pass

    def __poll(self):
        self.__db = sqlite3.connect(database=DATABASE_FILE_PATH)
        if not self.__check_table_exist(self.__table_name):
            self.__create_table(self.__table_name)

        while True:
            tmp_resend_success_ids, tmp_backup_data = [], []

            self.__resend_q_lock.acquire()
            while not self.__resend_success_queue.empty():
                tmp_resend_success_ids.append(self.__resend_success_queue.get())
            self.__resend_q_lock.release()

            self.__backup_q_lock.acquire()
            while not self.__backup_queue.empty():
                tmp_backup_data.append(self.__backup_queue.get())
            self.__backup_q_lock.release()

            s_t = time.time()
            self.__insert(data_list=tmp_backup_data)
            e_t = time.time()
            self.publish(LogEvent(level='info',
                                  msg=f"backup.__insert, consume {e_t - s_t}, insert size = {len(tmp_backup_data)}, at {s_t}"))

            self.__delete(idx_list=tmp_resend_success_ids)

            time.sleep(1)

    def __insert(self, data_list):
        c = self.__db.cursor()
        if len(data_list) == 0:
            return
        try:
            c.executemany(f"INSERT INTO {self.__table_name} (content) VALUES (?)", data_list)
            self.__db.commit()
        except Exception as e:
            self.publish(LogEvent(level='error',
                                  msg=f"\033[91m Error occur when inserting data={data_list}, {e}"))

    def __delete(self, idx_list):
        c = self.__db.cursor()
        for idx in idx_list:
            try:
                c.execute(f"DELETE FROM {self.__table_name} WHERE id={idx}")
            except Exception as e:
                self.publish(LogEvent(level='error',
                                      msg=f"\033[91m Error occur when deleting idx={idx}, {e}"))
            self.__db.commit()

    def __on_data_backup(self, e: Event):
        try:
            if isinstance(e, LogEvent):
                self.db.insert_log(src_type='online_log',
                                   level=e.level,
                                   ts=e.timestamp,
                                   content=e.msg)
            elif isinstance(e, ResultEvent):
                self.db.insert_sensor_loc(ts=e.timestamp,
                                          sensor=e.target_identifier,
                                          vm=VM,
                                          pos_x=e.values[0],
                                          pos_y=e.values[1],
                                          pos_z=e.values[2],
                                          )
            elif isinstance(e, SensorEvent) and e.data_type is SensorType.SENSOR_BLE:
                if not (hasattr(e, 'rmac') and hasattr(e, 'tmac')):
                    raise ValueError("missing key in BLE sensor event")
                self.db.insert_beacon_scan_data(ts=e.timestamp,
                                                vm=VM,
                                                beacon=e.tmac,
                                                rssi=e.values[1],
                                                sensor_label=e.rmac,
                                                major=0,
                                                minor=0,
                                                uuid=0,
                                                )  # todo
        except Exception as err:
            self.publish(LogEvent(level='error', msg=f"\033[91m Error occur when inserting data={e}, {err}"))

    def __on_resend_success(self, e: Event):
        if hasattr(e, 'ids'):
            self.__resend_q_lock.acquire()
            for idx in e.ids:
                self.__resend_success_queue.put(idx)
            self.__resend_q_lock.release()

    def __check_table_exist(self, table_name: str):
        c = self.__db.cursor()
        flag = len(c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';").fetchall()) != 0
        c.close()
        return flag

    def __create_table(self, table_name):
        sql_create_temp_table = f" CREATE TABLE IF NOT EXISTS {table_name} ( \
                                            id integer PRIMARY KEY autoincrement,\
                                            content text NOT NULL \
                                        ); "
        c = self.__db.cursor()
        c.execute(sql_create_temp_table)
        self.__db.commit()
        c.close()


if __name__ == "__main__":
    backup = BackUpSystem()
    backup.start()
