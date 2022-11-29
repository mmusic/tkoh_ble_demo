import time
class BeaconMonitor:
    def __init__(self, cf, LOC):
        self.cf = cf.get_beacon_table()
        self.loc = LOC

    def update_status(self, mac, rssi, ts):
        for site in self.cf:
            if site != 'index':
                for index, v in enumerate(self.cf[site]):
                    if mac == v['beacon']:
                        self.cf[site][index]['status'] = 1
                        self.cf[site][index]['rssi'] = rssi
                        self.cf[site][index]['ts'] = ts
                        break

    def send_to_monitor(self, data):
        self.update_status(data[3], data[4], data[5])

    def get_cf(self):
        for site in self.cf:
            if site != 'index':
                for index, v in enumerate(self.cf[site]):
                    if (time.time() * 1000 - v['ts']) > 5 * 1000:
                        self.cf[site][index]['status'] = 0
        return self.cf
