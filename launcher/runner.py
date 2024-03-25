from time import sleep
from typing import Callable, Optional
from multiprocessing import Process

from server import server_run
from bot import bot_run
from snake import game_run


class SnakeProcess:
    process: Optional[Process] = None

    def __init__(self, process_callback: Callable):
        self.process_callback = process_callback
        self.process_init()

    def process_init(self):
        self.process = Process(target=self.process_callback)
        self.process.daemon = True

    def run(self):
        self.process.start()

    def stop(self):
        self.process.terminate()
        self.process.join()
        self.process.close()
        self.process_init()


SERVER_PROCESS = SnakeProcess(server_run)
BOT_PROCESS = SnakeProcess(bot_run)
GAME_PROCESS = SnakeProcess(game_run)

IS_ALIVE = False


def components_start():
    global SERVER_PROCESS, IS_ALIVE
    SERVER_PROCESS.run()
    sleep(1)
    BOT_PROCESS.run()
    GAME_PROCESS.run()
    IS_ALIVE = True


def components_stop():
    global SERVER_PROCESS, IS_ALIVE
    BOT_PROCESS.stop()
    GAME_PROCESS.stop()
    sleep(5)
    SERVER_PROCESS.stop()
    IS_ALIVE = False


def components_toggle():
    global IS_ALIVE
    if IS_ALIVE:
        components_stop()
    else:
        components_start()
