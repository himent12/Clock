"""Countdown timer tab."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class TimerTab(ttk.Frame):
    """Simple countdown timer."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)

        self.remaining_seconds = 5 * 60
        self.running = False

        self.display = ttk.Label(self, text="05:00", style="Clock.SecondaryTime.TLabel")
        self.display.pack(anchor="center", pady=(10, 10))

        entry_row = ttk.Frame(self)
        entry_row.pack(anchor="center", pady=(0, 8))

        ttk.Label(entry_row, text="Minutes:").pack(side=tk.LEFT, padx=(0, 6))
        self.minutes_var = tk.StringVar(value="5")
        self.minutes_entry = ttk.Entry(entry_row, width=5, textvariable=self.minutes_var)
        self.minutes_entry.pack(side=tk.LEFT)

        action_row = ttk.Frame(self)
        action_row.pack(anchor="center")

        self.start_btn = ttk.Button(action_row, text="Start", command=self.toggle)
        self.start_btn.pack(side=tk.LEFT)
        ttk.Button(action_row, text="Set", command=self.set_minutes).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(action_row, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=(8, 0))

        self.info = ttk.Label(self, text="")
        self.info.pack(anchor="center", pady=(10, 0))

        self._tick()

    def set_minutes(self) -> None:
        value = self.minutes_var.get().strip()
        if not value.isdigit() or int(value) <= 0:
            self.info.configure(text="Enter a positive whole minute value.")
            return
        self.remaining_seconds = int(value) * 60
        self.running = False
        self.start_btn.configure(text="Start")
        self._refresh()
        self.info.configure(text="Timer configured.")

    def toggle(self) -> None:
        self.running = not self.running
        self.start_btn.configure(text="Pause" if self.running else "Start")

    def reset(self) -> None:
        self.running = False
        self.start_btn.configure(text="Start")
        self.remaining_seconds = 5 * 60
        self.minutes_var.set("5")
        self._refresh()
        self.info.configure(text="Timer reset.")

    def _refresh(self) -> None:
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.display.configure(text=f"{minutes:02d}:{seconds:02d}")

    def _tick(self) -> None:
        if self.running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self._refresh()
            if self.remaining_seconds == 0:
                self.running = False
                self.start_btn.configure(text="Start")
                self.info.configure(text="Time is up!")
        self.after(1000, self._tick)
