from typing import List, Tuple
from collections import deque


class VelocityModule:
    # todo: adjust to three dimension
    def __init__(self, window_size, cal_fq):
        self.cal_fq = float(cal_fq)
        self.history_position = deque([], maxlen=int(window_size))
        self.history_ts = deque([], maxlen=window_size)
        self.latest_ts = 0

        self.last_velocity = (0., 0., 0.)

    def estimate_velocity(self, cur_pos: Tuple[float, float, float]) -> Tuple[float, float, float]:
        self.latest_ts += self.cal_fq            # accumulate time in self.latest_ts
        self.history_position.append(cur_pos)
        self.history_ts.append(self.latest_ts)
        res = self._calculate_velocity_using_least_square()
        self._normalized_ts()
        return res

    def _calculate_velocity_using_least_square(self) -> Tuple[float, float, float]:
        total_time_slot = len(self.history_position)
        if total_time_slot < 2:
            return 0., 0., 0.
        t_sum, t_square_sum, x_sum, y_sum, z_sum, tx_sum, ty_sum, tz_sum = 0, 0, 0, 0, 0, 0, 0, 0
        for i in range(total_time_slot):
            cur_t = self.history_ts[i] - self.history_ts[0]
            # cur_t = self.history_ts[i] - start_time  # it's ok to have same base time and it won't out of range
            x_sum += self.history_position[i][0]
            y_sum += self.history_position[i][1]
            z_sum += self.history_position[i][2]

            t_sum += cur_t
            t_square_sum += cur_t ** 2

            tx_sum += cur_t * self.history_position[i][0]
            ty_sum += cur_t * self.history_position[i][1]
            tz_sum += cur_t * self.history_position[i][2]
        try:
            t_mean, tx_mean, ty_mean, tz_mean = t_sum / total_time_slot, tx_sum / total_time_slot, ty_sum / total_time_slot, tz_sum / total_time_slot
            x_mean, y_mean, z_mean, t_square_mean = x_sum / total_time_slot, y_sum / total_time_slot, y_sum / total_time_slot, t_square_sum / total_time_slot

            cur_vel = (
                (tx_mean - t_mean * x_mean) / (t_square_mean - t_mean**2),
                (ty_mean - t_mean * y_mean) / (t_square_mean - t_mean**2),
                (tz_mean - t_mean * z_mean) / (t_square_mean - t_mean**2),
            )
            self.last_velocity = cur_vel
            return cur_vel
        except ZeroDivisionError:
            print("division by zero")
            print("history_position = ", self.history_position)
            print("history_ts = ", self.history_ts)
            return self.last_velocity

    def _normalized_ts(self):
#         print(f"before normalize {self.history_ts}")
#         print(f"before latest_ts = {self.latest_ts}")
        offset = self.history_ts[0]
        for i in range(len(self.history_ts)):
            self.history_ts[i] -= offset
        if len(self.history_ts) > 0:
            self.latest_ts = self.history_ts[-1]
#        print(f"after normalize {self.history_ts}")
#        print(f"after latest_ts = {self.latest_ts}")