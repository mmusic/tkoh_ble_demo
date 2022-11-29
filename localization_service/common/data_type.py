from typing import Union


class DictStringify:
    def __str__(self):
        def _helper(obj):
            res = {}
            for k, v in vars(obj).items():
                if isinstance(v, DictStringify):
                    res[k] = _helper(v)
                else:
                    res[k] = v
            return res
        res = _helper(self)
        return str(res)


class SensorValue(DictStringify):
    pass


class Position(DictStringify):
    def __init__(self, x: float, y: float, z: float, timestamp: float, pos_type: int):
        self._x = x
        self._y = y
        self._z = z
        self._timestamp = timestamp
        self._pos_type = pos_type

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def pos_type(self):
        return self._pos_type


class SourceInfo(DictStringify):
    # note: the naming of class is not that good, it can hold much more information, take MTR project as an example
    def __init__(self,
                 source_identifier: str,
                 source_pos: Union[Position, None]):
        self._source_identifier = source_identifier
        self._source_pos = source_pos

    @property
    def source_identifier(self):
        return self._source_identifier

    @property
    def source_pos(self):
        return self._source_pos


class IMUValue(SensorValue):
    def __init__(self,
                 acc_x: float, acc_y: float, acc_z: float,
                 gyro_x: float, gyro_y: float, gyro_z: float,
                 mag_x: float, mag_y: float, mag_z: float):
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.acc_z = acc_z
        self.gyro_x = gyro_x
        self.gyro_y = gyro_y
        self.gyro_z = gyro_z
        self.mag_x = mag_x
        self.mag_y = mag_y
        self.mag_z = mag_z


class BeaconValue(SensorValue):
    def __init__(self,
                 beacon_mac: str,
                 rssi: Union[int, None],
                 major: Union[str, None],
                 minor: Union[str, None],
                 uuid: Union[str, None],
                 tx_power: Union[str, None],
                 battery: Union[str, None],
                 **kwargs
                 ):
        self._beacon_mac = beacon_mac
        self._rssi = rssi
        self._major = major
        self._minor = minor
        self._uuid = uuid
        self._tx_power = tx_power
        self._battery = battery
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def beacon_mac(self):
        return self._beacon_mac

    @property
    def rssi(self):
        return self._rssi

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def uuid(self):
        return self._uuid

    @property
    def tx_power(self):
        return self._tx_power

    @property
    def battery(self):
        return self._battery


class WIFIValue(SensorValue):
    def __init__(self, wifi_mac: str, rssi: int):
        self._wifi_mac = wifi_mac
        self._rssi = rssi

    @property
    def wifi_mac(self):
        return self._wifi_mac

    @property
    def rssi(self):
        return self._rssi


class SensorDataPackage(DictStringify):
    def __init__(self, target_identifier: str, data_type: str, value: SensorValue, timestamp: float, **kwargs):
        self._target_identifier = target_identifier
        self._data_type = data_type
        self._value = value
        self._timestamp = timestamp
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def value(self):
        return self._value

    @property
    def target_identifier(self):
        return self._target_identifier

    @property
    def data_type(self):
        return self._data_type

    @property
    def timestamp(self):
        return self._timestamp


class IMUDataPackage(SensorDataPackage):
    def __init__(self,
                 target_identifier: str,
                 value: IMUValue,
                 timestamp: float,
                 **kwargs):
        super(IMUDataPackage, self).__init__(target_identifier=target_identifier,
                                             data_type='1',
                                             value=value,
                                             timestamp=timestamp,
                                             **kwargs)


class WIFIDataPackage(SensorDataPackage):
    def __init__(self,
                 target_identifier: str,
                 value: WIFIValue,
                 timestamp: float,
                 source: SourceInfo,
                 **kwargs):
        super(WIFIDataPackage, self).__init__(target_identifier=target_identifier,
                                              data_type='2',
                                              value=value,
                                              timestamp=timestamp,
                                              **kwargs)
        self._source = source

    @property
    def source(self):
        return self._source


class BeaconDataPackage(SensorDataPackage):
    def __init__(self,
                 target_identifier: str,
                 value: BeaconValue,
                 timestamp: float,
                 source: SourceInfo,
                 **kwargs
                 ):
        super(BeaconDataPackage, self).__init__(target_identifier=target_identifier,
                                                data_type='3',
                                                value=value,
                                                timestamp=timestamp,
                                                **kwargs)
        self._source = source

    @property
    def source(self):
        return self._source


class LogMessage(DictStringify):
    def __init__(self, level: str, msg: str, **kwargs):
        self._level = level
        self._msg = msg

    @property
    def level(self):
        return self._level

    @property
    def msg(self):
        return self._msg


if __name__ == "__main__":
    print(LogMessage(level='error', msg="test"))
    print(SensorValue())

