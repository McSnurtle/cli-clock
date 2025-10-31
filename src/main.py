# imports - timer.py
import art
import curses
import datetime
import sys
import time
from threading import Thread
from typing import Any, List

from utils.config import get_config
from utils.clock import get_time
from utils.ascii_helper import generate_ascii, get_longest, INITIAL_X_OFFSET

# ===== Variables =====
RUNNING: bool = True
CONFIG: dict[str, Any] = get_config()
INTERVAL: int = CONFIG["interval_ms"]
tips: list[str] = ["[Q]uit", "[C]lock", "[T]imer", "[A]larm", "[S]topwatch"]


# ===== Functions =====
def main(stdscr) -> None:
    curses.curs_set(False)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    try:
        while RUNNING:
            stdscr.erase()
            height, width = stdscr.getmaxyx()
            stdscr.border()

            time_text: tuple[str] = generate_ascii(get_time())

            try:
                if CONFIG["show_date"]:
                    date_text: str = f"{CONFIG['date_prefix']}{get_time(CONFIG['date_format'])}{CONFIG['date_suffix']}"
                    stdscr.addstr(height // 2 - len(time_text) // 2 - 2, width // 2 - len(date_text) // 2, date_text)
                for idx, line in enumerate(time_text):
                    center = len(time_text) // 2
                    h_offset = center - idx + 1
                    if CONFIG["should_update_offset"]:
                        x_offset = get_longest(time_text)
                    else:
                        x_offset = INITIAL_X_OFFSET
                    stdscr.addstr(height // 2 - h_offset, width // 2 - x_offset // 2, line)

                tips_buffer: str = "     " + "     ".join(tips) + "     "
                stdscr.addstr(height-1, width // 2 - len(tips_buffer) // 2, tips_buffer)
            except curses.error:
                pass  # Terminal too small...

            stdscr.refresh()

            ch = stdscr.getch()
            if ch == ord('q'):
                break
            elif ch == ord('c'):
                pass
                # got to countdown screen

            # Sleep a bit to reduce CPU usage
            curses.napms(INTERVAL)

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    # tarty1
    # sblood
    # roman
    # rev
    # georgia11
    # fraktur
    # fire_font-s
    # colossal
    # art.font_list()
    curses.wrapper(main)
