# base Tab
from typing import Any


# ===== Classes =====
class Tab:
    keybind: str
    name: str

    def __init__(self, config: dict[str, Any]):
        self.config: dict[str, Any] = config

    def draw(self, stdscr, width: int, height: int):
        pass
