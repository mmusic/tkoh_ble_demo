from multiprocessing import Queue
from typing import List, Union, Tuple, Dict
from threading import Thread
import time
import random


# cython code wrapper class
class LocalizationModule:
    # note: core itself will return localization position only.
    # note: using queue is easier to do ipc in python, but it's not suitable for the logic of core
    def __init__(self,
                 algo_params: Union[Dict, None] = None,
                 map_constraints: Union[List[Tuple[Tuple]], None] = None):
        # todo: if the map constraint is None by default, then the init strategy should consider well.
        if algo_params is None:
            self.algo_params = {
                'num_of_particles': 800,
                'max_vel': 2.,  # maximum speed of human, unit in m/s
                'obs_model_mean': [-76.0656, 2.8871],  # mean and variance of P(rssi, distance)
                'obs_model_var': [[53.171, -5.218], [-5.218, 2.912]],
                'loss_model_range': [-120, -110],
                'weight_observe': 0.8,  # mean and variance of P(rssi, distance)
                'weight_loss': 1 - 0.8,
                # 'map_bound': [[-70, 110], [0, 15]],
                # 'position_candidates_regions': [MAPS[1], MAPS[2], MAPS[3], MAPS[4], MAPS[5], MAPS[6]],
                'grid_size': 0.5,
            }
        else:
            self.algo_params = algo_params
        self.map_constraints = map_constraints
        self.init_pos_flag = True

    def estimate_position(self, beacon_data_batch, imu_data_batch, wifi_data_batch) -> Dict:
        if beacon_data_batch is not None:
            sum_pos_x, sum_pos_y, sum_pos_z = 0, 0, 0
            sum_t = 0
            for beacon_data in beacon_data_batch:
                ts = beacon_data['timestamp']
                rssi = beacon_data['value']['rssi']
                x, y, z = beacon_data['source']['source_pos']['x'], beacon_data['source']['source_pos']['y'], beacon_data['source']['source_pos']['z']
                sum_pos_x, sum_pos_y, sum_pos_z = sum_pos_x + x, sum_pos_y + y, sum_pos_z + z
                sum_t += ts
            return {'x': sum_pos_x/len(beacon_data_batch),
                    'y': sum_pos_y/len(beacon_data_batch),
                    'z': sum_pos_z/len(beacon_data_batch),
                    'timestamp': sum_t/len(beacon_data_batch), }

