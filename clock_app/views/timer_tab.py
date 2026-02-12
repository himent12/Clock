"""Qt countdown timer tab."""

from __future__ import annotations

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class TimerTab(QWidget):
    """Countdown timer widget."""

    def __init__(self) -> None:
        super().__init__()
        self.remaining_seconds = 5 * 60
        self.running = False

        layout = QVBoxLayout(self)
        self.display = QLabel("05:00")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setFont(QFont("Consolas", 42, QFont.Weight.Bold))
        layout.addStretch()
        layout.addWidget(self.display)

        entry_row = QHBoxLayout()
        entry_row.addWidget(QLabel("Minutes:"))
        self.minutes_entry = QLineEdit("5")
        self.minutes_entry.setMaximumWidth(80)
        entry_row.addWidget(self.minutes_entry)
        entry_row.addStretch()
        layout.addLayout(entry_row)

        actions = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle)
        actions.addWidget(self.start_btn)

        set_btn = QPushButton("Set")
        set_btn.clicked.connect(self.set_minutes)
        actions.addWidget(set_btn)

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset)
        actions.addWidget(reset_btn)
        layout.addLayout(actions)

        self.info = QLabel("")
        layout.addWidget(self.info)
        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)

    def set_minutes(self) -> None:
        value = self.minutes_entry.text().strip()
        if not value.isdigit() or int(value) <= 0:
            self.info.setText("Enter a positive whole minute value.")
            return
        self.remaining_seconds = int(value) * 60
        self.running = False
        self.start_btn.setText("Start")
        self._refresh()
        self.info.setText("Timer configured.")

    def toggle(self) -> None:
        self.running = not self.running
        self.start_btn.setText("Pause" if self.running else "Start")

    def reset(self) -> None:
        self.running = False
        self.start_btn.setText("Start")
        self.remaining_seconds = 5 * 60
        self.minutes_entry.setText("5")
        self._refresh()
        self.info.setText("Timer reset.")

    def _refresh(self) -> None:
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.display.setText(f"{minutes:02d}:{seconds:02d}")

    def _tick(self) -> None:
        if self.running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self._refresh()
            if self.remaining_seconds == 0:
                self.running = False
                self.start_btn.setText("Start")
                self.info.setText("Time is up!")
