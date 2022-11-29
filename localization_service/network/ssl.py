import ssl
import socket
import json


class SSLClient:
    def __init__(self, ip, port, user_name=None, psw=None):
        pass
        # hostname = 'www.python.org'
        # context = ssl.create_default_context()
        #
        # with socket.create_connection((hostname, 443)) as sock:
        #     with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        #         print(ssock.version())

    def send(self, byte_msg: bytes, timeout=None):  # todo: it's suitable to restrict the send data to be dict?
        # todo: bs = str(len(bs)).encode('utf-8') + bs
        pass

    def receive(self, callback):
        pass


class SSLServer:
    # todo: decode from byte to string, utf-8
    # todo: json load
    pass
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain('/path/to/certchain.pem', '/path/to/private.key')
    #
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    #     sock.bind(('127.0.0.1', 8443))
    #     sock.listen(5)
    #     with context.wrap_socket(sock, server_side=True) as ssock:
    #         conn, addr = ssock.accept()
