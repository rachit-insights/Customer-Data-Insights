@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" -m jupyterlab Customer_Shopping_Behavior_Analysis.ipynb
pause
