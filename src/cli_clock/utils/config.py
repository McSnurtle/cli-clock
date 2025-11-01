# imports - timer.py config
import json
import os
import subprocess
from pathlib import Path
from typing import Any


# ===== Functions =====
def init_config() -> None:
    """If configs do not exist at `$HOME/.config/cli-clock/`, this function will create the directory and pull the latest defaults from the repo's main branch."""

    path: str = f"{Path.home()}/.config/cli-clock/"
    print(f"Searching for pre-installed configs in {path}")
    if not os.path.exists(path):
        print(f"None found, installing defaults to {path}")
        os.mkdir(path)
        subprocess.run(["curl", "-o" f"{path}conf.json",
                        "https://raw.githubusercontent.com/McSnurtle/cli-clock/refs/heads/main/etc/conf.json"])
        subprocess.run(["curl", "-o", f"{path}format-guide.md",
                        "https://raw.githubusercontent.com/McSnurtle/cli-clock/refs/heads/main/etc/format-guide.md"])


def get_config() -> dict[str, Any]:
    path: str = f"{Path.home()}/.config/cli-clock/conf.json"
    print(f"Fetching configs from {path}")
    with open(path, "r") as fp:
        return json.load(fp)
