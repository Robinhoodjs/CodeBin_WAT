@echo off
echo =======================================
echo    Wylaczanie dockera
echo =======================================
echo.

docker-compose down

echo.


echo =======================================
echo    Budowanie kontenerow na nowo
echo =======================================
echo.

docker-compose up -d --build

echo.