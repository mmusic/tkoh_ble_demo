from typing import List, Tuple, Dict
import configparser
from copy import deepcopy
import requests


class ConfigManager:
    def __init__(self, loc, url):
        self.table_url = url
        # print(r.content.decode())
        # self.cp_reader = configparser.ConfigParser()
        # print(root_cp)
        self.loc = loc
        self.refresh_table()


    def refresh_table(self):
        self.address_table = {}
        try:
            for site in self.loc:
                res = requests.get(self.table_url + site + '/addressTable' + site + '.cfg')
                filename = 'temp'
                with open(filename, 'w') as file_object:
                    file_object.write(res.content.decode())
                self.address_table[site] = self.read_beacon_table_cfg(filename)
        except Exception as e:
            print(e)

        # print(self.address_table)
        # return self.address_table
        # print(self.address_table['YMT'][1]['c9:1f:74:72:8f:d9'])


    def get_beacon_table(self) -> Dict:  # format: {mac_addr: ((pos_x, pos_y), idx)}
        return self.address_table


    def read_beacon_table_cfg(self, res):
        cp = configparser.ConfigParser()
        cp.read(res)
        beacon_address = cp.get('iBeacon_address', "beacons").split(';\n')  # get函数读取字典的的值
        num_of_beacon = len(beacon_address)
        beacon_addrs_list = []
        position_dict = {}
        for beacon in beacon_address:
            beaconOperator = beacon.split(',')  # 以逗号为分隔符
            address = beaconOperator[0]
            # beacon_addrs_list.append(address)
            try:
                positionX = float(beaconOperator[1])
                positionY = float(beaconOperator[2])
                tag = int(beaconOperator[3])
                t_address = {
                    'beacon': address,
                    'coor': [positionX, positionY, tag],
                    'status': 0,
                    'rssi': 0,
                    'ts': 0
                }
                beacon_addrs_list.append(t_address)
            except Exception as e:  # 读出錯誤類型以及詳細內容
                print("failed of construction of beacon addressTable, error with addressTable.cfg for reason below:")
                print(repr(e))  # 把某一类型的变量或者常量转换为字符串对象//str() 的输出追求可读性，输出格式要便于理解，适合用于输出内容到用户终端。
                # repr() 的输出追求明确性，除了对象内容，还需要展示出对象的数据类型信息，适合开发和调试阶段使用。
                break
        return beacon_addrs_list

# loc = ['KLB', 'YMT', 'CTL']
# c = ConfigManager(loc)
