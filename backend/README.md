## ⚙️ Wymagania wstępne
Aby uruchomić projekt na swoim komputerze, potrzebujesz zainstalować:
1. [Git](https://git-scm.com/)
2. [Docker Desktop](https://www.docker.com/products/docker-desktop/)

---

## 🚀 Szybki start (Instrukcja dla zespołu)

Postępuj zgodnie z poniższymi krokami, aby postawić całe środowisko na czystym komputerze:

### 1. Pobierz repozytorium
```bash
git clone [https://github.com/IgiWAT/CodeBin---Backend.git](https://github.com/IgiWAT/CodeBin---Backend.git)
cd CodeBin---Backend\
```

### 2. Zmień nazwę ".env .example" na ".env"

### 3. Uruchom serwer Docker
```bash
docker-compose up -d
```

### 4. Zbuduj bazę danych
Przypierwszym uruchomieniu trzeba utworzyć bazę danych 
```bash
docker-compose exec web python manage.py migrate
```

### 5. Utworzenie konta administratora
```bash
docker-compose exec web python manage.py createsuperuser
```

## Dostęp do aplikacji:
Aplikacja główna: [localhost](http://localhost:8000/)
Panel admina: [admin](http://localhost:8000/admin/)
Formaty JSON: [JSON](http://localhost:8000/api/kody/) 

## Zatrzymanie serwera Docker
```bash
docker-compose down
```

