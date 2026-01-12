# Instrukcje dla Windows (polski)

## Wymagania

Windows 10/11 z wlaczona wirtualizacja, WSL2 i Docker Desktop (dla uruchomienia obrazu backend + llama).

## Instalacja krok po kroku

1) Zainstaluj aplikacje CAPRI Desktop uruchamiajac instalator `CAPRI Setup 0.1.0.exe`. Postepuj wedlug kreatora instalacji i upewnij sie, ze aplikacja startuje poprawnie.
2) Rozpakuj paczke z backendem (`capri.zip`) do katalogu roboczego (np. `C:\capri`). W folderze powinny znalezc sie pliki projektu wraz z `docker-compose.yml`.
3) W rozpakowanym folderze uruchom:

   ```powershell
   docker compose up
   ```

## Rezultat

Polecenie wystartuje backend pod adresem <http://localhost:5000> oraz serwis Llama pod <http://localhost:3000>. Pierwsze uruchomienie moze pobrac ~600MB modelu do `apps/llama/models`.
