@echo off
echo =======================================
echo    Tworzenie kontenera + instalacja bibliotek
echo =======================================
echo.

docker-compose up -d --build

echo.

echo =======================================
echo    Migracja bazy danych
echo =======================================
echo.

docker-compose exec web python manage.py migrate

echo.


echo =======================================
echo    Tworzenie superusera
echo =======================================
echo.

docker-compose exec web python manage.py createsuperuser

echo.


