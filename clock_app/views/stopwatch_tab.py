"""Qt stopwatch tab."""

from __future__ import annotations

import time

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class StopwatchTab(QWidget):
    """Stopwatch widget."""

    def __init__(self) -> None:
        super().__init__()
        self._start_time = 0.0
        self._elapsed = 0.0
        self._running = False

        layout = QVBoxLayout(self)
        self.display = QLabel("00:00.00")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setFont(QFont("Consolas", 42, QFont.Weight.Bold))
        layout.addStretch()
        layout.addWidget(self.display)

        row = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle)
        row.addWidget(self.start_btn)

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset)
        row.addWidget(reset_btn)
        layout.addLayout(row)
        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(30)

    def toggle(self) -> None:
        if self._running:
            self._elapsed += time.perf_counter() - self._start_time
            self._running = False
            self.start_btn.setText("Start")
        else:
            self._start_time = time.perf_counter()
            self._running = True
            self.start_btn.setText("Pause")

    def reset(self) -> None:
        self._running = False
        self._elapsed = 0.0
        self.start_btn.setText("Start")
        self.display.setText("00:00.00")

    def _tick(self) -> None:
        total = self._elapsed
        if self._running:
            total += time.perf_counter() - self._start_time

        minutes = int(total // 60)
        seconds = total % 60
        self.display.setText(f"{minutes:02d}:{seconds:05.2f}")
