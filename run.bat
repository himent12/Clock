@echo off
setlocal EnableExtensions

title Clock Suite Launcher
cd /d "%~dp0"

set "LOG_FILE=run-error.log"
if exist "%LOG_FILE%" del /q "%LOG_FILE%"

echo [Clock Suite] Starting...

if not exist .venv\Scripts\python.exe (
  echo [INFO] First run detected. Installing dependencies...
  call install.bat
  if errorlevel 1 (
    echo [ERROR] Install failed.
    pause >nul
    exit /b 1
  )
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo [ERROR] Could not activate .venv
  pause
  exit /b 1
)

python -c "import PySide6" >nul 2>nul
if errorlevel 1 (
  echo [INFO] PySide6 missing. Running install.bat...
  call install.bat
  if errorlevel 1 (
    echo [ERROR] Dependency install failed.
    pause >nul
    exit /b 1
  )
)

python main.py 1>>"%LOG_FILE%" 2>>&1
set "EXIT_CODE=%errorlevel%"

if not "%EXIT_CODE%"=="0" (
  echo [ERROR] App failed with code %EXIT_CODE%
  echo ---- %LOG_FILE% ----
  type "%LOG_FILE%"
  echo ----------------------
  pause >nul
  exit /b %EXIT_CODE%
)

if exist "%LOG_FILE%" del /q "%LOG_FILE%"
exit /b 0
