@echo off
cls
echo.
echo ██████╗ ██╗    ██╗ █████╗ ███╗   ██╗██████╗  █████╗ 
echo ██╔══██╗██║    ██║██╔══██╗████╗  ██║██╔══██╗██╔══██╗
echo ██████╔╝██║ █╗ ██║███████║██╔██╗ ██║██║  ██║███████║
echo ██╔══██╗██║███╗██║██╔══██║██║╚██╗██║██║  ██║██╔══██║
echo ██║  ██║╚███╔███╔╝██║  ██║██║ ╚████║██████╔╝██║  ██║
echo ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝
echo.
echo 🇷🇼 RWANDA LOCATIONS - AUTOMATED SETUP
echo =======================================

:: Generate complete registration form
echo 🔄 Generating complete registration form...
python generate_full_register.py

:: Run main setup
echo 🔄 Setting up project structure...
call setup_rwanda_locations.bat

:: Start local server for testing
echo 🌐 Starting local server...
start "" "http://localhost:8080"
python -m http.server 8080

echo.
echo ✅ SETUP COMPLETE! 
echo 🌐 Server running at http://localhost:8080
echo 📝 Registration form: http://localhost:8080/rwanda_complete_register.html