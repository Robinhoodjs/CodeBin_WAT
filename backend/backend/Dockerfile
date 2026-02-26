# Pobieramy lekki obraz Pythona
FROM python:3.11-slim

# Ustawiamy zmienne środowiskowe (nie twórz plików .pyc, wypisuj logi od razu)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ustawiamy folder roboczy w kontenerze
WORKDIR /app

# Instalujemy zależności systemowe dla PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Kopiujemy requirements i instalujemy biblioteki
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Kopiujemy resztę projektu
COPY . .