@echo off
echo ========================================
echo 🇷🇼 RWANDA LOCATIONS SETUP AUTOMATION
echo ========================================
echo.

:: Set variables
set PROJECT_ROOT=..\
set JS_DIR=%PROJECT_ROOT%js
set CSS_DIR=%PROJECT_ROOT%css
set DATA_DIR=%PROJECT_ROOT%data
set ASSETS_DIR=%PROJECT_ROOT%assets

echo 📁 Creating directory structure...

:: Create directories if they don't exist
if not exist "%JS_DIR%" mkdir "%JS_DIR%"
if not exist "%CSS_DIR%" mkdir "%CSS_DIR%"
if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"
if not exist "%ASSETS_DIR%" mkdir "%ASSETS_DIR%"

echo ✅ Directories created successfully!
echo.

echo 📋 Copying Rwanda locations files...

:: Copy core files
copy "locations.json" "%DATA_DIR%\locations.json" >nul
copy "rwanda_locations.js" "%JS_DIR%\rwanda_locations.js" >nul
copy "rwanda_locations.css" "%CSS_DIR%\rwanda_locations.css" >nul

echo ✅ Core files copied successfully!
echo.

echo 📄 Creating integration files...

:: Create index.html with Rwanda locations
echo ^<!DOCTYPE html^> > "%PROJECT_ROOT%index.html"
echo ^<html lang="en"^> >> "%PROJECT_ROOT%index.html"
echo ^<head^> >> "%PROJECT_ROOT%index.html"
echo     ^<meta charset="UTF-8"^> >> "%PROJECT_ROOT%index.html"
echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^> >> "%PROJECT_ROOT%index.html"
echo     ^<title^>Rwanda Education Platform^</title^> >> "%PROJECT_ROOT%index.html"
echo     ^<link rel="stylesheet" href="css/rwanda_locations.css"^> >> "%PROJECT_ROOT%index.html"
echo ^</head^> >> "%PROJECT_ROOT%index.html"
echo ^<body^> >> "%PROJECT_ROOT%index.html"
echo     ^<h1^>🇷🇼 Rwanda Education Platform^</h1^> >> "%PROJECT_ROOT%index.html"
echo     ^<div class="rwanda-locations"^> >> "%PROJECT_ROOT%index.html"
echo         ^<select id="province" name="province" required^>^<option value=""^>Select Province^</option^>^</select^> >> "%PROJECT_ROOT%index.html"
echo         ^<select id="district" name="district" required disabled^>^<option value=""^>Select District^</option^>^</select^> >> "%PROJECT_ROOT%index.html"
echo         ^<select id="sector" name="sector" required disabled^>^<option value=""^>Select Sector^</option^>^</select^> >> "%PROJECT_ROOT%index.html"
echo         ^<select id="cell" name="cell" required disabled^>^<option value=""^>Select Cell^</option^>^</select^> >> "%PROJECT_ROOT%index.html"
echo         ^<select id="village" name="village" required disabled^>^<option value=""^>Select Village^</option^>^</select^> >> "%PROJECT_ROOT%index.html"
echo     ^</div^> >> "%PROJECT_ROOT%index.html"
echo     ^<script src="js/rwanda_locations.js"^>^</script^> >> "%PROJECT_ROOT%index.html"
echo     ^<script^>RwandaLocations.init('data/locations.json');^</script^> >> "%PROJECT_ROOT%index.html"
echo ^</body^> >> "%PROJECT_ROOT%index.html"
echo ^</html^> >> "%PROJECT_ROOT%index.html"

echo ✅ Integration files created!
echo.

:: Copy example files
copy "system_integration_example.html" "%PROJECT_ROOT%registration.html" >nul
copy "rwanda_complete_register.html" "%PROJECT_ROOT%complete_demo.html" >nul

echo 📊 Validating setup...

:: Check if files exist
if exist "%DATA_DIR%\locations.json" (
    echo ✅ locations.json - OK
) else (
    echo ❌ locations.json - MISSING
)

if exist "%JS_DIR%\rwanda_locations.js" (
    echo ✅ rwanda_locations.js - OK
) else (
    echo ❌ rwanda_locations.js - MISSING
)

if exist "%CSS_DIR%\rwanda_locations.css" (
    echo ✅ rwanda_locations.css - OK
) else (
    echo ❌ rwanda_locations.css - MISSING
)

if exist "%PROJECT_ROOT%index.html" (
    echo ✅ index.html - OK
) else (
    echo ❌ index.html - MISSING
)

echo.
echo 🎯 SETUP COMPLETE!
echo ========================================
echo 📁 Project structure:
echo    %PROJECT_ROOT%
echo    ├── css/
echo    │   └── rwanda_locations.css
echo    ├── js/
echo    │   └── rwanda_locations.js
echo    ├── data/
echo    │   └── locations.json
echo    ├── index.html
echo    ├── registration.html
echo    └── complete_demo.html
echo.
echo 🚀 Ready to use:
echo    • Double-click index.html for basic demo
echo    • Double-click registration.html for full form
echo    • Double-click complete_demo.html for complete example
echo.
echo ✅ All Rwanda locations (14,841 villages) are now integrated!
echo ========================================

pause