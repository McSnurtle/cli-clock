# imports - timer.py ascii_helper
import art
from typing import Iterable, Union, List, Tuple

from cli_clock.utils.config import get_config
from cli_clock.utils.clock import get_time


# ===== Variables =====
FONT: str = get_config()["font"]
INITIAL_X_OFFSET: int = max([len(i) for i in art.text2art(get_time("%H:%M:%S"), FONT).split("\n")])


# ===== Functions =====
def generate_ascii(text: str, font: str = FONT) -> tuple[str]:
    """Returns ascii text in the font as specified in `/etc/conf.json` or `font` as a tuple of strings."""
    return art.text2art(text, font).split("\n")


def get_longest(texts: Union[Iterable[str], Tuple[str], List[str]]) -> int:
    """Returns an int representing the longest length of a string found in `texts`"""
    return max([len(i) for i in texts])
