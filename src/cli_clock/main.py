# imports - timer.py
import curses
import sys
from typing import Any

from core.src.core.app import App
from core.src.core.tab_registry import register_tabs, keybinds, draw_functions, tabs, tips
from .utils.config import init_config

init_config()

try:
    from utils.config import get_config
except ModuleNotFoundError:
    from .utils.config import get_config

# ===== Variables =====
RUNNING: bool = True
CONFIG: dict[str, Any] = get_config()


def stop() -> None:
    [[thread.join() for thread in tab.threads] for tab in tabs.values()]
    curses.beep()
    sys.exit(0)


def launch() -> None:
    register_tabs("cli_clock.tabs", CONFIG)
    app = App("CLI-Clock", "clock", CONFIG)
    app.run()


if __name__ == '__main__':
    launch()
