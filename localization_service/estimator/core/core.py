# todo: syncronizer is done here, not in data pool
import time


class Core:
    def __init__(self, pool_handler, config_manager):
        self.pool_handler = pool_handler
        self.rssi_filter, self.localization_module, self.velocity_module = config_manager.init_modules_instances()

    def cal_position_and_velocity(self):
        start_cal = time.time()
        raw_rssi = self.pool_handler.get()
        print(f"pool rssi: {raw_rssi}")
        filtered_rssi, ts = self.rssi_filter.filter(raw_rssi)
        #print(f"rssi ={filtered_rssi}")
        # if ts is not None:
        #     print(f"ts={format(ts, '.2f')}")
        # else:
        #     print(f"ts={ts}")
        # print(f"pool_rssi = {[(rssi, t) for _, rssi, t in raw_rssi]}")
        cur_pos = self.localization_module.estimate_position(filtered_rssi, ts)
        cur_vel = self.velocity_module.estimate_velocity(cur_pos, ts)
        end_cal = time.time()
        print(f"cal_time = {end_cal - start_cal}")
        return cur_pos, cur_vel, ts


import time
from queue import deque
import threading
from copy import deepcopy


class RSSIPool:
    # used in online program

    _instance = None
    _inited = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_manager):
        if not type(self)._inited:
            type(self)._inited = True
            self.cur_ts = None
            self.window_size = float(config_manager.trackingIO_config['data_pool']['window_size_in_sec'])
            self.sec_per_update = float(config_manager.trackingIO_config['data_pool']['sec_per_update'])
            self.data_buffer = deque([])
            self.data_buffer_lock = threading.Lock()
            self.prev_latest_rssi_ts = None
            run_clock_thread = threading.Thread(target=self._run_clock)
            run_clock_thread.start()

    def _run_clock(self):
        while 1:
            self.cur_ts = time.time()
            self._update_data_buffer()
            time.sleep(self.sec_per_update)

    def send(self, data):
        #print(f"put data = {data}")
        self.data_buffer_lock.acquire()
        self.data_buffer.append(data[:])
        self.data_buffer_lock.release()

    def _update_data_buffer(self):
        self.data_buffer_lock.acquire()
        # print(f"update at ts = {self.cur_ts}")
        while len(self.data_buffer) > 0 and self.cur_ts - self.data_buffer[0][-1] > self.window_size:
            self.data_buffer.popleft()
        self.data_buffer_lock.release()

    def get(self):
        self.data_buffer_lock.acquire()
        if self.prev_latest_rssi_ts is not None:
            while len(self.data_buffer) > 0 and self.prev_latest_rssi_ts >= self.data_buffer[0][-1]:
                self.data_buffer.popleft()
        if len(self.data_buffer) > 0:
            self.prev_latest_rssi_ts = self.data_buffer[-1][-1]
        res = deepcopy(self.data_buffer)
        self.data_buffer_lock.release()
        return res
