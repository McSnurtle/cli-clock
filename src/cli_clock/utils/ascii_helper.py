# imports - timer.py ascii_helper
import art
from typing import Iterable, Union, List, Tuple


# ===== Functions =====
def generate_ascii(text: str, font: str) -> tuple[str]:
    """Returns ascii text in the font as specified in `/etc/conf.json` or `font` as a tuple of strings."""
    return art.text2art(text, font).split("\n")


def get_longest(texts: Union[Iterable[str], Tuple[str], List[str]]) -> int:
    """Returns an int representing the longest length of a string found in `texts`"""
    return max([len(i) for i in texts])


def INITIAL_X_OFFSET(font: str) -> int:
    return get_longest(generate_ascii("12:34:56", font))
