# imports - timer.py config
import json
from pathlib import Path
from typing import Any


# ===== Functions =====
def get_config() -> dict[str, Any]:
    path: str = f"{Path.home()}/"
    with open(path, "r") as fp:
        return json.load(fp)
