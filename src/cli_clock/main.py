# imports - timer.py
import curses
import sys
from typing import Any

from utils.config import get_config
from utils.clock import get_time
from utils.ascii_helper import generate_ascii, get_longest, INITIAL_X_OFFSET

# ===== Variables =====
RUNNING: bool = True
CONFIG: dict[str, Any] = get_config()
INTERVAL: int = CONFIG["interval_ms"]
tips: list[str] = ["[Q]uit", "[C]lock", "[T]imer", "[A]larm", "[S]topwatch"]


# ===== Functions =====
def draw_time(stdscr, text: tuple[str], height: int, width: int) -> None:
    for idx, line in enumerate(text):
        x_offset = INITIAL_X_OFFSET
        if CONFIG["should_update_offset"]:
            x_offset = get_longest(text)
        stdscr.addstr(
            int(height * 0.5 - (len(text) * 0.5 - idx + 1)),
            int(width * 0.5 - x_offset * 0.5),
            line)


def draw_date(stdscr, time_text: tuple[str], height: int, width: int) -> None:
    date_text: str = f"{CONFIG['date_prefix']}{get_time(CONFIG['date_format'])}{CONFIG['date_suffix']}"
    stdscr.addstr(
        int((height * 0.5 - len(time_text) * 0.5 - 2)),
        int((width * 0.5 - len(date_text) * 0.5)),
        date_text)


def draw_hints(stdscr, height: int, width: int) -> None:
    tips_buffer: str = "     " + "     ".join(tips) + "     "
    stdscr.addstr(height - 1, width // 2 - len(tips_buffer) // 2, tips_buffer)


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
                draw_time(stdscr, time_text, height, width)
                if CONFIG["show_date"]:
                    draw_date(stdscr, time_text, height, width)
                draw_hints(stdscr, height, width)
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
