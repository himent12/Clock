"""Backward-compatible launcher.

Prefer running `main.py`; this file remains for compatibility.
"""

from clock_app.app import run


if __name__ == "__main__":
    run()
