from typing import List, Tuple, Union, Dict
import time
import math
import numpy as np
from collections import defaultdict


class LocalizationModule:
    def __init__(self,
                 algo_params: Union[Dict, None] = None,
                 map_constraints: Union[List[List[Tuple[float, float, float]]], None] = None):
        # print("init localizationModule")
        if algo_params is None:
            algo_params = {
                'num_of_particles': 800,
                'max_vel': 2.,  # maximum speed of human, unit in m/s
                'obs_model_mean': [-76.0656, 2.8871],  # mean and variance of P(rssi, distance)
                'obs_model_var': [[53.171, -5.218], [-5.218, 2.912]],
                'loss_model_range': [-120, -110],
                'weight_observe': 0.8,  # mean and variance of P(rssi, distance)
                'weight_loss': 1 - 0.8,
                'grid_size': 0.5,
            }

        self.all_map_constraints = defaultdict(list)
        self.map_constraints = None
        for polygon in map_constraints:
            floor = polygon[0][2]
            self.all_map_constraints[floor].append(polygon)

        self.num_of_particles = int(algo_params['num_of_particles'])
        self.transition_model_max_vel = float(algo_params['max_vel'])

        self.observation_model_mean = algo_params['obs_model_mean']
        self.observation_model_var = algo_params['obs_model_var']
        self.var = self.observation_model_var[0][0] - (self.observation_model_var[0][1] ** 2) / self.observation_model_var[1][1]

        self.loss_model_range = algo_params['loss_model_range']

        self.grid_size = float(algo_params['grid_size'])

        self.particles = None  # List[Tuple[float, float, float], float]

        self.weight_observe = float(algo_params['weight_observe'])
        self.weight_loss = float(algo_params['weight_loss'])

        self.cur_rssi_info = None
        self.pre_ts = None
        self.cur_ts = None
        # self.delta_t = 0
        # self.cal_period = float(config_manager.root_config['TRACKING']['CAL_FQ'])  # todo: hard to decide whether drop it or not

        self.div_by_zero = False
        self.num_of_random_particles = 0

        self.floor = None

    def estimate_position(self,
                          beacon_data_batch: Union[List[Dict], None],
                          imu_data_batch: Union[List[Dict], None],
                          wifi_data_batch: Union[List[Dict], None]) -> Dict:  # {'x', 'y', 'z', 'timestamp'}
        # todo: not able to handle 3d positioning
        ##print("in estimate_position")
        # self.delta_t += self.cal_period  # todo
        if not beacon_data_batch and not imu_data_batch and not wifi_data_batch:
            return {'x': None, 'y': None, 'z': None, 'timestamp': time.time()}
        if not self.particles and not beacon_data_batch:
            return {'x': None, 'y': None, 'z': None, 'timestamp': time.time()}

        beacon_data_batch = sorted(beacon_data_batch, key=lambda d: d['timestamp'])
        beacon_data_batch_ts_list = [d['timestamp'] for d in beacon_data_batch]
        # print(beacon_data_batch_ts_list)
        self.pre_ts = self.cur_ts if self.cur_ts else beacon_data_batch[-1]['timestamp']
        self.cur_ts = beacon_data_batch[-1]['timestamp']
        self.cur_rssi_info = beacon_data_batch
        cur_z = beacon_data_batch[0]['source']['source_pos']['z']
        self.map_constraints = self.all_map_constraints[cur_z]

        if self.floor != cur_z:
            self.particles = None
        self.floor = cur_z

        if not self.particles:
            # note: duplicate gateway pos will not remove, the more possible particles init around it.
            anchor_points_with_range = []
            for beacon_data in self.cur_rssi_info:
                x, y = beacon_data['source']['source_pos']['x'], beacon_data['source']['source_pos']['y']
                anchor_points_with_range.append(((x, y), 30))  # todo: radius is related to position type
            # print(f"target_identifier: {beacon_data_batch[0]['target_identifier']}")
            self.particles = self._init_particles(num_of_particles=self.num_of_particles,
                                                  anchor_points_with_init_range=anchor_points_with_range)
        else:
            sample_start = time.time()
            self._do_sample()
            sample_end = time.time()

            weight_update_start = time.time()
            self._weight_update()
            weight_update_end = time.time()

            resample_start = time.time()
            self._do_resample()
            resample_end = time.time()

            self.div_by_zero = False

        # cal_pos_start = time.time()
        # todo: even if all particles are within map constraints, not guarantee that final result is within polygons
        cur_x, cur_y = self._caculate_position_via_particles()
        # cal_pos_end = time.time()
        # try:
        #     print(f"sample time = {sample_end - sample_start:.2f}, weight_updata time = {weight_update_end-weight_update_start:.2f}, cal_pos time = {cal_pos_end - cal_pos_start:.2f}, resample time = {resample_end - resample_start:.2f}")
        # except Exception as e:
        #     print('error', e)
        # self.delta_t = 0
        return {'x': cur_x, 'y': cur_y, 'z': cur_z, 'timestamp': self.cur_ts}

    def _weight_update(self):
        #print("in weight_update")
        sum_of_weight = 0.
        updated_weights = []
        # update_cal_start = time.time()
        for idx in range(self.num_of_particles):  # propotion to num_of_particles * num_of_beacons
            pos, w = self.particles[idx]
            updated_w = self._p_of_rssi_given_pos(pos)
            ###print("updated_weight = ", updated_w)
            sum_of_weight = sum_of_weight + updated_w
            updated_weights.append(updated_w)
        # update_cal_end = time.time()
        #print(f"update cal time = {update_cal_end - update_cal_start}")
        try:
            for idx in range(self.num_of_particles):
                updated_weights[idx] /= sum_of_weight
            for idx in range(self.num_of_particles):
                self.particles[idx] = (self.particles[idx][0], updated_weights[idx])
        except ZeroDivisionError:
            # kidnap happens
            self.div_by_zero = True
            print("ZeroDivisionError")

    # def _sample_pos_given_measurement(self):
    #     # todo: any better solution on when and how to get random samples?
    #     # find a beacon with max rssi and sample one pos around it
    #     max_rssi_idx = self.cur_rssi_info.index(max(self.cur_rssi_info, key=lambda d: d['value']['rssi']))
    #     max_rssi = self.cur_rssi_info[max_rssi_idx]['value']['rssi']
    #
    #     beacon_pos = self.beacon_positions[max_rssi_idx]
    #
    #     rssi_mean, distance_mean = self.observation_model_mean
    #
    #     _mean_of_distance_given_rssi = distance_mean + (max_rssi - rssi_mean) * self.observation_model_var[0][1] / self.observation_model_var[0][0]
    #     _var_of_distance_given_rssi = self.observation_model_var[1][1] - (self.observation_model_var[0][1] ** 2) / self.observation_model_var[0][0]
    #     sample_distance = np.random.normal(_mean_of_distance_given_rssi, _var_of_distance_given_rssi, 1)[0]
    #
    #     failure_counts = 0
    #     while 1:
    #         angle = np.random.randint(0, 10) * 36
    #         pos_x = math.cos(angle) * sample_distance + beacon_pos[0]
    #         pos_y = math.sin(angle) * sample_distance + beacon_pos[1]
    #         if self._particle_within_range((pos_x, pos_y)):
    #             return pos_x, pos_y
    #         failure_counts += 1
    #         if failure_counts > 30:
    #             failure_counts = 0
    #             sample_distance = np.random.normal(_mean_of_distance_given_rssi, _var_of_distance_given_rssi, 1)[0]
    #             #print(f"sample distance = {sample_distance}, {angle}, {pos_x, pos_y}")

    def _do_resample(self):
        new_particles = []
        if self.div_by_zero:
            self.num_of_random_particles = 100
            # print(f"random_choice = {random_choice}")
            print(f"random_particle_nums = {self.num_of_random_particles}")
            # for i in range(self.num_of_random_particles):
            #     random_pos = self._sample_pos_given_measurement()
            #     new_particles.append((random_pos, 0))
            anchor_points_with_init_range = []
            for beacon_data in self.cur_rssi_info:
                x, y = beacon_data['source']['source_pos']['x'], beacon_data['source']['source_pos']['y']
                rssi = beacon_data['value']['rssi']
                rssi_mean, distance_mean = self.observation_model_mean
                _mean_of_distance_given_rssi = distance_mean + (rssi - rssi_mean) * self.observation_model_var[0][1] / self.observation_model_var[0][0]
                _var_of_distance_given_rssi = self.observation_model_var[1][1] - (self.observation_model_var[0][1] ** 2) / self.observation_model_var[0][0]
                sample_distance = np.random.normal(_mean_of_distance_given_rssi, _var_of_distance_given_rssi, 1)[0]
                anchor_points_with_init_range.append(((x, y), sample_distance))

            # note: weight here will be updated later in this func
            new_particles = self._init_particles(num_of_particles=self.num_of_particles,
                                                 anchor_points_with_init_range=anchor_points_with_init_range)
        else:
            self.num_of_random_particles = 0

        if self.num_of_random_particles < len(self.particles):
            sum_of_weight = sum([w for _, w in self.particles])
            for idx in range(len(self.particles)):
                self.particles[idx] = (self.particles[idx][0], self.particles[idx][1] / sum_of_weight)
            cumsum = np.cumsum([weight for _, weight in self.particles])
            threshold = np.random.uniform(0., 1./len(self.particles))
            # print(f"{len(cumsum)}")
            # print(f"{len(self.particles)}")
            i = 0
            for j in range(len(self.particles) - self.num_of_random_particles):  # propotion to num_of_particles
                while threshold > cumsum[i]:
                    i += 1
                # meaning that the pointer is within the range
                new_particles.append((self.particles[i][0], 0))
                threshold += 1./len(self.particles)
                # print(f"j = {j}, threshold={threshold}")

        for i in range(len(new_particles)):
            new_particles[i] = (new_particles[i][0], 1. / len(new_particles))

        self.particles = new_particles
        ##print("after resample = ", self.particles)

    def _do_sample(self):
        ##print("in _do_sample")
        # probagate_start = time.time()
        self._propagate_particles()
        # probagate_end = time.time()

        ##print("after probagate", self.particles)
        new_particles = []
        # sample_start = time.time()
        for i in range(self.num_of_particles): # propotion to num_of_particles
            new_particles.append(self.particles[np.random.randint(0, self.num_of_particles)])
        self.particles = new_particles
        # sample_end = time.time()
        # #print(f"probagate time = {probagate_end - probagate_start}, sample time= {sample_end - sample_start}")
        ##print("after sample", self.particles)

    def _caculate_position_via_particles(self) -> Tuple[float, float]:
        # todo: 3d pos not able to calculate
        ##print("in _calculate_weight_loss")
        # here, we may compute a pos outside pos candidate regions
        cur_pos = [0., 0.]
        for pos, weight in self.particles:
            cur_pos[0] += weight * pos[0]
            cur_pos[1] += weight * pos[1]
        ##print("5 particles=", self.particles[:5])
        return cur_pos[0], cur_pos[1]

    def _distance(self, pos1, pos2, pos_type):
        # todo: different pos type
        return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)

    def _p_of_rssi_given_pos(self, pos: Tuple[float, float]):
        p = 1
        for data in self.cur_rssi_info:
            rssi, num_of_pack = data['value']['rssi'], 1
            x, y, z = data['source']['source_pos']['x'], data['source']['source_pos']['y'], data['source']['source_pos']['z']
            pos_type = data['source']['source_pos']['pos_type']
            distance = self._distance(pos, (x, y, z), pos_type)
            p *= self._p_of_rssi_given_distance(rssi, num_of_pack, distance)
        return p

    def _calculate_weight_loss(self, distance):
        if distance < 5.:
            return self.weight_loss
        elif distance > 40.:
            return 0.9999  # though it's almost impossible, but i can't write down 1, which will lead to zero division error
        else:
            return self.weight_loss + (1-self.weight_loss) / (40 - 5)

    def _p_of_rssi_given_distance(self, rssi, num_of_pack, distance):
        p_loss = 0
        if num_of_pack == 0:  # todo: what's this?
            p_loss = 1. / (self.loss_model_range[-1] - self.loss_model_range[-2])

        rssi_mean, distance_mean = self.observation_model_mean
        mean = rssi_mean + (distance-distance_mean)*self.observation_model_var[0][1]/self.observation_model_var[1][1]
        var = self.var
        p_observe = math.exp(-0.5*(rssi-mean)**2 / var) / math.sqrt(var * 2 * math.pi)

        weight_loss = self._calculate_weight_loss(distance)
        return (1 - weight_loss) * self.weight_observe * p_observe + weight_loss * self.weight_loss * p_loss

    def _init_particles(self,
                        num_of_particles,
                        anchor_points_with_init_range: List[Tuple[Tuple[float, float], float]] = None) -> List[Tuple[Tuple[float, float], float]]:
        # todo: 3d initialization
        position_candidates = self._init_position_candidates(anchor_points_with_init_range)
        particles = []
        for i in range(num_of_particles):
            # print(len(position_candidates))
            sample_idx = np.random.randint(0, len(position_candidates))
            particles.append((position_candidates[sample_idx], 1/num_of_particles))
        return particles

    def _propagate_particles(self):
        delta_t = self.cur_ts - self.pre_ts
        if delta_t * self.transition_model_max_vel < self.grid_size:  # assume that it stay at the same place
            print(f'not able to propagate: {delta_t * self.transition_model_max_vel}')
            return
        else:
            max_distance_in_cur_step = int((delta_t * self.transition_model_max_vel) // self.grid_size)
            ##print("inside probagate: delta_t = {}, max_distance = {}".format(delta_t, max_distance_in_cur_step))
            i = 0
            while i < self.num_of_particles:
                # #print("inside probagate")
                # start = time.time()
                pos, _ = self.particles[i]
                offset_x = np.random.randint(-max_distance_in_cur_step, max_distance_in_cur_step)
                offset_y = np.random.randint(-max_distance_in_cur_step, max_distance_in_cur_step)
                tmp_x, tmp_y = pos[0] + offset_x * self.grid_size, pos[1] + offset_y * self.grid_size
                for polygon in self.map_constraints:
                    if self._particle_within_range((tmp_x, tmp_y), polygon):
                        self.particles[i] = ((tmp_x, tmp_y), self.particles[i][1])
                i += 1

    def _init_position_candidates(self,
                                  anchor_points_with_init_range: List[Tuple[Tuple[float, float], float]] = None) -> List[Tuple[float, float]]:
        # todo: 3d initialization
        init_start = time.time()
        res = []
        if not anchor_points_with_init_range:
            if self.map_constraints:
                print(1234)
                x_min, x_max, y_min, y_max = -10000000000, 10000000000, -10000000000, 10000000000  # note: pay attention
                for p1, p2, p3, p4 in self.map_constraints:
                    x_min = min(p1[0], p2[0], p3[0], p4[0], x_min)
                    y_min = min(p1[1], p2[1], p3[1], p4[1], y_min)
                    x_max = max(p1[0], p2[0], p3[0], p4[0], x_max)
                    y_max = max(p1[1], p2[1], p3[1], p4[1], y_max)
                    for polygon in self.map_constraints:
                        res += self._2d_polygon_intersect_points(x_min=x_min,
                                                                 y_min=y_min,
                                                                 x_max=x_max,
                                                                 y_max=y_max,
                                                                 grid_size=self.grid_size,
                                                                 polygon=polygon)
            else:
                raise ValueError("Have neither map constraints nor anchor points, can't init particles!")
        else:
            if self.map_constraints:
                for anchor_point, radius in anchor_points_with_init_range:
                    x, y = anchor_point[0], anchor_point[1]
                    x_min, x_max, y_min, y_max = x - radius, x + radius, y - radius, y + radius
                    for polygon in self.map_constraints:
                        res += self._2d_polygon_intersect_points(x_min=x_min,
                                                                 y_min=y_min,
                                                                 x_max=x_max,
                                                                 y_max=y_max,
                                                                 grid_size=self.grid_size,
                                                                 polygon=polygon)   # todo: pay attention to the situation that no intersection at all
            else:
                for anchor_point, radius in anchor_points_with_init_range:
                    x, y = anchor_point[0], anchor_point[1]
                    x_min, x_max, y_min, y_max = x - radius, x + radius, y - radius, y + radius
                    x, y = x_min, x_max
                    while x < x_max:
                        while y < y_max:
                            res.append((x, y))
                            x, y = x + self.grid_size, y + self.grid_size
        init_end = time.time()
        print(f"init time = {init_end - init_start}")
        # print(f'position_candidates = {res}')
        return res

    @staticmethod
    def _2d_polygon_intersect_points(x_min, y_min, x_max, y_max, grid_size, polygon) -> List:
        res = []
        x, y = x_min, y_min
        while x < x_max:
            while y < y_max:
                if LocalizationModule._particle_within_range((x, y), polygon):
                    res.append((x, y))
                y += grid_size
            y = y_min
            x += grid_size
        return res

    @staticmethod
    def _particle_within_range(pos: Tuple[float, float],
                               polygon: List[Tuple[float, float, float]]) -> bool:
        # todo: not 3d checking
        # todo: should at least consider polygon in different floors
        res = False

        p1, p2, p3, p4 = polygon
        p1_p2_cross_product_p1_p = (p1[0] - p2[0]) * (p1[1] - pos[1]) - (p1[1] - p2[1]) * (p1[0] - pos[0])
        p3_p4_cross_product_p3_p = (p3[0] - p4[0]) * (p3[1] - pos[1]) - (p3[1] - p4[1]) * (p3[0] - pos[0])

        p1_p4_cross_product_p1_p = (p1[0] - p4[0]) * (p1[1] - pos[1]) - (p1[1] - p4[1]) * (p1[0] - pos[0])
        p3_p2_cross_product_p3_p = (p3[0] - p2[0]) * (p3[1] - pos[1]) - (p3[1] - p2[1]) * (p3[0] - pos[0])
        res |= (p1_p2_cross_product_p1_p * p3_p4_cross_product_p3_p >= 0) and (p1_p4_cross_product_p1_p * p3_p2_cross_product_p3_p >= 0)
        return res

