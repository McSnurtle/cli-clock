# imports - timer.py config
import json
import os
from pathlib import Path
from typing import Any


# ===== Variables =====
defaults: dict[str, Any] = {
  "format": "%H:%M:%S",
  "date_format": "%A, %B %d, %Y",
  "font": "georgian9",
  "date_font": "term",
  "date_prefix": "--+{ ",
  "date_suffix": " }+--",
  "show_date": True,
  "interval_ms": 100,
  "should_update_offset": False
}
format_guide: str = """# Time Formatting Guide
The below is sourced directly from the uber-helpful website [strftime.org](<https:?/https://strftime.org/>):\n
\n
### Example:\n
An example of the 12hr format "1:30:00 PM" would be:\n
\n
`%I:%M:%S %p`\n
\n
Or for 24hr format:\n
\n
`%H:%M:%S`\n
\n
### Formatting Codes:\n
\n
Code|	Example	|Description\n
| --- | --- | --- |\n
%a	|Sun	|Weekday as locale’s abbreviated name.\n
%A	|Sunday|	Weekday as locale’s full name.\n
%w|	0|	Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.\n
%d	|08|	Day of the month as a zero-padded decimal number.\n
%-d	|8|	Day of the month as a decimal number. (Platform specific)\n
%b	|Sep|	Month as locale’s abbreviated name.\n
%B	|September|	Month as locale’s full name.\n
%m	|09|	Month as a zero-padded decimal number.\n
%-m	|9|	Month as a decimal number. (Platform specific)\n
%y	|13|	Year without century as a zero-padded decimal number.\n
%Y	|2013|	Year with century as a decimal number.\n
%H	|07|	Hour (24-hour clock) as a zero-padded decimal number.\n
%-H	|7|	Hour (24-hour clock) as a decimal number. (Platform specific)\n
%I	|07|	Hour (12-hour clock) as a zero-padded decimal number.\n
%-I	|7|	Hour (12-hour clock) as a decimal number. (Platform specific)\n
%p	|AM|	Locale’s equivalent of either AM or PM.\n
%M	|06|	Minute as a zero-padded decimal number.\n
%-M	|6|	Minute as a decimal number. (Platform specific)\n
%S	|05|	Second as a zero-padded decimal number\n
.%-S	|5|	Second as a decimal number. (Platform specific)\n
%f	|000000|	Microsecond as a decimal number, zero-padded to 6 digits.\n
%z	|+0000|	UTC offset in the form ±HHMM[SS[.ffffff]] (empty string if the object is naive).\n
%Z	|UTC|	Time zone name (empty string if the object is naive).\n
%j	|251|	Day of the year as a zero-padded decimal number.\n
%-j	|251|	Day of the year as a decimal number. (Platform specific)\n
%U	|36|	Week number of the year (Sunday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.\n
%-U	|36|	Week number of the year (Sunday as the first day of the week) as a decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. (Platform specific)\n
%W	|35|	Week number of the year (Monday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Monday are considered to be in week 0.\n
%-W	|35|	Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0. (Platform specific)\n
%c	|Sun| Sep 8 07:06:05 2013	Locale’s appropriate date and time representation.\n
%x	|09/08/13|	Locale’s appropriate date representation.\n
%X	|07:06:05|	Locale’s appropriate time representation.\n
%%	|%|	A literal '%' character."""


# ===== Functions =====
def init_config() -> None:
    """If configs do not exist at `$HOME/.config/cli-clock/`, this function will create the directory and pull the latest defaults from the repo's main branch."""

    path: str = f"{Path.home()}/.config/cli-clock/"
    print(f"Searching for pre-installed configs in {path}")
    if not os.path.exists(path):
        print(f"None found, installing defaults to {path}")
        os.mkdir(path)
        with open(f"{path}conf.json", "w") as fp:
            fp.write(json.dumps(defaults))
        with open(f"{path}format-guide.md", "w") as fp:
            fp.write(format_guide)


def get_config() -> dict[str, Any]:
    path: str = f"{Path.home()}/.config/cli-clock/conf.json"
    print(f"Fetching configs from {path}")
    with open(path, "r") as fp:
        return json.load(fp)
