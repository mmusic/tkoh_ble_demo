from typing import List, Tuple, Optional
from queue import deque


class RSSIFilter:
    def __init__(self, config_manager):
        print("init RSSIFilter")
        self.rssi_buffer = None
        self.previous_filtered_rssi = None
        self.cur_filtered_rssi = None
        self.cur_window_start_time = None  # used for stream type rssi

        self.idx_to_macaddr = self._map_from_idx_to_macaddr(
            config_manager.beacon_table_config)

    def filter(self, rssi_info: deque):
        if len(rssi_info) == 0:
            return [], None
        if self.rssi_buffer is None:
            self._init_stream_type_rssi_buffer()
        return self.filter_rssi_from_pool(rssi_info)

    def filter_rssi_from_pool(self, raw_rssi_queue: deque) -> Tuple[List[Tuple[float, int]], Optional[float]]:
        ts_avg = 0.
        for mac_addr, rssi, ts in raw_rssi_queue:
            self.rssi_buffer[mac_addr].append(rssi)
            ts_avg += ts

        self._calculate_cur_filtered_rssi()

        res = []
        for idx in range(len(self.idx_to_macaddr)):
            mac_addr = self.idx_to_macaddr[idx]
            res.append((self.cur_filtered_rssi[mac_addr], len(
                self.rssi_buffer[mac_addr])))

        # refresh for next window
        self._init_stream_type_rssi_buffer()
        self.previous_filtered_rssi = self.cur_filtered_rssi
        self.cur_filtered_rssi = None

        return res, ts_avg / len(raw_rssi_queue)

    def _calculate_cur_filtered_rssi(self):
        self.cur_filtered_rssi = {mac_addr: sum(rssi_list)/len(rssi_list) if len(rssi_list) > 0 else -120. for mac_addr, rssi_list in self.rssi_buffer.items()}

    def _map_from_idx_to_macaddr(self, beacon_table_config) -> dict:
        res = {}
        _, beacon_addrs_list, __ = beacon_table_config

        for idx, mac_addr in enumerate(beacon_addrs_list):
            res[idx] = mac_addr
        return res

    def _init_stream_type_rssi_buffer(self):
        self.rssi_buffer = {self.idx_to_macaddr[i]: []
                            for i in range(len(self.idx_to_macaddr))}
