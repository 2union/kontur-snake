import os
import socket
from collections import deque
from _thread import *

from settings import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if isinstance(SOCKET_POINT, str):
    if os.path.exists(SOCKET_POINT):
        os.remove(SOCKET_POINT)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    s.bind(SOCKET_POINT)
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

commands = deque()
responses = deque()
finish = ''


def threaded_client(conn):
    global commands, finish, responses
    while True:
        try:
            data = conn.recv(PACKAGE_SIZE)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                client = int(arr[0])

                if client in {1, 3}:
                    if arr[1] == 'finish':
                        finish = reply
                        commands.clear()
                        reply = '1:0'
                    if arr[1] in ['T1', 'T2']:
                        responses.append(reply)

                if client in {1, 3} and len(commands):
                    reply = commands.popleft()

                if client == 2:
                    if len(finish):
                        reply = finish
                        finish = ''
                    if arr[1] != 'ping':
                        commands.append(arr[1])
                    elif len(responses):
                        reply = responses.popleft()

                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except Exception:
            break

    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to client!")

    start_new_thread(threaded_client, (conn,))
