# cli-clock.py 🕐
Finally a customizable, centered, nice CLI-based clock.

<img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/6cff4704-a824-4fba-bde2-77aa365673bb" />

## Features ✨
- Live CLI-based digital clock
- ASCII art characters
- Everything centered!
- Live updating date
- Completely customizable fonts
- Cool stylish border
- Resizable! (supports live terminal resizing)
- More coming soon... (maybe) :eyes:

## Installation ⚙️
The program is written in [Python](<https://www.python.org/>), and thus requires it as its sole system-wide dependency.

### For General Use
Run `pip install <URL>` where the `<URL` is the link to the `.whl` file in the [latest release](<https://github.com/McSnurtle/releases/latest>).
Then run the program with the command `cli-clock`. If the command is "not found" or similar, make sure your [Python scripts folder is on your PATH](<https://www.geeksforgeeks.org/python/how-to-add-python-to-windows-path/>).

### For Developers
```bash
git clone https://github.com/McSnurtle/cli-clock \
cd cli-clock \
python -m venv venv \
source ./venv/bin/activate \
pip install --upgrade --verbose -r requirements.txt \
pip install -e . \
cli-clock
```
On windows, you'll have to run `.\venv\Scripts\activate` instead of the above 4th line.

*Note: this project, all of its files, including this README.md were written entirely by hand, without the use of any AI tools whatsoever.*
