@echo off
title Inventory App

cd /d "%~dp0"

start "" /b python app.py

:wait
powershell -Command "try { Invoke-WebRequest http://localhost:5000 -UseBasicParsing -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }"

if errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto wait
)

start "" http://localhost:5000

pause
