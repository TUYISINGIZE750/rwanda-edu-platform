@echo off
cd /d "%~dp0"
python migrations/migrate_notifications.py
pause
