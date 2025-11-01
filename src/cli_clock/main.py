# imports - timer.py
import curses
import sys
from typing import Any

from .tab_registry import register_tabs, keybinds, draw_functions, tips
from .utils.config import init_config

init_config()

try:
    from utils.config import get_config
except ModuleNotFoundError:
    from .utils.config import get_config

# ===== Variables =====
RUNNING: bool = True
CONFIG: dict[str, Any] = get_config()


# ===== Functions =====
def draw_hints(stdscr, height: int, width: int) -> None:
    tips_buffer: str = "     " + "     ".join(tips) + "     "
    stdscr.addstr(height - 1, width // 2 - len(tips_buffer) // 2, tips_buffer)


def main(stdscr) -> None:
    curses.curs_set(False)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    height, width = stdscr.getmaxyx()

    tabs: dict[str, Any] = {
        "clock": curses.newwin(height, width, 0, 0),
        "timer": curses.newwin(height, width, 0, 0)
    }
    current_tab: str = "clock"  # default tab

    try:
        while RUNNING:
            stdscr.erase()
            _height, _width = stdscr.getmaxyx()
            stdscr.border()

            try:
                draw_hints(stdscr, _height, _width)
                print(tips)

                draw_functions[current_tab](stdscr, _height, _width)
            except curses.error:
                pass  # Terminal too small...
            # except KeyError as e:
            #     print(f"Error: attempted to open tab {current_tab} but it does not exist! ({e})")

            stdscr.refresh()

            event = stdscr.getch()
            if event == ord('q'):
                break
            elif event == curses.KEY_RESIZE:
                _height, _width = stdscr.getmaxyx()
                for tab in tabs.values():
                    tab.resize(_height, _width)
                    tab.mvwin(0, 0)
                stdscr.clear()
            elif event in [ord(key) for key in list(keybinds.keys())]:  # tab bindings
                current_tab: str = keybinds[chr(event)]
                print(f"Switching tab to: {keybinds[chr(event)]}")

            curses.napms(CONFIG["interval_ms"])

    except KeyboardInterrupt:
        sys.exit(0)


def launch() -> None:
    register_tabs(CONFIG)
    curses.wrapper(main)


if __name__ == '__main__':
    register_tabs(CONFIG)
    launch()
