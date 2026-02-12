"""Stopwatch tab UI and behavior."""

from __future__ import annotations

import time
import tkinter as tk
from tkinter import ttk


class StopwatchTab(ttk.Frame):
    """Lightweight stopwatch implementation."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)
        self._start_time = 0.0
        self._elapsed = 0.0
        self._running = False

        self.display = ttk.Label(self, text="00:00.00", style="Clock.SecondaryTime.TLabel")
        self.display.pack(anchor="center", pady=(12, 10))

        row = ttk.Frame(self)
        row.pack(anchor="center")

        self.start_btn = ttk.Button(row, text="Start", command=self.toggle)
        self.start_btn.pack(side=tk.LEFT)
        ttk.Button(row, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=(8, 0))

        self._tick()

    def toggle(self) -> None:
        if self._running:
            self._elapsed += time.perf_counter() - self._start_time
            self._running = False
            self.start_btn.configure(text="Start")
        else:
            self._start_time = time.perf_counter()
            self._running = True
            self.start_btn.configure(text="Pause")

    def reset(self) -> None:
        self._running = False
        self._elapsed = 0.0
        self.start_btn.configure(text="Start")
        self.display.configure(text="00:00.00")

    def _tick(self) -> None:
        total = self._elapsed
        if self._running:
            total += time.perf_counter() - self._start_time

        minutes = int(total // 60)
        seconds = total % 60
        self.display.configure(text=f"{minutes:02d}:{seconds:05.2f}")
        self.after(30, self._tick)
