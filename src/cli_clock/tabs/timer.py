# imports
import curses
import time
from threading import Thread
from pathlib import Path
from play_sounds import play_file
from typing import Any, Iterable, Iterator
from .base import Tab

from ..utils.ascii_helper import generate_ascii, get_longest, INITIAL_X_OFFSET

# ===== Init =====
curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

# ===== Variables =====
timer_sound: Path = Path("res/timer.mp3")


# ===== Classes =====
class EditableDigitManager(Iterable[int]):
    digits: list[int] = []

    def __init__(self, hours: int, minutes: int, seconds: int):
        buffer = ""
        for value in [hours, minutes, seconds]:
            buffer += f"{value:02}"
        [self.digits.append(int(char)) for char in buffer]

        # [self.digits.append(int(char)) for char in f"{value:02}" for value in [hours, minutes, seconds]]  # append each digit from the args
        # [self.digits.append(0) for _ in range(6 - len(self.digits)) if len(self.digits) < 6]    # if not enough digits, add zeroes

        self.selected_index: int = 0

    @property
    def duration(self) -> int:
        hours: int = (10 * 3_600 * self.digits[0]) + (3_600 * self.digits[1])
        minutes: int = (10 * 60 * self.digits[2]) + (60 * self.digits[3])
        seconds: int = (10 * self.digits[4]) + self.digits[5]
        # TODO: make more concise

        return hours + minutes + seconds

    @property
    def hours(self) -> int:
        return int(self.duration / 3_600) % 99  # don't have triple digit hours

    @property
    def minutes(self) -> int:
        return int(self.duration / 60) % 60

    @property
    def seconds(self) -> int:
        return int(self.duration % 60)

    def left(self) -> None:
        self.selected_index = self.selected_index + 1 % len(self.digits)

    def right(self) -> None:
        self.selected_index = self.selected_index - 1 % len(self.digits)

    def up(self) -> None:
        self.digits[-self.selected_index] = (self.digits[-self.selected_index] + 1) % 10

    def down(self) -> None:
        self.digits[-self.selected_index] = (self.digits[-self.selected_index] - 1) % 10

    def get_time(self) -> str:
        return f"{self.digits[0]}{self.digits[1]}:{self.digits[2]}{self.digits[3]}:{self.digits[4]}{self.digits[5]}"

    def __iter__(self) -> Iterator[int]:
        return self.digits


class TimerTab(Tab):
    keybind = "t"
    name = "timer"

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        # flags
        self.PAUSED: bool = True
        self.EDIT_MODE: bool = True

        # vars
        self.duration: float = 0  # seconds
        self.remaining: float = self.duration
        self.timer_thread: Thread = Thread(target=self.timer_loop, daemon=True)
        self.threads: list[Thread] = [self.timer_thread]
        self.timer_thread.start()
        self.manager = EditableDigitManager(self.hours, self.minutes, self.seconds)

        # graphics
        self.x_offset = INITIAL_X_OFFSET(self.config["font"], "00:00:00")

    @property
    def hours(self) -> int:
        return int(self.remaining / 3_600)

    @property
    def minutes(self) -> int:
        return int(self.remaining / 60) % 60

    @property
    def seconds(self) -> int:
        return int(self.remaining % 60)

    def timer_loop(self):
        while True:
            start = time.time()

            time.sleep(self.config["interval_ms"] * 0.001)

            if not self.PAUSED:
                if self.remaining > 0:  # if more time to go... keep updating
                    self.remaining = max([self.remaining - (time.time() - start),
                                          0])  # always get a minimum of zero to looping never happens
                else:  # otherwise if timer running and nothing left to go... party! (playsound)
                    play_file(timer_sound)

    def draw(self, stdscr, height: int, width: int) -> None:
        if not self.EDIT_MODE:
            time_text: tuple[str] = generate_ascii(self.get_time(), self.config["font"])
        else:
            time_text: tuple[str] = generate_ascii(self.manager.get_time(), self.config["font"])
            # time_texts: list[tuple[str]] = [generate_ascii(str(self.manager.digits[idx]), self.config["font"]) for idx
            #                                 in range(len(self.manager.digits))]
            # time_text: list[str] = []

        for idx, line in enumerate(time_text):
            if self.config["should_update_offset"]:
                self.x_offset = get_longest(time_text)
            stdscr.addstr(
                int(height * 0.5 - (len(time_text) * 0.5 - idx + 1)),
                int(width * 0.5 - self.x_offset * 0.5),
                line)

        title: str = "Timer"
        if self.EDIT_MODE:
            title: str = "Edit Timer"

        stdscr.addstr(
            int((height * 0.5 - len(time_text) * 0.5 - 2)),
            int(width * 0.5 - len(title) * 0.5),
            title)
        if self.EDIT_MODE:
            pass
            # TODO: draw some kind of "you're editing this digit" indicator

        self.draw_tips(stdscr, height, width, time_text)

    def draw_tips(self, stdscr, height: int, width: int, time_text: tuple[str]) -> None:
        tips: list[str] = ["[P]lay/Pause     [E]dit     [R]eset"]
        if self.EDIT_MODE:
            tips: list[str] = ["[P]lay/Pause     [E]xit     [R]eset", "[UP]     [DOWN]     [LEFT]     [RIGHT]"]
        for idx, tip in enumerate(tips):
            stdscr.addstr(
                int(height * 0.5 - len(time_text) * 0.5 + 2 + len(time_text)) + idx - 1,
                int(width * 0.5 - len(tip) * 0.5),
                tip
            )

    def handle_event(self, event: int):
        if event == ord("p"):
            self.toggle()
        elif event == ord("r"):
            self.reset()
        if self.EDIT_MODE:
            if event == ord("e"):
                self.save()
            if event == curses.KEY_UP:
                self.manager.up()
            elif event == curses.KEY_DOWN:
                self.manager.down()
            elif event == curses.KEY_LEFT:
                self.manager.left()
            elif event == curses.KEY_RIGHT:
                self.manager.right()
        elif not self.EDIT_MODE:
            if event == ord("e"):
                self.edit()

    def edit(self) -> None:
        self.reset()
        self.EDIT_MODE = True

    def save(self) -> None:
        self.duration = self.manager.duration
        self.reset()
        self.EDIT_MODE = False

    def toggle(self) -> None:
        self.PAUSED = not self.PAUSED  # toggle paused state

    def reset(self) -> None:
        self.PAUSED = True
        self.remaining = self.duration

    def get_time(self) -> str:
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"
