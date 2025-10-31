# imports - timer.py clock
import datetime

from utils.config import get_config


# ===== Variables =====
FORMAT: str = get_config()["format"]


# ===== Functions =====
def get_time(fmt: str = FORMAT) -> str:
    """Returns the formatted string representing the current system time."""
    return datetime.datetime.now().strftime(fmt)
