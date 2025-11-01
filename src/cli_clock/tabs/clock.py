# imports
import datetime
from typing import Any
from .base import Tab

from ..utils.ascii_helper import generate_ascii, get_longest, INITIAL_X_OFFSET


# ===== Functions =====
def get_time(fmt: str) -> str:
    """Returns the formatted string representing the current system time."""
    return datetime.datetime.now().strftime(fmt)


# ===== Classes =====
class ClockTab(Tab):
    keybind = "c"
    name = "clock"

    def draw(self, stdscr, height: int, width: int) -> None:
        time_text: tuple[str] = generate_ascii(get_time(self.config["format"]), self.config["font"])

        for idx, line in enumerate(time_text):
            x_offset = INITIAL_X_OFFSET(self.config["font"])
            if self.config["should_update_offset"]:
                x_offset = get_longest(time_text)
            stdscr.addstr(
                int(height * 0.5 - (len(time_text) * 0.5 - idx + 1)),
                int(width * 0.5 - x_offset * 0.5),
                line)
        if self.config["show_date"]:
            date_text: str = f"{self.config['date_prefix']}{get_time(self.config['date_format'])}{self.config['date_suffix']}"
            stdscr.addstr(
                int((height * 0.5 - len(time_text) * 0.5 - 2)),
                int((width * 0.5 - len(date_text) * 0.5)),
                date_text)
