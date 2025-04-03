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

Po wczytaniu dane są przetwarzane do formatu tabelarycznego (np. DataFrame), a lokalizacje geograficzne zapisywane jako `GeoDataFrame` w układzie współrzędnych **EPSG:2180** (PUWG 1992), co umożliwia ich dalszą analizę przestrzenną i wizualizację.

---

# Implementacja techniczna

## Moduł: `imgw_api.py`

Plik `imgw_api.py` zawiera funkcje odpowiedzialne za pobieranie metadanych dotyczących stacji pomiarowych oraz ich konwersję przestrzenną. Główne funkcje to:

### `get_hydro_metadata(url: str) -> GeoDataFrame`

- **Opis**: Funkcja pobiera metadane dotyczące hydrologicznych stacji pomiarowych ze wskazanego źródła (np. pliku CSV lub adresu URL z API IMGW).
  Na podstawie współrzędnych geograficznych (`lat`, `lon`) tworzy obiekt przestrzenny typu `GeoDataFrame`.

- **Parametry**:
  - `url` (`str`) – ścieżka lokalna lub URL do pliku CSV zawierającego metadane stacji hydrologicznych (w tym kolumny `lat`, `lon`).

- **Zakres działania**:
  - Wczytuje dane jako zwykły `DataFrame`,
  - Tworzy kolumnę `geometry` z punktów (longitude, latitude),
  - Ustawia CRS jako `EPSG:4326` (WGS 84),
  - Przekształca dane przestrzennie do układu PUWG 1992 (`EPSG:2180`).

- **Zwraca**:
  - `GeoDataFrame` z geometrią punktową w układzie współrzędnych PUWG 1992 (EPSG:2180).

> 📌 **Uwaga**: Przekształcenie CRS umożliwia łączenie danych ze statycznymi warstwami przestrzennymi Polski w tym samym układzie.

---

### `get_meteo_metadata(url: str) -> GeoDataFrame`

- **Opis**: Funkcja pobiera metadane dotyczące meteorologicznych stacji pomiarowych ze wskazanego źródła (np. pliku CSV lub adresu URL).
  Na podstawie współrzędnych geograficznych (`lat`, `lon`) buduje przestrzenną reprezentację stacji.

- **Parametry**:
  - `url` (`str`) – ścieżka lokalna lub URL do pliku CSV zawierającego metadane stacji meteorologicznych (w tym kolumny `lat`, `lon`).

- **Zakres działania**:
  - Wczytuje dane do `DataFrame`,
  - Generuje kolumnę `geometry` jako punkty z `lon` i `lat`,
  - Przypisuje CRS jako `EPSG:4326`,
  - Konwertuje dane do `EPSG:2180`.

- **Zwraca**:
  - `GeoDataFrame` z geometrią stacji meteorologicznych w układzie PUWG 1992.

> ✅ Dzięki przestrzennej reprezentacji danych możliwe jest ich bezpośrednie mapowanie i łączenie z danymi środowiskowymi i administracyjnymi.

  
### `get_hydro_data(first: int, last: int) -> DataFrame`

- **Opis**: Funkcja pobiera dobowe dane hydrologiczne ze strony IMGW w formacie ZIP dla wybranego zakresu lat (`first`–`last`).  
  Dane zawierają informacje o poziomie wody, przepływie oraz temperaturze wody w stacjach hydrologicznych w Polsce.

- **Parametry**:
  - `first` (`int`) – rok początkowy (np. 2018),
  - `last` (`int`) – rok końcowy (np. 2022).

- **Zakres działania**:
  - Pobierane są dane z katalogu `dane_hydrologiczne/dobowe/` IMGW.
  - Dla lat wcześniejszych niż 2023 dane są rozdzielone na miesiące (`codz_YYYY_MM.zip`), natomiast dla roku 2023 są zebrane w jednym pliku (`codz_2023.zip`).
  - Obsługiwane są dwa formaty separatorów danych: `,` oraz `;`, w zależności od roku.

- **Zwraca**:
  - `DataFrame` z połączonymi danymi z całego zakresu lat. Kolumny:
    - `Station Code` – kod stacji,
    - `Station Name` – nazwa stacji,
    - `Name` – nazwa cieku wodnego,
    - `Hydro Year` – rok hydrologiczny,
    - `Hydro Month` – miesiąc hydrologiczny,
    - `Day` – dzień,
    - `Water Level` – poziom wody [cm],
    - `Flow` – przepływ [m³/s],
    - `Water Temp` – temperatura wody [°C],
    - `Calendar Month` – miesiąc kalendarzowy.

- **Obsługa błędów**:
  - Jeżeli nie uda się pobrać pliku ZIP, funkcja wyświetla komunikat, ale nie przerywa działania.

---

> 📌 **Uwaga**: Konwersja do EPSG:2180 umożliwia bezpośrednie połączenie i wizualizację danych ze statycznymi warstwami granic administracyjnych Polski, które również są w tym układzie współrzędnych.
