@echo off
setlocal EnableExtensions
REM Conflict-resolved script baseline

title Clock Suite Cleanup

echo ==========================================
echo         Clock Suite Cleanup
echo ==========================================
echo Removing local development artifacts...

if exist .venv (
  echo - Removing .venv
  rmdir /s /q .venv
)

for /d /r %%D in (__pycache__) do (
  if exist "%%D" (
    echo - Removing %%D
    rmdir /s /q "%%D"
  )
)

for /r %%F in (*.pyc *.pyo) do (
  if exist "%%F" del /f /q "%%F"
)

if /I "%~1"=="--all" (
  echo - Removing pip cache (if present)
  if exist "%LocalAppData%\pip\Cache" rmdir /s /q "%LocalAppData%\pip\Cache"
)

echo [OK] Cleanup complete.
echo Tip: use "remove.bat --all" to also clear pip cache.
exit /b 0
