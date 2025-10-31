# imports - timer.py config
import json
from typing import Any


# ===== Functions =====
def get_config() -> dict[str, Any]:
    with open("etc/conf.json", "r") as fp:
        return json.load(fp)
