"""Clock tab UI inspired by modern split-pane clock suites."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class ClockTab(ttk.Frame):
    """Main clock page with settings sidebar + display panel."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=0)

        self.top_bar = ttk.Frame(self, style="Card.TFrame", padding=(16, 12))
        self.top_bar.pack(fill=tk.X)

        self.app_title = ttk.Label(
            self.top_bar,
            text="Aetherial Clock Suite",
            style="Clock.AppTitle.TLabel",
        )
        self.app_title.pack(side=tk.LEFT)

        self.icon_row = ttk.Frame(self.top_bar, style="Card.TFrame")
        self.icon_row.pack(side=tk.RIGHT)

        ttk.Label(self.icon_row, text="⌕", style="Clock.Icon.TLabel").pack(side=tk.LEFT, padx=8)
        ttk.Label(self.icon_row, text="⭳", style="Clock.Icon.TLabel").pack(side=tk.LEFT, padx=8)
        ttk.Label(self.icon_row, text="☰", style="Clock.Icon.TLabel").pack(side=tk.LEFT, padx=8)

        self.content = ttk.Frame(self, style="Card.TFrame")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.sidebar = ttk.Frame(self.content, style="Sidebar.TFrame", padding=(16, 16))
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(
            self.sidebar,
            text="Settings",
            style="Clock.SideTitle.TLabel",
        ).pack(anchor="w", pady=(0, 12))

        self.controls_row = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        self.controls_row.pack(fill=tk.X)

        self.side_actions = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        self.side_actions.pack(fill=tk.X, pady=(18, 0))

        ttk.Separator(self.sidebar).pack(fill=tk.X, pady=12)

        self.dev_tools = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        self.dev_tools.pack(fill=tk.X)

        self.actions_row = ttk.Frame(self.dev_tools, style="Sidebar.TFrame")
        self.actions_row.pack(fill=tk.X, pady=(8, 0))

        self.main_panel = ttk.Frame(self.content, style="MainPanel.TFrame", padding=(26, 24))
        self.main_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.time_label = ttk.Label(self.main_panel, text="--:--:--", style="Clock.Time.TLabel")
        self.time_label.pack(anchor="center", pady=(24, 6))

        self.date_label = ttk.Label(self.main_panel, text="", style="Clock.Date.TLabel")
        self.date_label.pack(anchor="center", pady=(0, 20))

        self.wave = tk.Canvas(self.main_panel, height=90, width=320, highlightthickness=0, bd=0)
        self.wave.pack(anchor="center")

        self.status_label = ttk.Label(self.main_panel, text="Running", style="Clock.Status.TLabel")
        self.status_label.pack(anchor="w", pady=(18, 0))

    def draw_wave(self, panel_bg: str, accent: str, baseline: str, dot: str) -> None:
        """Redraw decorative wave to match current theme."""
        self.wave.configure(bg=panel_bg)
        self.wave.delete("all")
        self.wave.create_line(20, 50, 300, 50, fill=baseline, width=1)
        self.wave.create_line(
            40,
            50,
            80,
            62,
            120,
            20,
            160,
            62,
            200,
            30,
            240,
            58,
            280,
            40,
            fill=accent,
            smooth=True,
            width=2,
        )
        self.wave.create_oval(157, 47, 163, 53, fill=dot, outline="")
