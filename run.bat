@echo off
setlocal

if not exist .venv\Scripts\python.exe (
  echo Environment not found. Run install.bat first.
  exit /b 1
)

call .venv\Scripts\activate.bat
python main.py
