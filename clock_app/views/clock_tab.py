"""Clock tab UI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class ClockTab(ttk.Frame):
    """Main clock display and control widgets."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=14)

        self.time_label = ttk.Label(self, text="--:--:--", style="Clock.Time.TLabel")
        self.time_label.pack(anchor="center", pady=(8, 4))

        self.date_label = ttk.Label(self, text="", style="Clock.Date.TLabel")
        self.date_label.pack(anchor="center", pady=(0, 12))

        self.controls_row = ttk.Frame(self)
        self.controls_row.pack(fill=tk.X, pady=(0, 8))

        self.actions_row = ttk.Frame(self)
        self.actions_row.pack(fill=tk.X)

        self.status_label = ttk.Label(self, text="Running", style="Clock.Status.TLabel")
        self.status_label.pack(anchor="w", pady=(10, 0))
