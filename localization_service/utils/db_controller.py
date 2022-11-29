import psycopg2
import time
from collections import defaultdict
"""
:description
get data from database server

:arg
host, port, user, password, database

Usage::
    >>> import db_controller.DataBaseController
    >>> (for db='kowloonbay')get_raw_beacon_data_phase2(device=1001, s_ts=1589955595910, e_ts=1589955599910)
    >>> (for db='kowloonbay')get_raw_loc_data_phase2(device=1001, s_ts=1589955595910, e_ts=1589955599910)
    >>> (for db='kowloonbay')insert_reporting_phase2(
    #                    sensor='1001',
    #                    shop_name='MX',
    #                    shop_id='K9a',
    #                    delivery_date='2020-20-20',
    #                    time_period='88:88:88-88:88:88',
    #                    alert='Y',
    #                    alert_time='99:99:99-99:99:99,88:88:88-88:88:88',
    #                    score='0.9',
    #                    warning='unreasonable',
                         ts=server_ts,
                         process_seq=process_name,
                         flag=default 1)
    >>> ToDo (for db='mtr_cms')get_raw_beacon_data 
    >>> ToDo (for db='mtr_cms')insert_reporting 
"""


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
                                     'todo':	"smallint NULL,  null for not a todo, 0 for todo, 1 for done",
                                     'solve_message': "text NULL", },

                       'beacon': {'id':	"integer 自动增量 [nextval('beacon_id_seq')]",
                                  'major':	"integer",
                                  'minor':	"integer",
                                  'uuid':	"text NULL",
                                  'beacon': "text	beacon mac",
                                  'vendor': "text NULL",
                                  },

                       'heartbeat': {'id':	"integer 自动增量 [nextval('heartbeat_id_seq')]",
                                     'sensor':	"text	sensor ble mac",
                                     'vm':	"double precision NULL",
                                     'start_up':	"smallint NULL",
                                     'sys_status': "text NULL",  # note: in dict format.
                                     'ts':	"bigint", },

                       'polygon': {'id': "integer 自动增量 [nextval('polygon_id_seq')]",
                                   'site': "integer	site code name",
                                   'floor': "integer	floor code name",
                                   'poly': "integer	poly index",
                                   'vertex': "text NULL	",
                                   'geojson':	"text NULL",
                                   'label':	"text NULL",
                                   'ts_create':	"bigint NULL",
                                   'flag':	"smallint NULL	delete flag",
                       },

                       'raw_beacon_data': {'id':	"integer 自动增量 [nextval('raw_beacon_data_id_seq')]",
                                           'vm':	"double precision",
                                           'beacon':	"text NULL	baecon mac",
                                           'major':	"smallint",
                                           'minor':	"smallint",
                                           'rssi':	"smallint",
                                           'ts':	"bigint",
                                           'sensor_label':	"text	sensor mqtt topic",
                                           'battery':	"smallint NULL",
                                           'uuid':	"text NULL"
                                           },

                       'raw_loc_data': {'id':	"integer 自动增量 [nextval('loc_online_data_id_seq')]",
                                        'sensor':	"text	sensor ble mac",
                                        'vm':	"double precision",
                                        'pos_x':	"double precision",
                                        'pos_y':	"double precision",
                                        'pos_z': "double precision",
                                        'ts':	"bigint",
                                        },

                       'sensor': {'id':	"integer 自动增量 [nextval('sensor_id_seq')]",
                                  'sensor':	"text	sensor ble mac",
                                  'site':	"integer NULL	site code name",
                                  'label':	"text NULL	sensor mqtt topic",
                                  'ts_create':	"bigint NULL",
                                  'x':	"double precision",
                                  'y':	"double precision",
                                  'z':	"double precision",
                                },
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
        self.conn.cursor().execute(sql)
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
        print(sql)
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
        print(sql)
        self.conn.cursor().execute(sql)
        self.conn.commit()

    def query_trajectory(self, tmac, s_ts, e_ts):
        cur = self.conn.cursor()
        cur.execute(f"SELECT pos_x, pos_y, pos_z, ts FROM raw_loc_data WHERE sensor = \'{tmac}\' AND {s_ts} < ts AND ts < {e_ts} ORDER BY ts ASC;")
        return cur.fetchall()

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


if __name__ == '__main__':
    pass
