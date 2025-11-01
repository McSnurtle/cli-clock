# base Tab
from threading import Thread
from typing import Any


# ===== Classes =====
class Tab:
    keybind: str
    name: str
    threads: list[Thread]

    def __init__(self, config: dict[str, Any]):
        self.config: dict[str, Any] = config

    def draw(self, stdscr, width: int, height: int):
        pass

    def handle_event(self, event: int):
        pass
