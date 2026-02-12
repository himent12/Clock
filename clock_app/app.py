"""Top-level app composition and behavior (PySide6)."""

from __future__ import annotations

from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout

from clock_app.core.state import AppState
from clock_app.utils.time_utils import format_clock_text, format_date_text
from clock_app.views.clock_tab import ClockTab
from clock_app.views.stopwatch_tab import StopwatchTab
from clock_app.views.timer_tab import TimerTab


class ClockWindow(QMainWindow):
    """Main PySide clock suite window."""

    def __init__(self) -> None:
        super().__init__()
        self.state = AppState()
        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self._reset_status)

        self.setWindowTitle("Clock Suite")
        self.resize(980, 680)
        self.setMinimumSize(860, 560)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.clock_tab = ClockTab()
        self.stopwatch_tab = StopwatchTab()
        self.timer_tab = TimerTab()

        self.tabs.addTab(self.clock_tab, "World Clock")
        self.tabs.addTab(self.stopwatch_tab, "Stopwatch")
        self.tabs.addTab(self.timer_tab, "Timer")

        self._bind_controls()
        self._bind_shortcuts()
        self._apply_theme()

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._tick_clock)
        self.clock_timer.start(200)

    def _palette(self) -> dict[str, str]:
        if self.state.dark_mode:
            return {
                "bg": "#10131a",
                "card": "#171d27",
                "panel": "#151d2a",
                "side": "#151b27",
                "fg": "#ecf1ff",
                "muted": "#aab5cd",
                "accent": "#2b83ea",
            }
        return {
            "bg": "#ecf0f8",
            "card": "#f4f7ff",
            "panel": "#ffffff",
            "side": "#edf2fb",
            "fg": "#1e2b43",
            "muted": "#5b6c8f",
            "accent": "#2b83ea",
        }

    def _style_sheet(self) -> str:
        p = self._palette()
        return f"""
        QMainWindow, QWidget {{ background: {p['bg']}; color: {p['fg']}; }}
        QTabWidget::pane {{ border: 0; }}
        QTabBar::tab {{ background: {p['card']}; color: {p['muted']}; padding: 10px 18px; border-top-left-radius: 8px; border-top-right-radius: 8px; }}
        QTabBar::tab:selected {{ color: {p['fg']}; background: {p['panel']}; }}

        #TopBar {{ background: {p['card']}; border-top-left-radius: 12px; border-top-right-radius: 12px; }}
        #Sidebar {{ background: {p['side']}; min-width: 260px; }}
        #MainPanel {{ background: {p['panel']}; }}
        #AppTitle {{ font-size: 28px; font-weight: 700; }}
        #TopIcons {{ color: {p['muted']}; font-size: 20px; }}
        #SideTitle {{ font-size: 20px; font-weight: 600; }}

        #TimeLabel {{ font-size: 84px; font-weight: 700; }}
        #DateLabel {{ font-size: 24px; color: {p['muted']}; }}
        #StatusLabel {{ color: {p['muted']}; }}

        QPushButton {{ padding: 8px 14px; border-radius: 8px; border: 1px solid {p['muted']}; background: {p['card']}; }}
        QPushButton:hover {{ border-color: {p['accent']}; }}
        #AccentButton {{ background: {p['accent']}; color: white; border: none; font-weight: 600; }}
        QCheckBox {{ spacing: 8px; padding: 3px 0; }}
        """

    def _bind_controls(self) -> None:
        t = self.clock_tab
        t.use_24h.toggled.connect(self._on_options_changed)
        t.show_seconds.toggled.connect(self._on_options_changed)
        t.use_utc.toggled.connect(self._on_options_changed)
        t.dark_mode.toggled.connect(self._toggle_dark_mode)
        t.always_on_top.toggled.connect(self._toggle_topmost)
        t.pause_btn.clicked.connect(self._toggle_running)
        t.copy_btn.clicked.connect(self._copy_time)
        t.quit_btn.clicked.connect(self.close)

    def _bind_shortcuts(self) -> None:
        QShortcut(QKeySequence("Space"), self, activated=self._toggle_running)
        QShortcut(QKeySequence("Ctrl+C"), self, activated=self._copy_time)
        QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)

    def _apply_theme(self) -> None:
        self.setStyleSheet(self._style_sheet())

    def _on_options_changed(self) -> None:
        t = self.clock_tab
        self.state.use_24h = t.use_24h.isChecked()
        self.state.show_seconds = t.show_seconds.isChecked()
        self.state.use_utc = t.use_utc.isChecked()
        self._refresh_clock_labels()

    def _toggle_dark_mode(self) -> None:
        self.state.dark_mode = self.clock_tab.dark_mode.isChecked()
        self._apply_theme()

    def _toggle_topmost(self) -> None:
        self.state.always_on_top = self.clock_tab.always_on_top.isChecked()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, self.state.always_on_top)
        self.show()

    def _toggle_running(self) -> None:
        self.state.running = not self.state.running
        self.clock_tab.pause_btn.setText("Pause" if self.state.running else "Resume")
        self._reset_status()

    def _copy_time(self) -> None:
        now = QDateTime.currentDateTimeUtc() if self.state.use_utc else QDateTime.currentDateTime()
        text = format_clock_text(
            now.toPython(), self.state.use_24h, self.state.show_seconds
        )
        QApplication.clipboard().setText(text)
        self._set_status(f"Copied: {text}", 1800)

    def _set_status(self, text: str, auto_clear_ms: int | None = None) -> None:
        self.clock_tab.status_label.setText(text)
        self._status_timer.stop()
        if auto_clear_ms is not None:
            self._status_timer.start(auto_clear_ms)

    def _reset_status(self) -> None:
        self.clock_tab.status_label.setText("Running" if self.state.running else "Paused")

    def _refresh_clock_labels(self) -> None:
        now = QDateTime.currentDateTimeUtc() if self.state.use_utc else QDateTime.currentDateTime()
        now_py = now.toPython()
        self.clock_tab.time_label.setText(
            format_clock_text(now_py, self.state.use_24h, self.state.show_seconds)
        )
        self.clock_tab.date_label.setText(format_date_text(now_py, self.state.use_utc))

    def _tick_clock(self) -> None:
        if self.state.running:
            self._refresh_clock_labels()


def run() -> None:
    app = QApplication.instance() or QApplication([])
    window = ClockWindow()
    window.show()
    app.exec()
