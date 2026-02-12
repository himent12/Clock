@echo off
setlocal EnableExtensions

REM Development cleanup script for Clock Suite
REM Removes local install artifacts created by install/run steps.

echo Cleaning Clock Suite development artifacts...

if exist .venv (
  echo - Removing .venv
  rmdir /s /q .venv
)

if exist __pycache__ (
  echo - Removing root __pycache__
  rmdir /s /q __pycache__
)

for /d /r %%D in (__pycache__) do (
  if exist "%%D" (
    echo - Removing %%D
    rmdir /s /q "%%D"
  )
)

for /r %%F in (*.pyc *.pyo) do (
  if exist "%%F" (
    del /f /q "%%F"
  )
)

echo Done.
echo This removed local runtime/build artifacts only.
exit /b 0
