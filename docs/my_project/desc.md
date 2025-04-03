# Cel projektu

Celem projektu jest opracowanie modelu uczenia maszynowego, który na podstawie dobowych danych meteorologicznych oraz hydrologicznych będzie przewidywał poziom wód lądowych.  
Dane wejściowe pochodzą ze strony [IMGW](https://dane.imgw.pl/) i obejmują:

- Dobowe pomiary meteorologiczne,
- Dobowe pomiary hydrologiczne.

Po wstępnym zapoznaniu się z danymi oraz ich przygotowaniu, zostaną wybrane zmienne niezależne do budowy modelu ML.

---

# Metody

## Wczytywanie metadanych i map

Mapy wykorzystywane w projekcie zawierają następujące warstwy:

- Granice administracyjne,
- Rzeki i jeziora,
- Stacje pomiarowe hydrologiczne i meteorologiczne,
- Podkład geograficzny Polski.

### Źródła danych

- **Granice administracyjne i podkład geograficzny**:  
  Pobierane statycznie jako pliki `.shp` z serwisu GIS Support:  
  [https://gis-support.pl/baza-wiedzy-2/dane-do-pobrania/granice-administracyjne/](https://gis-support.pl/baza-wiedzy-2/dane-do-pobrania/granice-administracyjne/)

- **Stacje IMGW (hydrologiczne i meteorologiczne)**:  
  Lokalizacje oraz kody stacji pobierane są dynamicznie poprzez **API IMGW**.

### Format danych

Po wczytaniu dane są przetwarzane do formatu tabelarycznego (np. DataFrame), co umożliwia dalszą analizę oraz wizualizację.

---

# Implementacja techniczna

## Moduł: `imgw_api.py`

Plik `imgw_api.py` zawiera funkcje odpowiedzialne za pobieranie metadanych dotyczących stacji pomiarowych. Główne funkcje to:

### `get_hydro_metadata()`

- Opis: Pobiera dane dotyczące hydrologicznych stacji pomiarowych.
- Zwraca: Kod stacji, położenie, współrzędne geograficzne.

### `get_meteo_metadata()`

- Opis: Pobiera dane dotyczące meteorologicznych stacji pomiarowych.
- Zwraca: Kod stacji, położenie, współrzędne geograficzne.

---

> 📌 **Uwaga**: Wszystkie dane są przetwarzane zgodnie z wymogami modelu ML — oczyszczane, ujednolicane i zapisywane w jednolitym formacie.

