from typing import Callable, Any, Tuple
from threading import Thread, Lock
import socket
import time
import select
import zlib

class TCPClient:
    def __init__(self, ip, port, user_name=None, psw=None, with_ssl=False):
        # todo: need to wrap ssl
        # todo: using context manager from outside to redirect the print statement
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
        self.__close_socket_lock = Lock()

        try:
            self.__s.connect((self.__ip, self.__port))
            print("connect success!!!!", self.__ip, self.__port)
        except socket.error as e:
            print("fail to connect to server when init")
            self.__s.close()
            self.__socket_good = False
        else:
            self.__socket_good = True
        Thread(target=self.__keep_conn_alive).start()

    def send(self, byte_msg: bytes, timeout=None) -> bool:
        # print("[send] socket state", self.__socket_good)
        if not self.__socket_good:
            print("socket no good")
            return False
        if type(byte_msg) is not bytes:
            print("error type")
            return False
        if timeout is not None:
            # todo: don't know if settimeout work for sendall
            self.__s.settimeout(timeout)

        # todo: can't reconnect now.
        # note: reproduce, remote server close, and the keep_conn_alive not work anymore?
        # note: try to lock the close operation
        try:
            # print("socket is good and I'm trying to send stuff!")
            # s_ts = time.time()
            compressed_date = zlib.compress(byte_msg)
            self.__s.sendall(self.__wrap_data(compressed_date))
            print(f'sending {len(byte_msg)} {len(compressed_date)}')
            # e_ts = time.time()
            # print(f"send time = {e_ts - s_ts}")
        except BlockingIOError as block_io_err:
            print(f"fail to send, due to", block_io_err)
            self.__network_good = False
        except TimeoutError as time_out_err:
            print(f"fail to send, due to", time_out_err)
            self.__network_good = False
        except ConnectionResetError as connection_reset_err:
            self.__close_socket_lock.acquire()  # todo: why again I don't have the chance to acquire the lock?
            print(f"fail to send, due to", connection_reset_err)
            self.__s.close()
            self.__socket_good = False
            self.__network_good = False
            print("[send] overwrite socket state to:", self.__socket_good)
            self.__close_socket_lock.release()
        except ConnectionRefusedError as connection_refuse_err:
            self.__close_socket_lock.acquire()
            print(f"fail to send, due to", connection_refuse_err)
            self.__s.close()
            print("[send] overwrite socket state to:", self.__socket_good)
            self.__close_socket_lock.release()
        except OSError as os_err:
            self.__close_socket_lock.acquire()
            print(f"fail to send, due to", os_err)
            self.__s.close()
            self.__socket_good = False
            print("[send] overwrite socket state to:", self.__socket_good)
            self.__close_socket_lock.release()
        else:
            self.__network_good = True
            self.__socket_good = True
            # print("send successful")
        finally:
            if self.__socket_good and self.__network_good:
                return True
            else:
                return False

    @staticmethod
    def __wrap_data(byte_msg: bytes) -> bytes:
        # note: wrap a byte msg with a 5 byte long digit, for the sake of 65536
        return str(len(byte_msg)).zfill(10).encode(encoding='utf-8') + byte_msg

    def receive(self) -> bytes:
        bs = b''
        while True:
            try:
                self.__close_socket_lock.acquire()
                print("start receiving")
                recv = self.__s.recv(1024)  # todo: why this will affect self.__s.connect?
                if not recv:
                    self.__close_socket_lock.release()   # note: this way of programming logic is liable to be forgotten
                    return b''  # note: when returning b'', it can be at least two possiblities, terminated by remote server or the connect fail but the socket is not yet closed.
                else:
                    bs = bs + recv
                try:
                    msg, remain = TCPServer.unwrap_data(bs)
                except Exception as e:
                    print("fail to unwrap data")
                    self.__close_socket_lock.release()
                    return b''
                if msg is None:
                    bs = remain
                else:
                    self.__close_socket_lock.release()
                    return msg
            except OSError as e:
                self.__close_socket_lock.release()
                print(f"error in receive: {e}")
                time.sleep(1)  # note: wait for reconnect
            except Exception as e:
                self.__close_socket_lock.release()
                import traceback
                print(f"try to receive data from server but fail, due to error: {traceback.format_exc()}")
                time.sleep(1)

    def close(self):
        self.__shut_down = True

    def __keep_conn_alive(self):
        while True:
            # print("checking connection situation")
            if self.__shut_down:
                try:
                    self.__s.close()
                except Exception as e:
                    print(e)
                finally:
                    print("shutdown")
                    break
            # print("[keep_conn_alive] socket state:", self.__socket_good)
            if not self.__socket_good:
                try:
                    self.__close_socket_lock.acquire()
                    print("trying to reconnect")
                    self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.__s.setblocking(False)
                    self.__s.settimeout(3)
                    self.__s.connect((self.__ip, self.__port))  # todo: why sometimes this will pass without throwing error even if it's not actually connected, seems that it's a problem due to share variable, after I add a lock to it, all things goes right.
                    print("connect success!!!!", self.__ip, self.__port)
                except OSError as e:
                    print("except error in client ", e)
                    self.__s.close()
                    self.__socket_good = False
                    self.__close_socket_lock.release()
                    time.sleep(2)
                    continue
                else:
                    self.__socket_good = True
                    print("[keep_conn_alive] overwrite socket state to:", self.__socket_good)
                    self.__close_socket_lock.release()
                    print("successfully connect to server")
            time.sleep(3)


class TCPServer:
    # todo: sync with server side tcp code
    def __init__(self, ip, port, username=None, psw=None):
        self.__socket_handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__ip = ip
        self.__port = port
        self.__callback = None

    def start(self, callback: Callable[[bytes, Tuple[str, int]], Any], daemon=False):
        self.__callback = callback
        if daemon:
            Thread(target=self.__loop_forever, args=(callback, )).start()
        else:
            self.__loop_forever(callback)

    def __loop_forever(self, callback: Callable[[bytes, Tuple[str, int]], Any]):
        self.__callback = callback
        self.__socket_handler.bind((self.__ip, self.__port))
        self.__socket_handler.listen(60)  # note: each sensor will consume one
        while True:
            conn, addr = self.__socket_handler.accept()
            print(f"accept connection addr: ", addr)
            Thread(target=self.client_handle, args=(conn, addr)).start()

    def client_handle(self, conn, addr):
        bs = b''
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
                        self.__callback(msg, addr)  # todo: if the on_receive_sensor_data itself is a instance method, then I have two self, how to deal with it?
                except Exception as e:
                    print(e)
                bs = remain
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

# server side code
# from network.tcp import TCPServer
#
#
# def on_receive_sensor_data(msg: bytes, addr):
#     print(f"receive {msg} from {addr}")
#
#
# server = TCPServer(ip='', port=5354)
# server.start(on_receive_sensor_data=on_receive_sensor_data)
