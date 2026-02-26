@echo off
echo =======================================
echo    Stawianie bazy danych na nowo
echo =======================================
echo.

docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

echo.
pause