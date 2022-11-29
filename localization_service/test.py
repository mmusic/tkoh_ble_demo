from multiprocessing.connection import Client
import time

address = ('localhost', 6060)  # family is deduced to be 'AF_INET'
client_conn_flag = False
try:
    client_conn = Client(address)
    client_conn_flag = True
except:
    print('error')

data = {'topic': 'BL-40',
                                                                # F000AAB004514000B0000000000000008900468C
        'data': ['043E2A02010001C0BBC40423ED1E0201061AFF4C000215F000AAB004514000B0000000000000008900468CC5B0'],
        'timestamp': time.time()}

if len(data['data']):
    # print(data)
    try:
        client_conn.send(data)
        print(data)
    except:
        client_conn_flag = False
    if not client_conn_flag:
        try:
            client_conn = Client(address)
            client_conn_flag = True
        except:
            pass