import time
# import sys
# sys.path = ['/Users/kfl/on-board-program'] + sys.path
import os
from typing import List, Union
from collections import defaultdict
from common.component import Component
from threading import Thread, active_count
from multiprocessing import Process, Lock, Queue, set_start_method
import queue
from .preprocessor import SensorDataPreprocessor
from common.data_type import *
from common.event import *
import time
from config.common import SENSOR_SITE
import importlib
from estimator.core.velocity.analyse_velocity import VelocityModule
# from estimator.core.localization.localization import LocalizationModule
from estimator.core.localization.localization_pf import LocalizationModule
from utils.utils import kill_thread
from config.TKOH import LOCALIZATION_MODULE_PARAMS, MAPS  # todo


class Estimator(Component):
    def __init__(self):
        super().__init__()
        self.add_event_listener(SensorEvent._event_type, self.on_receive_sensor_data)  # note: don't know why it warns

        self.add_event_publisher(LogEvent._event_type)
        self.add_event_publisher(ResultEvent._event_type)

        self.tracking_records = {}  # {target_identifier: {process_id, preprocessor_thread_handle, target_data_input_q}}
        self.process_records = {}  # {process_id: {target_nums, target_q, batch_input_q, result_q, log_q, terminate_q}}
        self.estimator_process_log_q = Queue()
        self.output_result_q = Queue()  # use the same one for all processes and threads


        # self.site = SENSOR_SITE
        # self.__site_config = None if self.site is None else self.__load_config()
        # self.__assist_thread_pool = [Thread(target=self.__poll_result_q),
        #                              Thread(target=self.__batch_sensor_data),
        #                              ]

    def __load_config(self):
        pass
        # # note: don't know if it's a good practice to use self here, implicitly depend on private variable
        # try:
        #     site_config = importlib.import_module(name=f'config.{self.site}')
        # except Exception as e:
        #     self.publish(LogEvent(level='error', msg=f"unable to load config for core {e}", timestamp=time.time()))
        #     return None
        # return site_config

    def __id_request(self):
        pass

    def start(self):
        # note: core would initialize its position based on the first few BLE inputs, if no BLE inputs, then no init pos
        Thread(target=self.__poll_result_q).start()

    def restart(self):
        pass

    def terminate_core(self):
        pass

    def __poll_result_q(self):
        while True:
            # {identifier, x, y, z, timestamp}
            position = self.output_result_q.get()  # xyz
            x, y, z, timestamp = position['x'], position['y'], position['z'], position['timestamp']
            self.publish(ResultEvent(identifier=position['target_identifier'],
                                     value=Position(x=x, y=y, z=z, timestamp=timestamp, pos_type=0)))

    def on_receive_sensor_data(self, event: SensorEvent):
        # note: define strategy to start a process or ask a process to start a thread
        # print(f"[estimator]: receive sensor data {event}")
        if event.value.target_identifier not in self.tracking_records:
            pid = self._find_a_free_process()
            sensor_data_input_q = Queue()

            if pid:
                target_q = self.process_records[pid]['target_q']
                batch_q = self.process_records[pid]['batch_input_q']
            else:
                target_q, batch_q, terminate_q = Queue(), Queue(), Queue()
                # print(batch_q)
                estimator_process = EstimatorProcess(target_q=target_q,
                                                     batch_input_q=batch_q,
                                                     result_q=self.output_result_q,
                                                     log_q=self.estimator_process_log_q,
                                                     terminate_q=terminate_q)

                # todo: using fork so that it could estimator_process.run can be used?
                p = Process(target=estimator_process.run, args=(False, ))
                p.start()
                self.process_records[p.pid] = {'target_nums': 1,
                                               'target_q': target_q,
                                               'batch_input_q': batch_q,
                                               'result_q': self.output_result_q,
                                               'log_q': self.estimator_process_log_q,
                                               'terminate_q': terminate_q}
                pid = p.pid

            preoprocess_thread = SensorDataPreprocessor(input_q=sensor_data_input_q, batch_output_q=batch_q)
            t = Thread(target=preoprocess_thread.run)
            t.start()

            self.tracking_records[event.value.target_identifier] = {'process_id': pid,
                                                                    'preprocessor_thread': t,
                                                                    'target_data_input_q': sensor_data_input_q}
            self.process_records[pid]['target_nums'] += 1

            target_q.put({'target_identifier': event.value.target_identifier,
                          'algo_params': LOCALIZATION_MODULE_PARAMS,
                          'map_constraints': MAPS})

        sensor_data_input_q = self.tracking_records[event.value.target_identifier]['target_data_input_q']
        if isinstance(event.value, BeaconDataPackage):
            d = {'target_identifier': event.value.target_identifier,
                                     'data_type': event.value.data_type,
                                     'value':  {'rssi': event.value.value.rssi},
                                     'source': {'source_pos': {'x': event.value.source.source_pos.x,
                                                               'y': event.value.source.source_pos.y,
                                                               'z': event.value.source.source_pos.z,
                                                               'pos_type': event.value.source.source_pos.pos_type,
                                                    },
                                                },
                                     'timestamp': event.timestamp
                                     }
            sensor_data_input_q.put(d)
            # if d['target_identifier'] == '771f4541e1be43aaa8835a3ed4e2e15b06360070':
            #     print('data put q done', d['timestamp'])

    def _find_a_free_process(self) -> Union[int, None]:
        min_target_nums = 1000
        suitable_pid = None
        for pid, process_info in self.process_records.items():
            if process_info['target_nums'] < 150 and process_info['target_nums'] < min_target_nums:
                min_target_nums = process_info['target_nums']
                suitable_pid = pid
        return suitable_pid

    def on_receive_remote_request(self, event: Event):
        pass

    def __batch_sensor_data(self):
        pass


class EstimatorProcess:
    # note: 1. responsible for creating core threads
    # note: 2. handle multiple targets
    # note: 3. each process has one batch_input_q
    def __init__(self, target_q: Queue, batch_input_q: Queue, result_q: Queue, log_q: Queue = None, terminate_q: Queue = None):
        self.result_q = result_q  # note: every element is of form {'target_identifier': str, 'pos': {'x', 'y', 'z'}, 'timestamp': }
        self.target_q = target_q  # note: every element is of form {'target_identifier', 'algo_params', 'map_constraints'}
        self.batch_input_q = batch_input_q  # note: every element is of form [{'target_identifier': {'beacon_batch':[], 'imu_batch':[], 'wifi_batch':[]}}]
        self.log_q = log_q        # note: every element is of form {'target_identifier', 'msg', 'timestamp'}
        self.terminate_q = terminate_q  # note: every element is of form {'target_identifier'}

        self._target_batch_input_q = {}

        self._register_target_lock = Lock()
        self._register_target = {}

    def run(self, daemon=True):
        # print("start a new process")
        t1 = Thread(target=self.redirect_batch_input_q)
        t2 = Thread(target=self.spawn_core_thread)
        t1.start()
        t2.start()
        if self.terminate_q:
            Thread(target=self.terminate_core_thread).start()
        if not daemon:
            t1.join()
            t2.join()

        # print("end a new process")

    def spawn_core_thread(self):
        while True:
            target_info = self.target_q.get()  # block
            target_ident = target_info['target_identifier']
            target_algo_params = target_info['algo_params']
            target_map_constraints = target_info['map_constraints']

            # self._register_target_lock.acquire()
            if target_ident not in self._register_target:
                # print('----target_ident', target_ident)
                localization_core = LocalizationModule(algo_params=target_algo_params,
                                                       map_constraints=list(target_map_constraints.values()))

                self._target_batch_input_q[target_ident] = Queue()
                self._register_target[target_ident] = localization_core
                # t = Thread(target=self.calculate, args=(target_ident, ))  # note: pay attention to the order
                # t.start()
                proc_write1 = Process(target=self.calculate, args=(target_ident,))
                proc_write1.start()
                # time.sleep(0.1)
            # self._register_target_lock.release()

    def terminate_core_thread(self):
        while True:
            terminate_target = self.terminate_q.get()  # block
            target_ident = terminate_target['target_identifier']

            self._register_target_lock.acquire()
            if target_ident in self._register_target:
                # hack, modify the output format from list to dict and also add tmac info
                t = self._register_target[target_ident]
                try:
                    kill_thread(t)
                except Exception:
                    pass
                finally:
                    del self._register_target[target_ident]
            self._register_target_lock.release()

    def redirect_batch_input_q(self):
        while True:
            batches = self.batch_input_q.get()
            target_ident = batches['target_identifier']
            # print('target_ident', target_ident)
            if target_ident in self._register_target:
                # pass
                self._target_batch_input_q[target_ident].put(batches)
            

    def calculate(self, target_identifier):
        # todo: may conflict with terminate for now
        # todo: handle multiple sensor
        q = self._target_batch_input_q[target_identifier]
        core = self._register_target[target_identifier]  # todo: err
        # time.sleep(10)
        while True:
            batch_sensor_data = q.get()  # block
            beacon_batch = batch_sensor_data['beacon_batch']
            # cal_start_ts = time.time()
            result = core.estimate_position(beacon_data_batch=beacon_batch, imu_data_batch=None, wifi_data_batch=None)
            result['target_identifier'] = target_identifier
            print(result)
            self.result_q.put(result)
            # cal_end_ts = time.time()
            assert 'x' in result and 'y' in result and 'z' in result and 'timestamp' in result
            # print(f'calc time = {cal_end_ts - cal_start_ts}s')


if __name__ == '__main__':
    m = importlib.import_module(name=f'config.KOB')
    print(dir(m))
