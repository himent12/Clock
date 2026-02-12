@echo off
setlocal EnableExtensions

title Clock Suite Launcher

REM Always run from this script's directory (for double-click launches)
cd /d "%~dp0"

set "LOG_FILE=run-error.log"
if exist "%LOG_FILE%" del /q "%LOG_FILE%"

echo ==========================================
echo         Clock Suite Launcher
echo ==========================================

if not exist .venv\Scripts\python.exe (
  echo [INFO] Virtual environment not found.
  echo [INFO] Running install.bat first...
  call install.bat
  if errorlevel 1 (
    echo [ERROR] Install failed. Press any key to close.
    pause >nul
    exit /b 1
  )
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo [ERROR] Failed to activate environment.
  echo [HINT] Run install.bat manually and retry.
  pause
  exit /b 1
)

echo [INFO] Launching app...
python main.py 1>>"%LOG_FILE%" 2>>&1
set "EXIT_CODE=%errorlevel%"

if not "%EXIT_CODE%"=="0" (
  echo.
  echo [ERROR] App exited with code %EXIT_CODE%.
  echo [INFO] Error output saved to %LOG_FILE%
  type "%LOG_FILE%"
  echo.
  echo Press any key to close.
  pause >nul
  exit /b %EXIT_CODE%
)

if exist "%LOG_FILE%" del /q "%LOG_FILE%"
exit /b 0
