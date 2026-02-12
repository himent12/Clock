"""Qt World Clock tab UI."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ClockTab(QWidget):
    """World Clock split-pane tab."""

    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        top = QFrame()
        top.setObjectName("TopBar")
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(16, 12, 16, 12)

        title = QLabel("Aetherial Clock Suite")
        title.setObjectName("AppTitle")
        top_layout.addWidget(title)
        top_layout.addStretch()

        icons = QLabel("⌕   ⭳   ☰")
        icons.setObjectName("TopIcons")
        top_layout.addWidget(icons)
        root.addWidget(top)

        content = QHBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(16, 16, 16, 16)

        side_title = QLabel("Settings")
        side_title.setObjectName("SideTitle")
        side_layout.addWidget(side_title)

        self.use_24h = QCheckBox("24-hour format")
        self.use_24h.setChecked(True)
        self.show_seconds = QCheckBox("Show seconds")
        self.show_seconds.setChecked(True)
        self.use_utc = QCheckBox("UTC mode")
        self.dark_mode = QCheckBox("Dark mode")
        self.dark_mode.setChecked(True)
        self.always_on_top = QCheckBox("Always on top")

        for widget in [self.use_24h, self.show_seconds, self.use_utc, self.dark_mode, self.always_on_top]:
            side_layout.addWidget(widget)

        side_layout.addSpacing(12)
        side_layout.addWidget(QLabel("⏻ Add City"))
        side_layout.addWidget(QLabel("Time Zone Converter"))
        self.alarm_btn = QPushButton("Alarm Settings")
        self.alarm_btn.setObjectName("AccentButton")
        side_layout.addWidget(self.alarm_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        side_layout.addStretch()

        content.addWidget(sidebar, 1)

        panel = QFrame()
        panel.setObjectName("MainPanel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(26, 24, 26, 24)

        self.time_label = QLabel("--:--:--")
        self.time_label.setObjectName("TimeLabel")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(QFont("Segoe UI", 46, QFont.Weight.Bold))

        self.date_label = QLabel("")
        self.date_label.setObjectName("DateLabel")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Running")
        self.status_label.setObjectName("StatusLabel")

        self.pause_btn = QPushButton("Pause")
        self.copy_btn = QPushButton("Copy time")
        self.quit_btn = QPushButton("Quit")

        actions = QHBoxLayout()
        actions.addWidget(self.pause_btn)
        actions.addWidget(self.copy_btn)
        actions.addStretch()
        actions.addWidget(self.quit_btn)

        panel_layout.addStretch()
        panel_layout.addWidget(self.time_label)
        panel_layout.addWidget(self.date_label)
        panel_layout.addStretch()
        panel_layout.addLayout(actions)
        panel_layout.addWidget(self.status_label)

        content.addWidget(panel, 2)

        wrap = QWidget()
        wrap.setLayout(content)
        root.addWidget(wrap)
