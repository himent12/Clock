# Clock Suite (Desktop)

A polished desktop clock app with **Clock + Stopwatch + Timer** in a clean multi-file codebase.

## Why this version

- Better organization (separated modules and views)
- Better UI (dark themed, tabbed layout)
- Better utility (clock controls + stopwatch + timer)
- Still easy to install and run

## Quick install (Windows)

1. Clone or download the repo.
2. Double-click `install.bat`.
3. Double-click `run.bat`.

That’s it.

## Quick run (Linux/macOS)

```bash
./run.sh
```

## Features

### Clock tab
- Live time + date
- 12/24 hour toggle
- Show/hide seconds
- Local/UTC switch
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
- `clock_app/app.py` - app composition and core orchestration
- `clock_app/core/state.py` - app state model
- `clock_app/utils/time_utils.py` - time formatting/helpers
- `clock_app/views/clock_tab.py` - clock tab widgets
- `clock_app/views/stopwatch_tab.py` - stopwatch tab
- `clock_app/views/timer_tab.py` - timer tab
- `install.bat` - Windows installer/bootstrap
- `run.bat` - Windows launcher
- `run.sh` - Linux/macOS launcher

## Requirements

- Python 3.10+
- Tkinter (included in most Python desktop installs)
