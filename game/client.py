import socket
from typing import Union, Tuple


class Client:

    def __init__(self, socket_point: Union[str, Tuple[str, int]], package_size: int):
        if isinstance(socket_point, str):
            self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        else:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = socket_point
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
            reply = self.client.recv(self.package_size).decode()
            return reply
        except socket.error as e:
            return str(e)
