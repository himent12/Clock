"""Application state container."""

from dataclasses import dataclass


@dataclass
class AppState:
    """Mutable UI state for the desktop app."""

    running: bool = True
    use_24h: bool = True
    show_seconds: bool = True
    use_utc: bool = False
    always_on_top: bool = False
