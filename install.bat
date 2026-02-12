@echo off
setlocal EnableExtensions

title Clock Suite Installer

REM Always run from this script's directory (for double-click launches)
cd /d "%~dp0"

echo ==========================================
echo         Clock Suite Installer
echo ==========================================

echo [Check] Looking for Python launcher...
where py >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python launcher not found.
  echo Install Python 3 from https://www.python.org/downloads/ and try again.
  pause
  exit /b 1
)

if not exist requirements.txt (
  echo [ERROR] requirements.txt not found. Run this from the project root.
  pause
  exit /b 1
)

if not exist .venv (
  echo [Step 1/4] Creating virtual environment...
  py -3 -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create .venv
    pause
    exit /b 1
  )
) else (
  echo [Step 1/4] Virtual environment already exists.
)

echo [Step 2/4] Activating environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo [ERROR] Could not activate virtual environment.
  pause
  exit /b 1
)

echo [Step 3/4] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 echo [WARN] pip upgrade failed. Continuing...

echo [Step 4/4] Installing requirements...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Requirements install failed.
  pause
  exit /b 1
)

echo.
echo [OK] Install complete.
echo Run the app with: run.bat
exit /b 0
