# Frontend generatora zadań

## Pobranie projektu na własny komputer

1. Utwórz lub przejdź do katalogu, w którym chcesz umieścić projekt.

2. Sklonuj repozytorium:
   `git clone git@github.com:KevinKaluzny/Algo_platforma_WAT--frontend.git`

## Sklonuj repozytorium:

Aby uruchomić projekt lokalnie, wymagany jest zainstalowany Node.js.
Jeśli nie masz go zainstalowanego, pobierz go z oficjalnej strony:
👉 https://nodejs.org/en/download/current.

1. Instalacja paczek:
   `npm install`

2. Uruchomienie aplikacji oraz symulowanego serwera:
   `yarn start`

   Aplikacja uruchomi się domyślnie pod adresem:
	 `http://localhost:3000`

	 Symulowany serwer (json-server) działa na porcie:
	 `http://localhost:3131`

2. Zatrzymanie aplikacji i serwera:
   `Ctrl + C`

## Praca zespołowa

W celu zachowania porządku w repozytorium oraz usprawnienia współpracy zalecane jest stosowanie Gitflow Workflow.

Gitflow zakłada m.in.:

- oddzielną gałąź main (wersja produkcyjna),

- gałąź develop (wersja rozwojowa),

- tworzenie osobnych gałęzi dla nowych funkcjonalności (feature/*),

- pull requesty przed mergowaniem zmian.

Więcej informacji na temat Gitflow:
👉 https://nulab.com/learn/software-development/git-tutorial/git-collaboration/branching-workflows/gitflow-workflow/

## Architektura projektu

Projekt jest aplikacją typu SPA (Single Page Application) stworzoną w oparciu o React.

### Główne technologie

- **React** – budowa interfejsu użytkownika

- **React Router** – obsługa routingu (nawigacja bez przeładowania strony)

- **Redux** – zarządzanie globalnym stanem aplikacji

- **Axios** – komunikacja z API (zapytania HTTP POST/GET)

- **Material UI (MUI)** – komponenty interfejsu użytkownika

- **json-server** – symulacja backendu

- **SCSS Modules** – stylowanie komponentów

- **Yarn** - konkurencyjny menedżer paczek, który jest nieco szybszy od NPM

- **Jest** - testy jednostkowe

### Struktura projektu

    /src
      /components      → komponenty aplikacji (Generator, Parameters, Results itd.)
      /redux           → konfiguracja store i slice'y
      /styles          → pliki stylów
      App.js           → konfiguracja routingu
      index.js         → punkt wejścia aplikacji

    /db
      server.json      → symulowana baza danych (json-server)

    /public
      index.html       → główny plik HTML
      assets           → statyczne zasoby

### Ważna informacja techniczna

Folder db znajduje się w katalogu głównym projektu (a nie w public).
Pozwala to uniknąć niepożądanego przeładowywania aplikacji przez React Dev Server podczas modyfikacji pliku server.json.

### Mechanizm działania generatora

1. Użytkownik wprowadza dane w formularzu.

2. Kliknięcie przycisku powoduje:

   - wysłanie zapytania POST z parametrami do symulowanego serwera,

   - następnie wykonanie zapytania GET w celu pobrania wygenerowanych wyników.

3. Otrzymane dane są zapisywane w Redux store.

4. Komponent Results pobiera dane ze store i renderuje je w interfejsie.

Całość działa bez przeładowania strony, zgodnie z architekturą SPA.