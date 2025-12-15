@echo off
echo Testing Rwanda Locations API...
echo.

echo Testing provinces endpoint:
curl -X GET "http://localhost:8000/api/v1/locations/provinces" -H "accept: application/json"
echo.
echo.

echo Testing districts for Southern Province:
curl -X GET "http://localhost:8000/api/v1/locations/districts/Southern%%20Province" -H "accept: application/json"
echo.
echo.

echo Testing schools in Kamonyi district:
curl -X GET "http://localhost:8000/api/v1/locations/schools/district/Southern%%20Province/Kamonyi" -H "accept: application/json"
echo.

pause