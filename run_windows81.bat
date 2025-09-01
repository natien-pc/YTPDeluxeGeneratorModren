@echo off
REM Launcher for YTP Deluxe Generator on Windows 8.1
REM Make sure python (3.x) is on PATH or provide full path to python.exe
SETLOCAL
if exist "%~dp0\python.exe" (
  "%~dp0\python.exe" main.py
) else (
  python main.py
)
ENDLOCAL
pause