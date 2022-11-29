import numpy as np
cimport numpy as np
import time
import json
import math
import cython
from libc.math cimport exp, pow, sqrt, M_PI

# input format


# output format
# {'target_identifier': target_ident,
#  'x': pos_with_ts[0],
#  'y': pos_with_ts[1],
#  'z': pos_with_ts[2],
#  'timestamp': pos_with_ts[3]}

cdef class LocalizationModule:

    cdef int num_of_particles
    cdef double delta_t
    cdef double cal_fq
    cdef int div_by_zero
    cdef int num_of_random_particles
    cdef double transition_model_max_vel, grid_size, weight_observe, weight_loss, pre_ts, cur_ts, var
    cdef double observation_model_mean[2]
    cdef double observation_model_var[2][2]
    cdef double loss_model_range[2]

    cdef double [:, :] particles_pos
    cdef double [:] particles_weights
    cdef double [:, :] beacon_positions
    cdef double [:] cur_rssi_info
    cdef double [:, :, :] regions
    cdef double [:, :] map_bound
    cdef int [:] num_of_pack

    def __init__(self, config_manager):
        localization_configs = config_manager.algo_config['localization']

        self.num_of_particles = int(localization_configs['num_of_particles'])
        self.transition_model_max_vel = float(localization_configs['max_vel'])

        self.observation_model_mean = json.loads(localization_configs['obs_model_mean'])
        self.observation_model_var = json.loads(localization_configs['obs_model_var'])
        self.var = self.observation_model_var[0][0] - pow(self.observation_model_var[0][1], 2) / self.observation_model_var[1][1]

        self.loss_model_range = json.loads(localization_configs['loss_model_range'])
        self.beacon_positions = self._init_beacon_positions(config_manager.beacon_table_config)

        self.grid_size = float(localization_configs['grid_size'])

        self.map_bound = np.array(json.loads(localization_configs['map_bound']), dtype=float)
        self.regions = np.array(json.loads(localization_configs['position_candidates_regions']), dtype=float)

        self._init_particles()

        self.weight_observe = float(localization_configs['weight_observe'])
        self.weight_loss = float(localization_configs['weight_loss'])

        self.delta_t = 0
        self.cal_fq = float(config_manager.root_config['TRACKING']['CAL_FQ'])

        self.pre_ts = time.time()
        self.cur_ts = time.time()

        self.div_by_zero = 0
        self.num_of_random_particles = 0

    cpdef estimate_position(self,
                            filtered_rssi,
                            cur_ts):
        self.delta_t += self.cal_fq
        if len(filtered_rssi) == 0:
            return tuple()

        rssi, num_of_pack = zip(*filtered_rssi)
        self.pre_ts = self.cur_ts
        self.cur_ts = cur_ts
        self.cur_rssi_info = np.array(rssi, dtype=float) # conver to Cython memoryViews
        self.num_of_pack = np.array(num_of_pack, dtype=int) # conver to Cython memoryViews

        # sample_start = time.time()
        self._do_sample()
        # sample_end = time.time()

        # weight_update_start = time.time()
        self._weight_update()
        # weight_update_end = time.time()

        # resample_start = time.time()
        self._do_resample()
        # resample_end = time.time()

        # cal_pos_start = time.time()
        cur_pos = self._caculate_position_via_samples()
        # cal_pos_end = time.time()

        #print(f"{self.particles_weights[:5]}")
        # #print(f"sample time = {sample_end - sample_start}, weight_updata time = {weight_update_end-weight_update_start}, cal_pos time = {cal_pos_end - cal_pos_start}, resample time = {resample_end - resample_start}")
        self.delta_t = 0
        return cur_pos

    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef _probagate_particles(self):
        cdef int i, max_distance_in_cur_step
        cdef double sum_time, pos_x, offset_x, pos_y, offset_y
        cdef int[:] rand_offset_x, rand_offset_y
        cdef bint within_range

        delta_t = self.delta_t
        if delta_t * self.transition_model_max_vel < self.grid_size:  # assume that it stay at the same place
            return
        else:
            max_distance_in_cur_step = int((delta_t * self.transition_model_max_vel) / self.grid_size)
            #print("inside probagate: delta_t = {}, max_distance = {}".format(delta_t, max_distance_in_cur_step))
            i = 0
            sum_time = 0
            rand_offset_x = np.random.random_integers(-max_distance_in_cur_step, max_distance_in_cur_step, self.num_of_particles)
            rand_offset_y = np.random.random_integers(-max_distance_in_cur_step, max_distance_in_cur_step, self.num_of_particles)

            while i < self.num_of_particles:
                pos_x = self.particles_pos[i, 0]
                pos_y = self.particles_pos[i, 1]
                offset_x = rand_offset_x[i]
                offset_y = rand_offset_y[i]
                tmp_x = pos_x + offset_x * self.grid_size
                tmp_y = pos_y + offset_y * self.grid_size
                within_range = self._particle_within_range(tmp_x, tmp_y)
                if within_range > 0:
                    self.particles_pos[i,0] = tmp_x
                    self.particles_pos[i,1] = tmp_y
                i += 1
            # ##print("out _probagate_particles")

    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    cdef bint _particle_within_range(self, double pos_x, double pos_y):
        cdef int region_num = self.regions.shape[0]
        cdef double p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y
        cdef double p1_p2_cross_product_p1_p, p3_p4_cross_product_p3_p, p1_p4_cross_product_p1_p, p3_p2_cross_product_p3_p
        cdef bint res = 0

        for i in range(region_num):
            p1_x = self.regions[i, 0, 0]
            p1_y = self.regions[i, 0, 1]
            p2_x = self.regions[i, 1, 0]
            p2_y = self.regions[i, 1, 1]
            p3_x = self.regions[i, 2, 0]
            p3_y = self.regions[i, 2, 1]
            p4_x = self.regions[i, 3, 0]
            p4_y = self.regions[i, 3, 1]

            p1_p2_cross_product_p1_p = (p1_x - p2_x) * (p1_y - pos_y) - (p1_y - p2_y) * (p1_x - pos_x)
            p3_p4_cross_product_p3_p = (p3_x - p4_x) * (p3_y - pos_y) - (p3_y - p4_y) * (p3_x - pos_x)

            p1_p4_cross_product_p1_p = (p1_x - p4_x) * (p1_y - pos_y) - (p1_y - p4_y) * (p1_x - pos_x)
            p3_p2_cross_product_p3_p = (p3_x - p2_x) * (p3_y - pos_y) - (p3_y - p2_y) * (p3_x - pos_x)
            res |= ((p1_p2_cross_product_p1_p * p3_p4_cross_product_p3_p) >= 0) & ((p1_p4_cross_product_p1_p * p3_p2_cross_product_p3_p) >= 0)
        return res

    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    cdef _do_sample(self):
        cdef double [:,:] new_particles_pos = self.particles_pos.copy()
        cdef int[:] rand_pos_idx = np.random.random_integers(0, self.num_of_particles-1, self.num_of_particles)

        ##print("in _do_sample")
        probagate_start = time.time()
        self._probagate_particles()
        probagate_end = time.time()

        sample_start = time.time()
        for i in range(self.num_of_particles):
            new_particles_pos[i, 0] = self.particles_pos[rand_pos_idx[i], 0]
            new_particles_pos[i, 1] = self.particles_pos[rand_pos_idx[i], 1]
        self.particles_pos[:] = new_particles_pos
        sample_end = time.time()
        #print(f"probagate time = {probagate_end - probagate_start}, sample time= {sample_end - sample_start}")

    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    cdef _weight_update(self):
        cdef double[:] updated_weights = self.particles_weights.copy()
        cdef double sum_of_weight = 0

        # update_cal_start = time.time()
        for idx in range(self.num_of_particles):  # propotion to num_of_particles * num_of_beacons
            pos = self.particles_pos[idx, :]
            updated_w = self._p_of_rssi_given_pos(pos)
            #####print("updated_weight = ", updated_w)
            sum_of_weight = sum_of_weight + updated_w
            updated_weights[idx] = updated_w
        # update_cal_end = time.time()
        # #print(f"update cal time = {update_cal_end - update_cal_start}")
        if sum_of_weight == 0.:
            self.div_by_zero = 1
            print("zero division error in Localization._weight_update")
        else:
            for idx in range(self.num_of_particles):
                updated_weights[idx] /= sum_of_weight
            self.particles_weights[:] = updated_weights
            self.div_by_zero = 0

    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    cdef double _p_of_rssi_given_pos(self, double[:] pos):
        cdef double p = 1
        cdef int len_of_rssi = self.cur_rssi_info.size
        cdef double rssi, distance
        cdef int num_of_pack

        for idx in range(len_of_rssi):
            rssi = self.cur_rssi_info[idx]
            num_of_pack = self.num_of_pack[idx]
            distance = self._distance(pos, self.beacon_positions[idx, :])
            p *= self._p_of_rssi_given_distance(rssi, num_of_pack, distance)
        return p

    cdef double _calculate_weight_loss(self, double distance):
        if distance < 5.:
            return self.weight_loss
        elif distance > 40.:
            return 0.99999
        else:
            return self.weight_loss + (1-self.weight_loss) / (40 - 5)

    @cython.cdivision(True)
    @cython.initializedcheck(False)
    cdef double _p_of_rssi_given_distance(self, double rssi, int num_of_pack, double distance):
        cdef double p_loss = 0, p_observe = 0

        if num_of_pack == 0:
            p_loss = 1 / (self.loss_model_range[1] - self.loss_model_range[0])

        rssi_mean = self.observation_model_mean[0]
        distance_mean = self.observation_model_mean[1]

        mean = rssi_mean + (distance - distance_mean) * self.observation_model_var[0][1]/ self.observation_model_var[1][1]
        p_observe = exp(-0.5*pow(rssi-mean, 2) / self.var) / sqrt(self.var * 2 * M_PI)

        weight_loss = self._calculate_weight_loss(distance)

        return (1 - weight_loss) * self.weight_observe * p_observe + weight_loss * self.weight_loss * p_loss

    @cython.boundscheck(False)
    cdef double _distance(self, double[:] pos1, double[:] pos2):
        return sqrt(pow(pos1[0]-pos2[0],2) + pow(pos1[1]-pos2[1], 2))

    cdef tuple _caculate_position_via_samples(self):
        cdef int n
        cdef double cur_pos_x = 0, cur_pos_y = 0
        n = self.particles_weights.size
        #print(f"size_of_particle_weighs={n}")
        for i in range(n):
            pos_x = self.particles_pos[i, 0]
            pos_y = self.particles_pos[i, 1]
            weight = self.particles_weights[i]
            cur_pos_x += weight * pos_x
            cur_pos_y += weight * pos_y
            #print(f"prev_pos=({pos_x}, {pos_y})")
            #print(f"{weight}")
            #print(f"cur_pos=({cur_pos_x}, {cur_pos_y})")
        return tuple([cur_pos_x, cur_pos_y])

    @cython.boundscheck(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef double[:] _sample_pos_given_measurement(self):
        cdef int max_rssi_idx = 0
        cdef int len_of_rssi = self.cur_rssi_info.size
        cdef int failure_counts = 0
        cdef double pos[2]
        cdef double beacon_pos_x, beacon_pos_y
        cdef double sample_offset_x, sample_offset_y, _mean_of_distance_given_rssi, _var_of_distance_given_rssi, max_rssi

        # find a beacon with max rssi and sample one pos around it
        for i in range(len_of_rssi):
            if self.cur_rssi_info[max_rssi_idx] < self.cur_rssi_info[i]:
                max_rssi_idx = i
        max_rssi = self.cur_rssi_info[max_rssi_idx]

        beacon_pos_x = self.beacon_positions[max_rssi_idx, :][0]
        beacon_pos_y = self.beacon_positions[max_rssi_idx, :][1]

        rssi_mean = self.observation_model_mean[0]
        distance_mean = self.observation_model_mean[1]

        _mean_of_distance_given_rssi = distance_mean + (max_rssi - rssi_mean) * self.observation_model_var[0][1] / self.observation_model_var[0][0]
        _var_of_distance_given_rssi = self.observation_model_var[1][1] - (self.observation_model_var[0][1] ** 2) / self.observation_model_var[0][0]
        sample_offset_x = np.random.normal(_mean_of_distance_given_rssi, _var_of_distance_given_rssi, 1)[0]
        sample_offset_y = np.random.normal(_mean_of_distance_given_rssi, _var_of_distance_given_rssi, 1)[0]

        failure_counts = 0
        while 1:
            pos_x = sample_offset_x + beacon_pos_x
            pos_y = sample_offset_y + beacon_pos_y
            if self._particle_within_range(pos_x, pos_y):
                pos[0] = pos_x
                pos[1] = pos_y
                return pos
            failure_counts += 1
            if failure_counts > 30:
                failure_counts = 0
                sample_offset_x = np.random.normal(_mean_of_distance_given_rssi, _var_of_distance_given_rssi, 1)[0]
                sample_offset_y = np.random.normal(_mean_of_distance_given_rssi, _var_of_distance_given_rssi, 1)[0]
            ##print(f"sample distance = {sample_distance}, {angle}, {pos_x, pos_y}")

    cdef _do_resample(self):
        ##print("in _do_resample")
        cdef double [:, :] new_particles_pos = self.particles_pos.copy()
        cdef double[:] random_pos
        cdef int i = 0
        cdef double [:] cumsum
        cdef double threshold

        #print(f"1 old_particles_pos = {new_particles_pos[5, 0], new_particles_pos[5, 1]}")
        if self.div_by_zero == 1:
            self.num_of_random_particles = 100
            for j in range(self.num_of_random_particles):
                random_pos = self._sample_pos_given_measurement()
                new_particles_pos[j, 0] = random_pos[0]
                new_particles_pos[j, 1] = random_pos[1]
                # #rint(f"random_pos = {random_pos[0], random_pos[1]}")
        else:
            self.num_of_random_particles = 0

        cumsum = np.cumsum([weight for weight in self.particles_weights])
        threshold = np.random.uniform(0., 1./self.num_of_particles)
        for j in range(self.num_of_random_particles, self.num_of_particles):  # restrict len(self.particles) = self.num_pf_particles
            while threshold > cumsum[i]:
                i += 1
            new_particles_pos[j, 0] = self.particles_pos[i, 0]
            new_particles_pos[j, 1] = self.particles_pos[i, 1]
            threshold += 1./self.num_of_particles

        #print(f"1 new_particles_pos = {new_particles_pos[5, 0], new_particles_pos[5, 1]}")
        #print(f"1 new_particles_weights = {self.particles_weights[5]}")
        self.particles_pos[...] = new_particles_pos
        self.particles_weights[...] = 1. / self.num_of_particles
        # #print(f"{1/self.num_of_particles}")
        #print(f"1 new_particles_weights = {self.particles_weights[5]}")
        ####print("after resample = ", self.particles)

    cdef _init_particles(self): # return to Cython memoryViews
        position_candidates = self._init_position_candidates()  # set(Tuple[float, float])
        weights = [1./self.num_of_particles] * self.num_of_particles
        particles_pos = []
        for i in range(self.num_of_particles):
            sample_idx = np.random.randint(0, len(position_candidates))
            particles_pos.append(position_candidates[sample_idx])
        tmp_particles_pos = np.array(particles_pos, dtype=float)
        tmp_particles_weights = np.array(weights, dtype=float)
        #print(tmp_particles_pos[:5])
        #print(tmp_particles_weights[:5])
        self.particles_pos = np.array(particles_pos, dtype=float)
        self.particles_weights = np.array(weights, dtype=float)

    cdef _init_beacon_positions(self, beacon_table_info): # return to Cython memoryViews
        res = []
        _, beacon_addrs_list, position_dict = beacon_table_info
        for beacon_addr in beacon_addrs_list:
            res.append(list(position_dict[beacon_addr][0]))
        return np.array(res, dtype=float)

    def _init_position_candidates(self): # return python obj
        res = []
        x_min = self.map_bound[0, 0]
        x_max = self.map_bound[0, 1]
        y_min = self.map_bound[1, 0]
        y_max = self.map_bound[1, 1]
        x, y = x_min, y_min
        while x < x_max:
            while y < y_max:
                if self._particle_within_range(x, y):
                    res.append((x, y))
                y += self.grid_size
            y = y_min
            x += self.grid_size
        return res