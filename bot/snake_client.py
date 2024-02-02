import socket
from typing import Union, Tuple


class SnakeClient:
    def __init__(self, socket_name: Union[str, Tuple[str, int]], package_size: int):
        if isinstance(socket_name, str):
            self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        else:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = socket_name
        self.package_size = package_size
        self.connect()

    def connect(self):
        self.client.connect(self.addr)

    def send(self, data: str):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            self.client.settimeout(1)
            reply = self.client.recv(self.package_size).decode()
            return reply
        except socket.error as e:
            return str(e)
