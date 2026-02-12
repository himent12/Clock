"""Simple-but-capable desktop clock app using Tkinter only."""

from datetime import datetime, timezone
import tkinter as tk
from tkinter import ttk


class ClockApp:
    """Digital clock desktop application with lightweight controls."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Clock")
        self.root.geometry("520x270")
        self.root.minsize(500, 250)

        self.running = True
        self.use_24h = tk.BooleanVar(value=True)
        self.show_seconds = tk.BooleanVar(value=True)
        self.use_utc = tk.BooleanVar(value=False)
        self.always_on_top = tk.BooleanVar(value=False)
        self.status_text = tk.StringVar(value="Running")

        self._build_ui()
        self._tick()

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(outer, text="Desktop Clock", font=("Segoe UI", 14, "bold"))
        title.pack(anchor="w", pady=(0, 8))

        self.time_label = ttk.Label(outer, text="--:--:--", font=("Segoe UI", 52, "bold"))
        self.time_label.pack(anchor="center", pady=(4, 2))

        self.date_label = ttk.Label(outer, text="", font=("Segoe UI", 15))
        self.date_label.pack(anchor="center", pady=(2, 10))

        controls = ttk.Frame(outer)
        controls.pack(fill=tk.X, pady=(0, 8))

        ttk.Checkbutton(
            controls,
            text="24-hour",
            variable=self.use_24h,
            command=self._refresh_now,
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Checkbutton(
            controls,
            text="Show seconds",
            variable=self.show_seconds,
            command=self._refresh_now,
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Checkbutton(
            controls,
            text="UTC",
            variable=self.use_utc,
            command=self._refresh_now,
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Checkbutton(
            controls,
            text="Always on top",
            variable=self.always_on_top,
            command=self._toggle_on_top,
        ).pack(side=tk.LEFT)

        actions = ttk.Frame(outer)
        actions.pack(fill=tk.X)

        self.run_button = ttk.Button(actions, text="Pause", command=self._toggle_running)
        self.run_button.pack(side=tk.LEFT)

        ttk.Button(actions, text="Copy time", command=self._copy_time).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(actions, text="Quit", command=self.root.destroy).pack(side=tk.RIGHT)

        ttk.Label(outer, textvariable=self.status_text).pack(anchor="w", pady=(8, 0))

    def _current_datetime(self) -> datetime:
        if self.use_utc.get():
            return datetime.now(timezone.utc)
        return datetime.now()

    def _time_format(self) -> str:
        if self.use_24h.get():
            return "%H:%M:%S" if self.show_seconds.get() else "%H:%M"
        return "%I:%M:%S %p" if self.show_seconds.get() else "%I:%M %p"

    def _toggle_on_top(self) -> None:
        self.root.attributes("-topmost", self.always_on_top.get())

    def _toggle_running(self) -> None:
        self.running = not self.running
        self.run_button.configure(text="Pause" if self.running else "Resume")
        self.status_text.set("Running" if self.running else "Paused")
        if self.running:
            self._refresh_now()

    def _copy_time(self) -> None:
        now = self._current_datetime()
        text = now.strftime(self._time_format())
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_text.set(f"Copied: {text}")

    def _refresh_now(self) -> None:
        now = self._current_datetime()
        self.time_label.configure(text=now.strftime(self._time_format()))

        zone = "UTC" if self.use_utc.get() else "Local"
        self.date_label.configure(text=f"{now.strftime('%A, %B %d, %Y')}  •  {zone}")

    def _tick(self) -> None:
        if self.running:
            self._refresh_now()
        self.root.after(200, self._tick)


def main() -> None:
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    ClockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
