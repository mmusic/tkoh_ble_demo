import time
from threading import Thread, Lock
from typing import Union, List, Set, Callable
from config.TKOH import FILTER_MODULE_PARAMS, CAL_PERIOD_SEC
from collections import defaultdict


class SensorDataPreprocessor:
    # todo: it needs a config itself, and such config is tightly coupled with project background
    # todo: general configuration on multiple sensors, make it a pluggable module?
    def __init__(self, input_q, batch_output_q):
        # note: the input_q will only handle data with same target_identifier
        # note: how should we define format of 'value' in code?  using dict is the most general form that could be used across process
        self.input_q = input_q
        self.batch_output_q = batch_output_q  # note: every element is of form [{'target_identifier', 'data_type', 'value', 'timestamp', **other_keys}]

        # passing config from outside?
        self.beacon_preprocessor = BeaconDataPreprocessor(rssi_threshold=FILTER_MODULE_PARAMS['RSSI_THRESHOLD'])

    def run(self):
        Thread(target=self.batch_input_data).start()

    def batch_input_data(self):
        # note: define the batching strategy
        while True:
            batches = defaultdict(list)  # note: {target_ident: {'beacon_batch':[], 'imu_batch':[], 'wifi_batch':[]}}

            while not self.input_q.empty():
                sensor_data = self.input_q.get()
                # print("SensorDataPreprocessor, self.input_q.get()", sensor_data)
                target_ident = sensor_data['target_identifier']
                sensor_type = sensor_data['data_type']

                if sensor_type == '3':
                    batches['beacon_batch'].append(sensor_data)
                else:
                    continue  # todo

            if batches:
                processed_beacon_batch = self.beacon_preprocessor.preprocess_batch(batches['beacon_batch'])
                # processed_wifi_batch = self._preprocess_beacon(batches['wifi_batch'])
                # processed_imu_batch = self._preprocess_beacon(batches['imu_batch'])

                # print("SensorDataPreprocessor, processed_beacon_batch", processed_beacon_batch)
                if processed_beacon_batch:
                    self.batch_output_q.put({'target_identifier': target_ident,
                                             'beacon_batch': processed_beacon_batch,
                                             'imu_batch': [],
                                             'wifi_batch': []})
            time.sleep(CAL_PERIOD_SEC)


        # while True:
        #     beacon_data = []
        #     imu_data = []
        #     wifi_data = []
        #     if self.__core_running_process is not None:
        #         self.__clear_sensor_data_q_lock.acquire()
        #         while not self.sensor_data_q.empty():
        #             d = self.sensor_data_q.get()
        #             if d[0] == 1:
        #                 imu_data.append(d)
        #             elif d[0] == 2:
        #                 wifi_data.append(d)
        #             else:
        #                 beacon_data.append(d)
        #         self.__clear_sensor_data_q_lock.release()
        #
        #         beacon_data = self.__fuse_multi_in_one_beacon(beacon_data)
        #
        #         batched_data = beacon_data+imu_data+wifi_data
        #         if len(batched_data) > 0:
        #             self.__clear_sensor_batch_data_q_lock.acquire()
        #             self.sensor_batch_data_q.put(batched_data)
        #             print("[estimator]: insert batched data")
        #             self.__clear_sensor_batch_data_q_lock.release()
        #
        #     if self.__site_config is not None:
        #         time.sleep(self.__site_config.CAL_PERIOD_SEC)
        #     else:
        #         time.sleep(2)


class BeaconDataPreprocessor:
    def __init__(self,
                 rssi_threshold: Union[int, None] = None,
                 valid_beacon_format_list: Union[List[Callable[[str], bool]], None] = None,
                 equivalent_beacon_set: Union[None, List[Set]] = None,
                 avg_flag=False,
                 **kwargs
                 ):

        self.rssi_threshold = rssi_threshold
        self.valid_beacon_format_list = valid_beacon_format_list
        self.equivalent_beacon_set = equivalent_beacon_set  # todo: do a transformation
        self.avg_flag = avg_flag

    def preprocess_batch(self, raw_beacon_batch: List) -> List:
        batch = raw_beacon_batch
        if self.valid_beacon_format_list:
            batch = self.filter_none_deploy_beacons(batch, self.valid_beacon_format_list)
        if self.rssi_threshold:
            batch = self.filter_weak_rssi(batch, self.rssi_threshold)
        if self.equivalent_beacon_set:
            batch = self.fuse_multi_in_one(batch)
        if self.avg_flag:
            batch = self.average_rssi(batch)
        return batch

    @staticmethod
    def average_rssi(batch_data: List) -> List:
        avg_batch = []
        batch_records = defaultdict(list)
        for beacon_data in batch_data:
            batch_records[beacon_data['target_identifier']].append(beacon_data)
        for batch in batch_records.values():
            target_identifier = batch[0]['target_identifier']
            data_type = batch[0]['data_type']
            source = batch[0]['source']

            rssi = 0
            for beacon_data in batch:
                rssi += beacon_data['value']['rssi']
            rssi = rssi / len(batch)

            timestamp = 1_000_000_000
            for beacon_data in batch:
                timestamp = max(timestamp, beacon_data['timestamp'])
            avg_batch.append(({'target_identifier': target_identifier,
                               'data_type': data_type,
                               'value':  {'rssi': rssi},
                               'source': source,
                               'timestamp': timestamp}))
        return avg_batch

    @staticmethod
    def filter_weak_rssi(batch_data: List, rssi_threshold: int) -> List:
        # todo: bad design, you don't even know how beacon_data looks like, but maybe I don't need to know how it looks like?
        batch = []
        if rssi_threshold is not None:
            for data in batch_data:
                if data['value']['rssi']:
                    if 'value' in data and 'rssi' in data['value'] and data['value']['rssi'] >= rssi_threshold:
                        batch.append(data)
        else:
            return batch_data
        return batch

    @staticmethod
    def fuse_multi_in_one(batch_data: List) -> List:
        pass

    @staticmethod
    def filter_none_deploy_beacons(batch_data: List, valid_beacon_format_list: List[Callable[[str], bool]]) -> List:
        batch = []
        if valid_beacon_format_list:
            for data in batch_data:
                if 'value' in data and 'manufacturer' in data['value']:
                    for valid_format in valid_beacon_format_list:
                        if valid_format(data['value']['manufacturer']):
                            batch.append(data)
        else:
            return batch_data
        return batch


# class IMUDataPreprocessor:
#     def __init__(self):
#         pass
#
#     def preprocess_batch(self, raw_imu_batch: List) -> List:
#         pass
#
#     @staticmethod
#     def imu_step_estimation():
#         pass
#

# class WIFIDataPreprocessor:
#     def __init__(self):
#         pass
#
#     def preprocess_batch(self, raw_wifi_batch: List) -> List:
#         pass
#
#     @staticmethod
#     def wifi_fuse_multi_ssid_in_one():
#         pass

