@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Follow the setup instructions in README.md to create .venv first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" run.py
pause
