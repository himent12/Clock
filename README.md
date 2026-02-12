# Clock Suite (Desktop)

A polished desktop clock app with **World Clock + Stopwatch + Timer** and a modern split-pane design.

## Why this version

- Better organization (separated modules and views)
- Better UI inspired by premium clock suites
- Better utility (clock controls + stopwatch + timer)
- Simple installer and cleanup scripts for Windows

## Quick install (Windows)

1. Clone or download the repo.
2. Double-click `install.bat`.
3. Double-click `run.bat`.

For development cleanup/uninstall of local artifacts, run `remove.bat`.
Use `remove.bat --all` to also clear pip cache.

That’s it.

## Quick run (Linux/macOS)

```bash
./run.sh
```

## Features

### World Clock tab
- Modern split layout with left settings panel and main time display
- 24-hour format toggle
- Show/hide seconds
- UTC mode
- Dark mode toggle
- Always-on-top
- Pause/resume updates
- Copy current time
- Keyboard shortcuts:
  - `Space`: pause/resume
  - `Ctrl+C`: copy time
  - `Ctrl+Q`: quit app

### Stopwatch tab
- Start/pause
- Reset
- Smooth live updates

### Timer tab
- Set minutes
- Start/pause
- Reset
- Completion message

## Project structure

- `main.py` - app entrypoint
- `clock_app/app.py` - app composition and orchestration
- `clock_app/core/state.py` - app state model
- `clock_app/utils/time_utils.py` - time formatting/helpers
- `clock_app/views/clock_tab.py` - world clock tab widgets
- `clock_app/views/stopwatch_tab.py` - stopwatch tab
- `clock_app/views/timer_tab.py` - timer tab
- `install.bat` - Windows installer/bootstrap
- `run.bat` - Windows launcher
- `remove.bat` - Windows cleanup/uninstall (dev artifacts)
- `run.sh` - Linux/macOS launcher

## Requirements

- Python 3.10+
- Tkinter (included in most Python desktop installs)
