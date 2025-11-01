# imports
import time
from threading import Thread
from datetime import datetime, timedelta
from typing import Any
from .base import Tab

from ..utils.ascii_helper import generate_ascii, get_longest, INITIAL_X_OFFSET


class StopwatchTab(Tab):
    keybind = "s"
    name = "stopwatch"

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.elapsed: float = 0.0
        self.paused: bool = True
        self.stopwatch_thread: Thread = Thread(target=self.stopwatch_loop, daemon=True)
        self.stopwatch_thread.start()
        self.threads = [self.stopwatch_thread]

    def stopwatch_loop(self):
        while True:
            start = time.time()

            time.sleep(self.config["interval_ms"] * 0.001)

            if not self.paused:
                self.elapsed += time.time() - start

    def draw(self, stdscr, height: int, width: int) -> None:
        time_text: tuple[str] = generate_ascii(self.get_time(), self.config["font"])

        for idx, line in enumerate(time_text):
            x_offset = INITIAL_X_OFFSET(self.config["font"], "00:00:00")
            if self.config["should_update_offset"]:
                x_offset = get_longest(time_text)
            stdscr.addstr(
                int(height * 0.5 - (len(time_text) * 0.5 - idx + 1)),
                int(width * 0.5 - x_offset * 0.5),
                line)

        stdscr.addstr(
            int((height * 0.5 - len(time_text) * 0.5 - 2)),
            int(width * 0.5 - len("Stopwatch") * 0.5),
            "Stopwatch")
        stdscr.addstr(
            int(height * 0.5 - len(time_text) * 0.5 + 2 + len(time_text)),
            int(width * 0.5 - len("[B]egin     [P]ause     [R]eset") * 0.5),
            "[B]egin     [P]ause     [R]eset"
        )

    def handle_event(self, event: int):
        if event == ord("b"):
            self.begin()
        if event == ord("p"):
            self.toggle()
        elif event == ord("r"):
            self.reset()

    def begin(self):
        self.paused = False

    def toggle(self) -> None:
        if self.elapsed > 0:    # make [B]egin the only option to start a stopwatch
            self.paused = not self.paused  # toggle paused state

    def reset(self) -> None:
        self.paused = True
        self.elapsed: float = 0.0

    def get_time(self) -> str:
        # EXAMPLE BY AI:
        return (datetime(1, 1, 1) + timedelta(seconds=self.elapsed)).strftime("%H:%M:%S")  # .%f")[:-3]
