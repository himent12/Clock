"""Simple desktop clock app using Tkinter."""

from datetime import datetime
import tkinter as tk
from tkinter import ttk


class ClockApp:
    """Digital clock desktop application."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Clock")
        self.root.geometry("360x160")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        self.time_label = ttk.Label(frame, text="--:--:--", font=("Segoe UI", 42, "bold"))
        self.time_label.pack(pady=(0, 8))

        self.date_label = ttk.Label(frame, text="", font=("Segoe UI", 16))
        self.date_label.pack()

        self._tick()

    def _tick(self) -> None:
        now = datetime.now()
        self.time_label.configure(text=now.strftime("%H:%M:%S"))
        self.date_label.configure(text=now.strftime("%A, %B %d, %Y"))
        self.root.after(200, self._tick)


def main() -> None:
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    app = ClockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
