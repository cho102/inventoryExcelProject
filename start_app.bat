@echo off
title Inventory App

cd /d "%~dp0"

start "" /b python app.py

timeout /t 2 /nobreak >nul

start "" http://localhost:5000

pause
