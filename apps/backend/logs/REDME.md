# Metryki

## Pola i znaczenie

- **day** — numer dnia planu (1‑indeksowany). Jednostka: brak (liczba całkowita).
- **total_route_km** — suma odległości między kolejnymi punktami w planie dnia. Jednostka: kilometry.
Obliczane jako suma dystansów kolejnych miejsc. apps/backend/src/metrics/trip_metrics.py
- **time_conflicts** — liczba konfliktów czasowych w danym dniu (np. wejście przed otwarciem, wyjście po
zamknięciu, przekroczenie końca dnia). Jednostka: liczba zdarzeń. apps/backend/src/metrics/
trip_metrics.py
- **cluster_distance_km** — średnia odległość parowa pomiędzy wszystkimi parami miejsc w dniu. Jednostka:
kilometry. apps/backend/src/metrics/trip_metrics.py
- **sentiment_alignment_pct** — odsetek miejsc, których kategorie/subkategorie pokrywają się z
preferencjami użytkownika. Jednostka: %. Zakres 0–100. apps/backend/src/metrics/trip_metrics.py
- **avoidance_rate** — liczba miejsc, które wchodzą w kategorie oznaczone do unikania. Jednostka: liczba
miejsc. apps/backend/src/metrics/trip_metrics.py
- **diversity_score** — stosunek liczby unikalnych kategorii w planie (z all_categories) do liczby
kategorii preferowanych przez użytkownika. Jednostka: bezwymiarowa. Typowo 0–1, ale może
przekroczyć 1, jeśli plan zawiera kategorie spoza preferencji (licznik nie jest ograniczony do
preferencji). apps/backend/src/metrics/trip_metrics.py

## Założenia czasowe

- Dzień planu ma domyślnie start o 600 minutach (10:00) i koniec o 1320 minutach (22:00). To wpływa
na time_conflicts. apps/backend/src/metrics/trip_metrics.py
