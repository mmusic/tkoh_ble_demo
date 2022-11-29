import psycopg2
import logging
import json


class DataBaseConnector:

    def __init__(self, db_name='kowloonbay', db_usr='postgres', db_usr_psw='mtrec', db_host='127.0.0.1', db_port='7023'):
        self.database = db_name
        self.usr = db_usr
        self.psw = db_usr_psw
        self.host = db_host
        self.port = db_port
        self.conn = psycopg2.connect(database=self.database,
                                     user=self.usr,
                                     password=self.psw,
                                     host=self.host,
                                     port=self.port)

        self.tables = {'daily_log': {'id': "integer 自动增量 [nextval('daily_log_id_seq')]",
                                     'ts':	"bigint",
                                     'src_type': "text NULL",
                                     'content':	"text",  # note: in dict format
                                     'level':	"text NULL",
                                     'todo':	"smallint NULL",
                                     'solve_message': "text NULL", },

                       'beacon': {'id':	"integer 自动增量 [nextval('beacon_id_seq')]",
                                  'major':	"integer",
                                  'minor':	"integer",
                                  'x':	"double precision",
                                  'y':	"double precision",
                                  'z':	"double precision", },

                       'raw_beacon_data': {'id':	"integer 自动增量 [nextval('raw_beacon_data_id_seq')]",
                                           'vm':	"double precision",
                                           'mac':	"text NULL	baecon mac",
                                           'major':	"smallint",
                                           'minor':	"smallint",
                                           'rssi':	"smallint",
                                           'ts':	"bigint",
                                           'sensor':	"text	sensor ble mac", },

                       'heartbeat': {'id':	"integer 自动增量 [nextval('heartbeat_id_seq')]",
                                     'sensor':	"text	sensor ble mac",
                                     'vm':	"double precision NULL",
                                     'start_up':	"smallint NULL",
                                     'sys_status': "text NULL",  # note: in dict format.
                                     'ts':	"bigint", },

                       'raw_imu_data': {'id':	"integer 自动增量 [nextval('raw_imu_data_id_seq')]",
                                        'vm':	"double precision NULL",
                                        'sensor':	"text	sensor ble mac",
                                        'axis_1':	"double precision NULL",
                                        'axis_2':	"double precision NULL",
                                        'axis_3':	"double precision NULL",
                                        'axis_4':	"double precision NULL",
                                        'axis_5':	"double precision NULL",
                                        'axis_6':	"double precision NULL",
                                        'axis_7':	"double precision NULL",
                                        'axis_8':	"double precision NULL",
                                        'axis_9':	"double precision NULL",
                                        'ts':	"bigint", },

                       'raw_loc_data': {'id':	"integer 自动增量 [nextval('loc_online_data_id_seq')]",
                                        'sensor':	"text	sensor ble mac",
                                        'vm':	"double precision",
                                        'pos_x':	"double precision",
                                        'pos_y':	"double precision",
                                        'val_x':	"double precision",
                                        'val_y':	"double precision",
                                        'alarm':	"smallint",
                                        'ts':	"bigint",	},

                       'sensor': {'id':	"integer 自动增量 [nextval('sensor_id_seq')]",
                                  'sensor':	"text	unique, default bluetooth mac",
                                  'site':	"integer NULL	site code name",
                                  'label':	"integer NULL",
                                  'ts_create':	"bigint NULL",	},
                       }
        self.__table_examination()

    def __table_examination(self):
        # todo: check if the table is consistent with schema(at least with same key) or not, if not, write log a warning
        pass

    def insert_beacon_scan_data(self, **kwargs):
        vals = ''
        for k, v in kwargs.items():
            if type(v) is int or type(v) is float:
                vals += str(v) + ','
            else:
                vals += '\'' + str(v) + '\'' + ','
        vals = vals.strip(',')
        keys = ','.join(map(str, list(kwargs.keys())))
        sql = f"INSERT INTO raw_beacon_data ({keys}) VALUES ({vals})"
        self.conn.cursor().execute(sql)
        self.conn.commit()

    def insert_sensor_loc(self, **kwargs):
        vals = ''
        for k, v in kwargs.items():
            if type(v) is int or type(v) is float:
                vals += str(v) + ','
            elif type(v) is str:
                if '\'' in v:
                    vals += '\'' + str(v).replace('\'', '\'\'') + '\'' + ','  # note: quite tricky here.
                else:
                    vals += '\'' + str(v) + '\'' + ','
            else:
                print("invalid value type")
                return
        vals = vals.strip(',')
        keys = ','.join(map(str, list(kwargs.keys())))
        sql = f"INSERT INTO raw_loc_data ({keys}) VALUES ({vals})"
        # print(sql)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()

    def insert_beacon_battery(self, **kwargs):
        vals = ''
        for k, v in kwargs.items():
            if type(v) is int or type(v) is float:
                vals += str(v) + ','
            elif type(v) is str:
                if '\'' in v:
                    vals += '\'' + str(v).replace('\'', '\'\'') + '\'' + ','  # note: quite tricky here.
                else:
                    vals += '\'' + str(v) + '\'' + ','
            else:
                print("invalid value type")
                return
        vals = vals.strip(',')
        keys = ','.join(map(str, list(kwargs.keys())))
        sql = f"INSERT INTO raw_beacon_battery ({keys}) VALUES ({vals})"
        # print(sql)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()


    def insert_heartbeat(self, **kwargs):
        vals = ''
        for k, v in kwargs.items():
            if type(v) is int or type(v) is float:
                vals += str(v) + ','
            elif type(v) is str:
                if '\'' in v:
                    vals += '\'' + str(v).replace('\'', '\'\'') + '\'' + ','  # note: quite tricky here.
                else:
                    vals += '\'' + str(v) + '\'' + ','
            else:
                print("invalid value type")
                return
        vals = vals.strip(',')
        keys = ','.join(map(str, list(kwargs.keys())))
        sql = f"INSERT INTO heartbeat ({keys}) VALUES ({vals})"
        # print(sql)
        self.conn.cursor().execute(sql)
        self.conn.commit()

    def insert_imu_data(self, **kwargs):
        vals = ''
        for k, v in kwargs.items():
            if type(v) is int or type(v) is float:
                vals += str(v) + ','
            elif type(v) is str:
                if '\'' in v:
                    vals += '\'' + str(v).replace('\'', '\'\'') + '\'' + ','  # note: quite tricky here.
                else:
                    vals += '\'' + str(v) + '\'' + ','
            else:
                print("invalid value type")
                return
        vals = vals.strip(',')
        keys = ','.join(map(str, list(kwargs.keys())))
        sql = f"INSERT INTO raw_imu_data ({keys}) VALUES ({vals})"
        # print(sql)
        self.conn.cursor().execute(sql)
        self.conn.commit()

    def insert_log(self, **kwargs):
        vals = ''
        for k, v in kwargs.items():
            if type(v) is int or type(v) is float:
                vals += str(v) + ','
            elif type(v) is str:
                if '\'' in v:
                    vals += '\'' + str(v).replace('\'', '\'\'') + '\'' + ','  # note: quite tricky here.
                else:
                    vals += '\'' + str(v) + '\'' + ','
            else:
                print("invalid value type")
                return
        vals = vals.strip(',')
        keys = ','.join(map(str, list(kwargs.keys())))
        sql = f"INSERT INTO daily_log ({keys}) VALUES ({vals})"
        # print(sql)
        self.conn.cursor().execute(sql)
        self.conn.commit()

    def query_full_table(self, table_name, *key_name_list):
        query_key = ','.join(key_name_list)
        try:
            cursor = self.conn.cursor()
            sql = f"select {query_key} from {table_name }"
            cursor.execute(sql)
        except Exception as e:
            print(e)
            return None
        else:
            return cursor.fetchall()
        finally:
            self.conn.commit()

    def all_targets_last_seen_status(self, s_ts):
        try:
            cursor = self.conn.cursor()
            sql = f"select sensor, max(vm), max(pos_x), max(pos_y), max(pos_z), max(ts) from raw_loc_data where ts > {s_ts} GROUP BY sensor"
            cursor.execute(sql)
        except Exception as e:
            print(e)
            return None
        else:
            return cursor.fetchall()
        finally:
            self.conn.commit()

    def all_targets_last_seen_battery(self, s_ts):
        try:
            cursor = self.conn.cursor()
            sql = f"select beacon, max(battery), max(ts) from raw_beacon_battery where ts > {s_ts} GROUP BY beacon"
            cursor.execute(sql)
        except Exception as e:
            print(e)
            return None
        else:
            return cursor.fetchall()
        finally:
            self.conn.commit()

    def all_beacons(self):
        try:
            cursor = self.conn.cursor()
            sql = f"select * from beacon"
            cursor.execute(sql)
        except Exception as e:
            print(e)
            return None
        else:
            return cursor.fetchall()
        finally:
            self.conn.commit()

    def query_history_target_status(self, target_identifier, s_ts, e_ts):
        try:
            cursor = self.conn.cursor()
            sql = f"select sensor, pos_x, pos_y, pos_z, ts from raw_loc_data where sensor = '{target_identifier}' and ts >= {s_ts} and ts <= {e_ts} order by ts ASC"
            # print(sql)
            cursor.execute(sql)
        except Exception as e:
            print(e)
            return None
        else:
            return cursor.fetchall()
        finally:
            self.conn.commit()

if __name__ == "__main__":
    db_connect_info = {'db_usr': 'postgres',
                       'db_usr_psw': 'mtrec2020',
                       'db_host': '143.89.49.63',
                       'db_port': '7023',
                       'db_name': 'mtr_cms'}

    db = DataBaseConnector(**db_connect_info)
    data = db.query_full_table('sensor', 'id', 'sensor', 'site', 'label', 'ts_create')
    print(data)

# db.insert_beacon_scan_data(rssi=-80,
    #                            vm=1.1,
    #                            mac='xx:xx:xx:xx:xx:xx',
    #                            ts=1111111111,
    #                            major=12345,
    #                            minor=12345,
    #                            sensor='yy:yy:yy:yy:yy:yy',)

    # db.insert_heartbeat(sensor='yy:yy:yy:yy:yy:yy',
    #                     sys_status=str({'temperature': '56', 'imu_status': True}),
    #                     ts=1111111111,
    #                     vm=1.1,)

    # db.insert_log(ts=1111111111,
    #               src_type='sensor',
    #               content=str({'event_type': 'log_msg', 'level': 'warn', 'msg': 'test test test'}),
    #               level='warn', )

    # db.insert_imu_data(vm=1.1,
    #                    ts=111111111,
    #                    sensor='yy:yy:yy:yy:yy:yy',
    #                    axis_1=0.0,
    #                    axis_2=0.0,
    #                    axis_3=0.0,
    #                    axis_4=0.0,
    #                    axis_5=0.0,
    #                    axis_6=0.0,
    #                    axis_7=0.0,
    #                    axis_8=0.0,
    #                    axis_9=0.0, )

    # db.insert_sensor_loc(ts=11111111,
    #                      vm=1.1,
    #                      pos_x=0.0,
    #                      pos_y=0.0,
    #                      pos_z=0.0,
    #                      vel_x=0.0,
    #                      vel_y=0.0,
    #                      vel_z=0.0,
    #                      alarm=1,
    #                      sensor='yy:yy:yy:yy:yy:yy',
    #                     )
