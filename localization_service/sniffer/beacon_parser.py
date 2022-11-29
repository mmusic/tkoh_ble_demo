from common.data_type import BeaconValue
from typing import Union
from config.TKOH import TARGET_IDENTIFIER_SET



class BeaconParser:
    @staticmethod
    def check_deployed(manufacturer_data: str) -> bool:
        raise NotImplementedError

    @staticmethod
    def get_beacon_value(manufacturer_data: str,
                         rssi: Union[int, None],
                         mac: Union[int, None]) -> BeaconValue:
        # note: if manufacturer_data contains
        raise NotImplementedError


# [BEACON INFO DEFINITION]
class TKOHBeaconParser(BeaconParser):
    @staticmethod
    def _cmax_battery_voltage_transform(raw: int):
        k = raw * 0.1 + 1.9
        battery_voltage_to_battery_percentage_mapping = {
            1.9: '1%',
            2.0: '5%',
            2.1: '10%',

            2.2: '15%',
            2.3: '17%',
            2.4: '20%',

            2.5: '23%',
            2.6: '25%',
            2.7: '50%',

            2.8: '75%',
            2.9: '97%',
            3.0: '98%',

            3.1: '98%',
            3.2: '99%',
            3.3: '99%',
            3.4: '100%'
        }
        return battery_voltage_to_battery_percentage_mapping[k]

    @staticmethod
    def check_deployed(manufacturer_data: str) -> bool:
        # using uuid+major+minor to check if it's deployed
        manufacturer_data = manufacturer_data.lower()
        if len(manufacturer_data) == 90:
            uuid_major_minor = manufacturer_data[46: 86]
            if uuid_major_minor in TARGET_IDENTIFIER_SET:
                return True
            else:
                return False

    @staticmethod
    def get_beacon_value(manufacturer_data: str,
                         rssi: Union[int, None],
                         mac: Union[int, None]) -> BeaconValue:
        # if data not satisfied, will throw error
        assert len(manufacturer_data) == 90, f"beacon msg format is not valid in TKOH service: {manufacturer_data}"
        beacon_header = manufacturer_data[38:46].lower()
        mac = manufacturer_data[14:26] if mac is None else mac
        major = None
        minor = None
        uuid = None
        rssi = rssi
        battery = None
        tx_power = None

        # todo: potentially error occur, bc you have no way to filter out non-deployed beacon with same header(for CMAX)
        if beacon_header == '59000000':
        	# print('mmm----', manufacturer_data)
        	if manufacturer_data[50:52] != '00':
        		battery = f"{int(manufacturer_data[50: 52], 16)}%"
        elif beacon_header == '5a000315':
            battery = TKOHBeaconParser._cmax_battery_voltage_transform(int(manufacturer_data[72: 74], 16))
            major = manufacturer_data[78: 82]
            minor = manufacturer_data[82: 86]
        elif beacon_header == '4c000215':
            uuid_major_minor = manufacturer_data[46: 86]
            if uuid_major_minor in TARGET_IDENTIFIER_SET:
                uuid = manufacturer_data[46: 78]
                major = manufacturer_data[78: 82]
                minor = manufacturer_data[82: 86]
                rssi = int(manufacturer_data[88: 90], 16) - 0x100
                # print('rssi-----------------', rssi)
                # if rssi:
                # 	pass
                # else:
                # 	print('error------------', manufacturer_data)
            else:
                raise
        else:
            raise ValueError(f'Incorrect beacon header, manufacturer_data={manufacturer_data}')

        return BeaconValue(beacon_mac=mac,
                           rssi=rssi,
                           major=major,
                           minor=minor,
                           uuid=uuid,
                           tx_power=tx_power,
                           battery=battery,
                           )


if __name__ == "__main__":
    cmax_major = 1590
    cmax_minor = 91
    cmax_uuid = '771F4541E1BE43AAA8835A3ED4E2E15B'

    sg_major = 35072
    sg_minor = 19312
    sg_uuid = 'F000AAB004514000B000000000000000'

    print(len(sg_uuid))
    print(len(cmax_uuid))

    print(str(hex(cmax_major))[2:].zfill(4), str(hex(cmax_minor))[2:].zfill(4))
    print(str(hex(sg_major))[2:].zfill(4), str(hex(sg_minor))[2:].zfill(4))

