@echo off
taskkill /F /FI "WINDOWTITLE eq Inventory App*" /T >nul 2>&1
exit
