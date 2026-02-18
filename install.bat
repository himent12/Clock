@echo off
setlocal EnableExtensions

title Clock Suite Installer
cd /d "%~dp0"

echo [Clock Suite] Installing...

where py >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python launcher (py) not found.
  echo Install Python 3 from: https://www.python.org/downloads/
  pause
  exit /b 1
)

if not exist .venv (
  py -3 -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed creating virtual environment.
    pause
    exit /b 1
  )
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo [ERROR] Failed to activate virtual environment.
  pause
  exit /b 1
)

python -m pip install --disable-pip-version-check --upgrade pip
python -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Dependency installation failed.
  pause
  exit /b 1
)

echo [OK] Done. Launch with run.bat
exit /b 0
