"""Top-level app composition and behavior."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from clock_app.core.state import AppState
from clock_app.utils.time_utils import current_datetime, format_clock_text, format_date_text
from clock_app.views.clock_tab import ClockTab
from clock_app.views.stopwatch_tab import StopwatchTab
from clock_app.views.timer_tab import TimerTab


class ClockApplication:
    """Composed multi-tab desktop app."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.state = AppState()
        self._status_clear_job: int | None = None

        self._configure_root()
        self._configure_styles()
        self._build_ui()
        self._bind_shortcuts()
        self._tick_clock()

    def _configure_root(self) -> None:
        self.root.title("Clock Suite")
        self.root.geometry("680x430")
        self.root.minsize(620, 390)

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        bg = "#10131a"
        card = "#171d27"
        fg = "#ebf0ff"
        accent = "#8eb8ff"

        self.root.configure(bg=bg)

        style.configure("TFrame", background=bg)
        style.configure("TNotebook", background=bg, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(12, 6))

        style.configure("Card.TFrame", background=card)
        style.configure("Clock.Time.TLabel", background=card, foreground=fg, font=("Segoe UI", 52, "bold"))
        style.configure("Clock.SecondaryTime.TLabel", background=card, foreground=accent, font=("Consolas", 42, "bold"))
        style.configure("Clock.Date.TLabel", background=card, foreground="#b8c4de", font=("Segoe UI", 14))
        style.configure("Clock.Status.TLabel", background=card, foreground="#9ba7bf", font=("Segoe UI", 10))

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(container)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.clock_tab = ClockTab(notebook)
        self.clock_tab.configure(style="Card.TFrame")
        notebook.add(self.clock_tab, text="Clock")

        self.stopwatch_tab = StopwatchTab(notebook)
        self.stopwatch_tab.configure(style="Card.TFrame")
        notebook.add(self.stopwatch_tab, text="Stopwatch")

        self.timer_tab = TimerTab(notebook)
        self.timer_tab.configure(style="Card.TFrame")
        notebook.add(self.timer_tab, text="Timer")

        self._build_clock_controls()

    def _build_clock_controls(self) -> None:
        c = self.clock_tab.controls_row
        a = self.clock_tab.actions_row

        self.use_24h = tk.BooleanVar(value=self.state.use_24h)
        self.show_seconds = tk.BooleanVar(value=self.state.show_seconds)
        self.use_utc = tk.BooleanVar(value=self.state.use_utc)
        self.always_on_top = tk.BooleanVar(value=self.state.always_on_top)

        ttk.Checkbutton(c, text="24-hour", variable=self.use_24h, command=self._on_options_changed).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Checkbutton(c, text="Show seconds", variable=self.show_seconds, command=self._on_options_changed).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Checkbutton(c, text="UTC", variable=self.use_utc, command=self._on_options_changed).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Checkbutton(c, text="Always on top", variable=self.always_on_top, command=self._toggle_topmost).pack(side=tk.LEFT)

        self.pause_btn = ttk.Button(a, text="Pause", command=self._toggle_running)
        self.pause_btn.pack(side=tk.LEFT)
        ttk.Button(a, text="Copy time", command=self._copy_time).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(a, text="Quit", command=self.root.destroy).pack(side=tk.RIGHT)

    def _bind_shortcuts(self) -> None:
        self.root.bind("<space>", lambda _event: self._toggle_running())
        self.root.bind("<Control-c>", lambda _event: self._copy_time())
        self.root.bind("<Control-q>", lambda _event: self.root.destroy())

    def _set_status(self, text: str, auto_clear_ms: int | None = None) -> None:
        self.clock_tab.status_label.configure(text=text)
        if self._status_clear_job:
            self.root.after_cancel(self._status_clear_job)
            self._status_clear_job = None
        if auto_clear_ms is not None:
            self._status_clear_job = self.root.after(auto_clear_ms, self._reset_status)

    def _reset_status(self) -> None:
        self.clock_tab.status_label.configure(text="Running" if self.state.running else "Paused")

    def _on_options_changed(self) -> None:
        self.state.use_24h = self.use_24h.get()
        self.state.show_seconds = self.show_seconds.get()
        self.state.use_utc = self.use_utc.get()
        self._refresh_clock_labels()

    def _toggle_topmost(self) -> None:
        self.state.always_on_top = self.always_on_top.get()
        self.root.attributes("-topmost", self.state.always_on_top)

    def _toggle_running(self) -> None:
        self.state.running = not self.state.running
        self.pause_btn.configure(text="Pause" if self.state.running else "Resume")
        self._reset_status()
        if self.state.running:
            self._refresh_clock_labels()

    def _copy_time(self) -> None:
        now = current_datetime(self.state.use_utc)
        text = format_clock_text(now, self.state.use_24h, self.state.show_seconds)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self._set_status(f"Copied: {text}", auto_clear_ms=1800)

    def _refresh_clock_labels(self) -> None:
        now = current_datetime(self.state.use_utc)
        self.clock_tab.time_label.configure(
            text=format_clock_text(now, self.state.use_24h, self.state.show_seconds)
        )
        self.clock_tab.date_label.configure(text=format_date_text(now, self.state.use_utc))

    def _tick_clock(self) -> None:
        if self.state.running:
            self._refresh_clock_labels()
        self.root.after(200, self._tick_clock)


def run() -> None:
    root = tk.Tk()
    ClockApplication(root)
    root.mainloop()
