import configparser
from typing import Tuple


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.CELL_SIZE: int = 0
        self.CELL_NUMBER: int = 0
        self.INFO_CELLS: int = 0
        self.SNAKE_VOLUME: float = 0
        self.PACKAGE_SIZE: int = 0
        self.SESSION_LENGTH: int = 0
        self.SOCKET_POINT: str | Tuple[str, int] = ""
        self.TELEGRAM_TOKEN: str = ""

        self.settings_file: str = "settings.ini"
        self.config = configparser.ConfigParser()

        self.load_config()

    @staticmethod
    def get_socket_point(sp: str) -> str | Tuple[str, int]:
        if ":" in sp:
            host = sp.split(":")
            return host[0], int(host[1])
        return sp

    @staticmethod
    def set_socket_point(sp: str | Tuple[str, int]) -> str:
        if isinstance(sp, str):
            return sp
        return ":".join(sp)

    def load_config(self):
        self.config.read(self.settings_file)

        self.CELL_SIZE: int = int(self.config.get("GAME", "CELL_SIZE"))
        self.CELL_NUMBER: int = int(self.config.get("GAME", "CELL_NUMBER"))
        self.INFO_CELLS: int = int(self.config.get("GAME", "INFO_CELLS"))
        self.SNAKE_VOLUME: float = float(self.config.get("GAME", "SNAKE_VOLUME"))

        self.PACKAGE_SIZE: int = int(self.config.get("NETWORK", "PACKAGE_SIZE"))
        self.SESSION_LENGTH: int = int(self.config.get("NETWORK", "SESSION_LENGTH"))
        self.SOCKET_POINT: str | Tuple[str, int] = self.get_socket_point(self.config.get("NETWORK", "SOCKET_POINT"))

        self.TELEGRAM_TOKEN: str = self.config.get("BOT", "TELEGRAM_TOKEN")

    def write_config(self):
        self.config.set("GAME", "CELL_SIZE", str(self.CELL_SIZE))
        self.config.set("GAME", "CELL_NUMBER", str(self.CELL_NUMBER))
        self.config.set("GAME", "INFO_CELLS", str(self.INFO_CELLS))
        self.config.set("GAME", "SNAKE_VOLUME", str(self.SNAKE_VOLUME))

        self.config.set("NETWORK", "PACKAGE_SIZE", str(self.PACKAGE_SIZE))
        self.config.set("NETWORK", "SESSION_LENGTH", str(self.SESSION_LENGTH))
        self.config.set("NETWORK", "SOCKET_POINT", self.set_socket_point(self.SOCKET_POINT))

        self.config.set("BOT", "TELEGRAM_TOKEN", self.TELEGRAM_TOKEN)

        with open(self.settings_file, "w") as configfile:
            self.config.write(configfile)


