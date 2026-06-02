# Zadanie 2 – GitHub Actions CI/CD (Docker + GHCR)

## Opis projektu

Projekt przedstawia aplikację webową napisaną w Python (Flask), która umożliwia sprawdzenie aktualnej pogody dla wybranych miast. Dane pogodowe pobierane są z API Open-Meteo.

Aplikacja została skonteneryzowana przy użyciu Dockera oraz zautomatyzowana w procesie CI/CD przy użyciu GitHub Actions.

---

## Funkcjonalność aplikacji

- wybór miasta z listy
- pobieranie aktualnych danych pogodowych (temperatura, wiatr)
- prosty interfejs webowy (Flask + HTML template)
- uruchomienie w kontenerze Docker

---

## Uruchomienie lokalne

docker build -t weather-app .
docker run -p 8080:8080 weather-app


## Aplikacja dostępna pod:

http://localhost:8080


## Dockerfile

Aplikacja działa w oparciu o multi-stage build:

etap builder: instalacja zależności Python
etap runtime: minimalny obraz Alpine

Dodatkowo:

HEALTHCHECK dla kontenera
konfiguracja portu 8080
optymalizacja rozmiaru obrazu


## GitHub Actions CI/CD
Pipeline realizuje następujące kroki:


### 1. Checkout kodu

Pobranie repozytorium do runnera.


### 2. Build multi-architecture

Obraz budowany dla architektur:

linux/amd64
linux/arm64

Wykorzystano Docker Buildx + QEMU.


### 3. Cache buildów

Cache przechowywany jest w publicznym repozytorium Docker Hub:

docker.io/mynion/cache

Tryb:

mode=max

Zapewnia to przyspieszenie kolejnych buildów.


### 4. Skan bezpieczeństwa (CVE)

Obraz jest skanowany przy użyciu Trivy.

Pipeline przerywa build, jeśli wykryte zostaną podatności:

HIGH
CRITICAL


### 5. Publikacja obrazu

Obraz publikowany jest do GitHub Container Registry:

ghcr.io/mynion/pawcho_zadanie2

Tagi:

latest (najnowsza wersja)
commit SHA (wersja identyfikowalna)
semver (1.0.x – numer builda)


### 6. Smoke test

Po zbudowaniu obrazu uruchamiany jest test kontenera:

start kontenera
sprawdzenie endpointu HTTP
zatrzymanie kontenera


## Tagowanie obrazów

Zastosowano trzy typy tagów:

latest – najnowsza wersja
github.sha – unikalna wersja dla commitów
1.0.x – wersjonowanie semantyczne buildów


## Uzasadnienie cache

Cache został umieszczony w Docker Hub, ponieważ:

umożliwia współdzielenie cache pomiędzy runnerami
przyspiesza budowanie obrazów
spełnia wymaganie użycia registry cache w trybie max


## Uzasadnienie CVE scan

Wybrano Trivy, ponieważ:

jest darmowy i open-source
działa w CI bez dodatkowej konfiguracji serwera
umożliwia blokowanie buildów przy krytycznych podatnościach
jest standardem w pipeline’ach Docker CI/CD


## Link do obrazu

ghcr.io/mynion/pawcho_zadanie2:latest