# from multiprocessing import Queue
# from typing import List, Union, Tuple, Dict
# from threading import Thread
# import time
# import random
#
#
# # cython code wrapper class
class LocalizationModule:
    pass
#     # note: core itself will return localization position only.
#     # note: using queue is easier to do ipc in python, but it's not suitable for the logic of core
#     def __init__(self,
#                  algo_params: Union[Dict, None] = None,
#                  map_constraints: Union[List[Tuple[Tuple]], None] = None):
#         # todo: if the map constraint is None by default, then the init strategy should consider well.
#         if algo_params is None:
#             self.algo_params = {
#                 'num_of_particles': 800,
#                 'max_vel': 2.,  # maximum speed of human, unit in m/s
#                 'obs_model_mean': [-76.0656, 2.8871],  # mean and variance of P(rssi, distance)
#                 'obs_model_var': [[53.171, -5.218], [-5.218, 2.912]],
#                 'loss_model_range': [-120, -110],
#                 'weight_observe': 0.8,  # mean and variance of P(rssi, distance)
#                 'weight_loss': 1 - 0.8,
#                 # 'map_bound': [[-70, 110], [0, 15]],
#                 # 'position_candidates_regions': [MAPS[1], MAPS[2], MAPS[3], MAPS[4], MAPS[5], MAPS[6]],
#                 'grid_size': 0.5,
#             }
#         else:
#             self.algo_params = algo_params
#         self.map_constraints = map_constraints
#         self.init_pos_flag = False
#
#     def estimate_position(self, beacon_data_batch, imu_data_batch, wifi_data_batch) -> Dict:
#         # todo
#         if beacon_data_batch is not None:
#             sum_pos_x, sum_pos_y, sum_pos_z = 0, 0, 0
#             sum_t = 0
#             for beacon_data in beacon_data_batch:
#                 sensor_type = beacon_data['data_type']
#                 ts = beacon_data['timestamp']
#                 value = beacon_batch['value']
#                 x, y, z = beacon_pos
#                 sum_pos_x, sum_pos_y, sum_pos_z = sum_pos_x + x, sum_pos_y + y, sum_pos_z + z
#                 sum_t += ts
#             return {'x': , 'y':, 'z':, 'timestamp'}
#
#         while True:
#             print(f"[localization]: try to get data at {time.time()}")
#             sensor_data_batch = self.sensor_batch_input_q.get()
#             print(f"[localization]: success get data at {time.time()}")
#             imu_batch = []
#             beacon_batch = []
#             wifi_batch = []
#             for sensor_data in sensor_data_batch:
#                 if str(sensor_data[0]) == '1':
#                     imu_batch.append(sensor_data)
#                 elif str(sensor_data[0]) == '2':
#                     wifi_batch.append(sensor_data)
#                 elif str(sensor_data[0]) == '3':
#                     beacon_batch.append(sensor_data)
#
#             if not self.init_pos_flag and len(beacon_batch) == 0:
#                 print("at start time, there's no beacon data, so the localization system won't be able to init pos")
#                 continue
#
#             # fake algo logic written in python code for testing
#
#             print(f"[localization]: calculate done try to insert at {time.time()}")
#             position_with_ts = list(map(lambda e: e/len(beacon_batch), [sum_pos_x, sum_pos_y, sum_pos_z, sum_t]))
#             self.localization_output_q.put(position_with_ts)
#             print(f"[localization]: insert done at {time.time()}")
#             self.init_pos_flag = True
#             time.sleep(random.randint(50, 100) / 100)  # simulate actual calculation time
