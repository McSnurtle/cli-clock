# imports - timer.py clock
import datetime


# ===== Functions =====
def get_time(fmt: str) -> str:
    """Returns the formatted string representing the current system time."""
    return datetime.datetime.now().strftime(fmt)

# TODO: Add alarm, timer, and stopwatch using Delta time
