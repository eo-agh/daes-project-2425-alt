## 4.04.2025
### Problem:
Brak Meta Danych Stacji Pomiarowych - Hydro

### Rozwiązanie:
Wysłano Maila z prośbą o udostępnienie danych do IMGW.
W razie gdyby nie otrzymano pozytywnego odzewu, meta dane stacji zostaną stworzone sztucznie poprzez mapowanie nazw stacji do miejscowości, w których się znajdują.

Update: Są dostępne przez API w formacie JSON.

### Problem:
Meta Dane Stacji Pomiarowych - Meteo w formacie PDF.

Update: Są dostępne przez API w formacie JSON

### Rozwiązanie:
Pomysł: Wykorzystanie modułu przetwarzania obrazów poprzez LLM w celu ekstrakcji danych o geolokacji stacji pomiarowych. Jeśli to nie wyjdzie, zastosujemy rozwiązanie
analogiczne do "Hydro".

### Problem:
Pobieranie danych pomiarowych Hydro i Meteo.

### Rozwiązanie: 

1. Połączenie się z API archiwum danych IMGW. Podejście automatyczne [Trudniejsze].
	1.1 Z opcją stworzenia lokalnej bazy danych w celu zredukowania ilości zapytań i niepotrzebnych czynności związanych z czyszczeniem danych
	1.2 Wykonywania zapytań "za każdym razem" wraz z implementacją automatycznego czyszczenia danych po otrzymaniu danych z zapytania.
2. Pobranie danych ręcznie i zapisanie ich w lokalnej bazie danych.

### Problem: 
Jakość danych Pomiarowych. Dane w zależności od roku, mogą różnić się formatem.

### Rozwiązanie:
Eksploracyjna analiza danych i preprocessing danych.

### Problem: 
Wybranie zakresu lat do analizy.

### Rozwiązanie:
Eksploracyja analiza danych. Na podstawie wstępnego przeglądu danych, ustalimy zakres danych do analizy.

## 28.03.2025

Postęp: Zapoznano się ze struktura plików. Podjęcie decyzji o temacie projektu.

Problemy / kwestie do przedyskutowania: Brak podanej informacji o położeniu stacji hydrologicznych. Dane dla stacji meteorologicznych zapisane w formacie PDF.

## 21.03.2025

Postęp: Wstępnie ustalono zakres projektu. Wybrano dane, które zostaną wykorzystane w projekcie.

Problemy / kwestie do przedyskutowania: Trudności w pobraniu danych przez API.