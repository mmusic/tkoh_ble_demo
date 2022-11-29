import socket
from typing import Callable, Any, Tuple
from threading import Thread
import time


class UDPClient:
    def __init__(self, ip: str, port: int, user_name=None, psw=None, with_ssl=False):
        # todo: need to wrap ssl
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_address = (ip, port)

    def send(self, bdata: bytes):
        print(f"before send: ", time.time())
        self.socket.sendto(bdata, self.udp_address)
        print(f"after send: ", time.time())


class UDPServer:
    def __init__(self, ip: str, port: int, user_name=None, psw=None, with_ssl=False):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.psw = psw
        self.with_ssl = with_ssl
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (self.ip, self.port)

    def start(self, callback: Callable[[bytes, Tuple[str, int]], Any] = None):
        self.sock.bind(self.addr)
        while True:
            bs, addr = self.sock.recvfrom(1024)
            print("accept bytes")
            if callback is None:
                self.client_handle(bs, addr)
            else:
                callback(bs, addr)

    def client_handle(self, bdata:bytes, addr):
            print("handle msg: ", bdata.decode('utf-8'))

    def send(self, bdata: bytes):
        return 0


if __name__ == "__main__":
    # server side
    ip = ''
    port = 5354
    server = UDPServer(ip=ip, port=port)
    t = Thread(target=server.start)
    t.start()
    t.join()


# client side
# from network.udp import UDPClient
# import time
#
# if __name__ == "__main__":
#     ip = ''
#     port = 5354
#     client = UDPClient(ip=ip, port=port)
#     client.send(b"send 1")
#     time.sleep(10)
#     client.send(b"send 2")
