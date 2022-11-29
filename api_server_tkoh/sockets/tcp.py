from typing import Callable, Any, Tuple
from threading import Thread, Lock
import socket
import time
from queue import Queue


# note: client will send msg in the following format: b'some_number{bytes_you_wanna_send}'
# note: some property to keep: never crash, constant resource usage, able to send, non-blocking
# note: but if it's non-blocking, I can't tell immediately if the packet is sent completely or not
class TCPClient:
    def __init__(self, ip, port, user_name=None, psw=None, with_ssl=False):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.setblocking(False)
        self.__s.settimeout(3)
        self.__ip = ip
        self.__port = port
        self.__user_name = user_name
        self.__psw = psw
        self.__socket_good = False
        self.__network_good = False
        self.__shut_down = False
        try:
            self.__s.connect((self.__ip, self.__port))
        except socket.error as e:
            print("fail to connect to app when init")
            self.__socket_good = False
        else:
            self.__socket_good = True
        Thread(target=self.__keep_conn_alive).start()

    def send(self, byte_msg: bytes, timeout=None) -> bool:
        if not self.__socket_good:
            print("socket no good")
            return False
        if type(byte_msg) is not bytes:
            print("error type")
            return False
        if timeout is not None:
            self.__s.settimeout(timeout)

        try:
            s_ts = time.time()
            self.__s.sendall(self.wrap_data(byte_msg))
            e_ts = time.time()
            print(f"send time = {e_ts - s_ts}")
        except BlockingIOError as block_io_err:
            print(block_io_err)
            self.__network_good = False
        except ConnectionResetError as connection_reset_err:
            print(connection_reset_err)
            self.__s.close()
            self.__socket_good = False
        except TimeoutError as time_out_err:
            print(time_out_err)
            self.__network_good = False
        except ConnectionRefusedError as connection_refuse_err:
            print(connection_refuse_err)
            self.__s.close()
            self.__socket_good = False
        except OSError as os_err:
            print(os_err)
            self.__s.close()
            self.__socket_good = False
        else:
            self.__network_good = True
            self.__socket_good = True
        finally:
            if self.__socket_good and self.__network_good:
                return True
            else:
                return False

    @staticmethod
    def wrap_data(byte_msg: bytes) -> bytes:
        # note: wrap a byte msg with a 5 byte long digit, for the sake of 65536
        return str(len(byte_msg)).zfill(10).encode(encoding='utf-8') + byte_msg

    def receive(self, callback):
        pass

    def close(self):
        self.__shut_down = True

    def __keep_conn_alive(self):
        while True:
            print("checking connection situation")
            if self.__shut_down:
                try:
                    self.__s.close()
                except Exception as e:
                    print(e)
                finally:
                    print("shutdown")
                    break
            if not self.__socket_good:
                try:
                    self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.__s.setblocking(False)
                    self.__s.settimeout(3)
                    self.__s.connect((self.__ip, self.__port))
                except OSError as e:
                    print("except error in client ", e)
                    self.__s.close()
                    time.sleep(2)
                    continue
                else:
                    print("successfully connect to app")
                    self.__socket_good = True
            time.sleep(3)


class TCPServer:
    def __init__(self, ip, port, username=None, psw=None):
        self.__socket_handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__ip = ip
        self.__port = port
        self.__callback = None
        self.__receive_buf = Queue()
        self.__conns = {}  # Dict[Tuple: client_sock}
        self.__conns_lock = Lock()

    def start(self):
        Thread(target=self.__loop_forever).start()

    def __loop_forever(self):
        self.__socket_handler.bind((self.__ip, self.__port))
        self.__socket_handler.listen(60)  # note: each sensor will consume one
        while True:
            conn, addr = self.__socket_handler.accept()
            print(f"accept connection addr: ", addr)
            if addr in self.__conns:
                print(f"accept another connection with same ip addr = {addr}, discard it")
                conn.close()
                continue
            self.__conns[addr] = conn
            Thread(target=self.client_handle, args=(addr, )).start()  # note: can be used to mimic the crash

    def receive(self):  # blocking operation
        return self.__receive_buf.get()

    def response(self, msg: bytes, addr: Tuple):
        self.__conns_lock.acquire()
        if addr in self.__conns:
            client_socket = self.__conns[addr]
        else:
            print(f"bad connection to {addr}, discard msg {msg}")
            return None
        self.__conns_lock.release()

        try:
            wrapped_data = TCPClient.wrap_data(msg)
            client_socket.sendall(wrapped_data)
        except Exception as e:
            print(e)

    def client_handle(self, addr):
        bs = b''
        self.__conns_lock.acquire()
        conn = self.__conns[addr]
        self.__conns_lock.release()
        with conn:
            while True:
                try:
                    recv = conn.recv(1024)
                except OSError:
                    break
                if not recv:  # note: if client side call .close() then this will be executed, otherwise the connection will wait till timeout and the resource will not release till then
                    break
                else:
                    bs = bs + recv
                try:
                    msg, remain = self.unwrap_data(bs)
                except Exception as e:
                    print(e)
                    break
                try:
                    if msg is not None:
                        self.__receive_buf.put((msg, addr))
                except Exception as e:
                    print(e)
                bs = remain
        self.__conns_lock.acquire()
        del self.__conns[addr]
        self.__conns_lock.release()
        print("close connection")

    @staticmethod
    def unwrap_data(byte_msg: bytes):
        """
        :param byte_msg:
        :return: (complete_bytes: bytes, remain_bytes: bytes)

        if byte_msg doesn't contain a complete message, then the return message will be None
        """
        if len(byte_msg) <= 10:
            return None, byte_msg
        else:
            b_byte_len = byte_msg[:10]
            try:
                byte_length = int(b_byte_len.decode(encoding='utf-8'))
            except Exception:
                raise
            else:
                if len(byte_msg) - 10 < byte_length:
                    return None, byte_msg
                return byte_msg[10: 10 + byte_length], byte_msg[10+byte_length:]


if __name__ == "__main__":
    client = TCPClient(ip='', port=5354)
    num = 1
    while num > 0:
        send_success = True
        send_success = send_success and client.send(b"no timeout"*1000)
        # send_success = send_success and client.send(b"timeout", timeout=1)
        if send_success:
            num -= 1
        time.sleep(2)
    client.close()

# app side code
# from network.tcp import TCPServer
#
#
# def callback(msg: bytes, ip_addr):
#     print(f"receive {msg} from {ip_addr}")
#
#
# app = TCPServer(ip='', port=5354)
# app.start(callback=callback)
