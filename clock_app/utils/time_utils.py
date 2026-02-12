"""Time/date formatting helpers."""

from __future__ import annotations

from datetime import datetime, timezone


def current_datetime(use_utc: bool) -> datetime:
    """Return current datetime in UTC or local timezone."""
    return datetime.now(timezone.utc) if use_utc else datetime.now()


def format_clock_text(now: datetime, use_24h: bool, show_seconds: bool) -> str:
    """Format time text for the clock display."""
    if use_24h:
        return now.strftime("%H:%M:%S" if show_seconds else "%H:%M")
    return now.strftime("%I:%M:%S %p" if show_seconds else "%I:%M %p")


def format_date_text(now: datetime, use_utc: bool) -> str:
    """Format date + zone text for subtitle."""
    zone = "UTC" if use_utc else "Local"
    return f"{now.strftime('%A, %B %d, %Y')}  •  {zone}"
