@echo off
setlocal

REM Simple installer for Clock Suite on Windows
where py >nul 2>nul
if %errorlevel% neq 0 (
  echo Python launcher not found. Install Python 3 from https://www.python.org/downloads/
  exit /b 1
)

if not exist .venv (
  echo [1/3] Creating virtual environment...
  py -3 -m venv .venv
  if %errorlevel% neq 0 exit /b 1
)

echo [2/3] Activating environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 exit /b 1

echo [3/3] Upgrading pip and installing requirements...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt
if %errorlevel% neq 0 exit /b 1

echo.
echo Install complete.
echo Run the app with: run.bat
exit /b 0
