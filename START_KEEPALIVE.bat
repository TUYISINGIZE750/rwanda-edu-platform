@echo off
title Keep-Alive Service - Rwanda Edu Platform
echo ========================================
echo KEEP-ALIVE SERVICE STARTED
echo ========================================
echo.
echo This will ping the server every 10 minutes
echo to prevent Render from going to sleep.
echo.
echo Server: https://rwanda-edu-platform.onrender.com
echo.
echo Keep this window open!
echo ========================================
echo.

cd backend
python keep_alive_service.py
