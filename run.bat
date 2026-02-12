@echo off
setlocal EnableExtensions

title Clock Suite Launcher

if not exist .venv\Scripts\python.exe (
  echo Virtual environment not found.
  echo Running install.bat first...
  call install.bat
  if errorlevel 1 exit /b 1
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo [ERROR] Failed to activate environment.
  exit /b 1
)

python main.py
set EXIT_CODE=%errorlevel%
if not "%EXIT_CODE%"=="0" (
  echo.
  echo [ERROR] App exited with code %EXIT_CODE%.
)
exit /b %EXIT_CODE%
