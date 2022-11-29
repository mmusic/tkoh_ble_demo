from utils.db_controller import DataBaseConnector
from config.TKOH import SOURCE_INFO
REMOTE_DATABASE_NAME = 'tkoh_cms'
REMOTE_DATABASE_USER = 'postgres'
REMOTE_DATABASE_USER_PSW = 'mtrec2020'
REMOTE_DATABASE_IP = '143.89.49.63'
REMOTE_DATABASE_PORT = '7023'

db_login_info = {'db_host': REMOTE_DATABASE_IP,
                 'db_port': REMOTE_DATABASE_PORT,
                 'db_usr': REMOTE_DATABASE_USER,
                 'db_usr_psw': REMOTE_DATABASE_USER_PSW,
                 'db_name': REMOTE_DATABASE_NAME}
db = DataBaseConnector(**db_login_info)


def generate_uuid_major_minor_set():
    uuid_major_minor_list = db.query_full_table('beacon', 'uuid', 'major', 'minor')

    print(len(uuid_major_minor_list))

    uuid_major_minor_set = set()
    for uuid, major, minor in uuid_major_minor_list:
        uuid_major_minor_set.add(uuid+str(hex(major))[2:].zfill(4)+str(hex(minor))[2:].zfill(4))

    print(uuid_major_minor_set)
    print(len(uuid_major_minor_set))


def generate_source_info_dict():
    source_info_dict = {}
    source_info_list = db.query_full_table('sensor', 'sensor', 'x', 'y', 'z')
    print(source_info_list)
    print(len(source_info_list))
    for source_ident, source_x, source_y, source_z in source_info_list:
        source_info_dict[source_ident] = SOURCE_INFO(source_identifier=source_ident,
                                                     x=source_x,
                                                     y=source_y,
                                                     z=source_z,
                                                     type='non-lon-lat',
                                                     activated=True,
                                                     addition_info=None)
    print(source_info_dict)
    print(len(source_info_dict))


if __name__ == "__main__":
    generate_source_info_dict()
