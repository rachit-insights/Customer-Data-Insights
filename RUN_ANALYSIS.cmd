@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" pipeline.py --mysql
pause
