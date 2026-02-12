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
        self.style = ttk.Style(self.root)
        self.state = AppState()
        self._status_clear_job: int | None = None

        self._configure_root()
        self._apply_theme()
        self._build_ui()
        self._bind_shortcuts()
        self._tick_clock()

    def _configure_root(self) -> None:
        self.root.title("Clock Suite")
        self.root.geometry("900x640")
        self.root.minsize(820, 560)

    def _palette(self) -> dict[str, str]:
        if self.state.dark_mode:
            return {
                "bg": "#10131a",
                "card": "#171d27",
                "sidebar": "#151b27",
                "panel": "#151d2a",
                "fg": "#ecf1ff",
                "muted": "#b6c2de",
                "dim": "#8a96af",
                "accent": "#2b83ea",
            }
        return {
            "bg": "#eceff5",
            "card": "#f5f7fb",
            "sidebar": "#f1f4fa",
            "panel": "#ffffff",
            "fg": "#1c2230",
            "muted": "#4d5b76",
            "dim": "#62708f",
            "accent": "#2b83ea",
        }

    def _apply_theme(self) -> None:
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        p = self._palette()
        self.root.configure(bg=p["bg"])

        self.style.configure("TFrame", background=p["bg"])
        self.style.configure("Card.TFrame", background=p["card"])
        self.style.configure("Sidebar.TFrame", background=p["sidebar"])
        self.style.configure("MainPanel.TFrame", background=p["panel"])

        self.style.configure("TNotebook", background=p["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=p["card"], foreground=p["muted"], padding=(22, 10))
        self.style.map("TNotebook.Tab", foreground=[("selected", p["fg"])], background=[("selected", p["panel"])])

        self.style.configure("TCheckbutton", background=p["sidebar"], foreground=p["muted"], font=("Segoe UI", 12))
        self.style.map("TCheckbutton", foreground=[("selected", p["fg"]), ("active", p["fg"])])

        self.style.configure("TButton", font=("Segoe UI", 11), padding=(10, 6))
        self.style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), padding=(14, 8), background=p["accent"], foreground="#ffffff")

        self.style.configure("Clock.AppTitle.TLabel", background=p["card"], foreground=p["fg"], font=("Segoe UI", 19, "bold"))
        self.style.configure("Clock.Icon.TLabel", background=p["card"], foreground=p["dim"], font=("Segoe UI", 17))
        self.style.configure("Clock.SideTitle.TLabel", background=p["sidebar"], foreground=p["fg"], font=("Segoe UI", 14, "bold"))
        self.style.configure("Clock.Time.TLabel", background=p["panel"], foreground=p["fg"], font=("Segoe UI", 62, "bold"))
        self.style.configure("Clock.SecondaryTime.TLabel", background=p["card"], foreground=p["accent"], font=("Consolas", 42, "bold"))
        self.style.configure("Clock.Date.TLabel", background=p["panel"], foreground=p["muted"], font=("Segoe UI", 16))
        self.style.configure("Clock.Status.TLabel", background=p["panel"], foreground=p["dim"], font=("Segoe UI", 10))

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=14)
        container.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(container)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.clock_tab = ClockTab(notebook)
        self.clock_tab.configure(style="Card.TFrame")
        notebook.add(self.clock_tab, text="World Clock")

        self.stopwatch_tab = StopwatchTab(notebook)
        self.stopwatch_tab.configure(style="Card.TFrame")
        notebook.add(self.stopwatch_tab, text="Stopwatch")

        self.timer_tab = TimerTab(notebook)
        self.timer_tab.configure(style="Card.TFrame")
        notebook.add(self.timer_tab, text="Timer")

        self._build_clock_controls()

    def _build_clock_controls(self) -> None:
        c = self.clock_tab.controls_row
        side = self.clock_tab.side_actions
        a = self.clock_tab.actions_row

        self.use_24h = tk.BooleanVar(value=self.state.use_24h)
        self.show_seconds = tk.BooleanVar(value=self.state.show_seconds)
        self.use_utc = tk.BooleanVar(value=self.state.use_utc)
        self.always_on_top = tk.BooleanVar(value=self.state.always_on_top)
        self.dark_mode = tk.BooleanVar(value=self.state.dark_mode)

        ttk.Checkbutton(c, text="24-hour format", variable=self.use_24h, command=self._on_options_changed).pack(anchor="w", pady=4)
        ttk.Checkbutton(c, text="Show seconds", variable=self.show_seconds, command=self._on_options_changed).pack(anchor="w", pady=4)
        ttk.Checkbutton(c, text="UTC mode", variable=self.use_utc, command=self._on_options_changed).pack(anchor="w", pady=4)
        ttk.Checkbutton(c, text="Dark mode", variable=self.dark_mode, command=self._toggle_dark_mode).pack(anchor="w", pady=4)
        ttk.Checkbutton(c, text="Always on top", variable=self.always_on_top, command=self._toggle_topmost).pack(anchor="w", pady=4)

        ttk.Label(side, text="⏻ Add City", style="Clock.Date.TLabel").pack(anchor="w", pady=(2, 6))
        ttk.Label(side, text="Time Zone Converter", style="Clock.Date.TLabel").pack(anchor="w", pady=(2, 12))
        ttk.Button(side, text="Alarm Settings", style="Accent.TButton").pack(anchor="w")

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

    def _toggle_dark_mode(self) -> None:
        self.state.dark_mode = self.dark_mode.get()
        self._apply_theme()
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
        self.clock_tab.time_label.configure(text=format_clock_text(now, self.state.use_24h, self.state.show_seconds))
        self.clock_tab.date_label.configure(text=format_date_text(now, self.state.use_utc))

    def _tick_clock(self) -> None:
        if self.state.running:
            self._refresh_clock_labels()
        self.root.after(200, self._tick_clock)


def run() -> None:
    root = tk.Tk()
    ClockApplication(root)
    root.mainloop()
