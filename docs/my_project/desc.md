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

### `get_hydro_metadata() -> GeoDataFrame`

- Opis: Pobiera dane dotyczące hydrologicznych stacji pomiarowych ze wskazanego źródła (np. CSV z API IMGW).
- Tworzy kolumnę `geometry` na podstawie `lat` i `lon`.
- Przypisuje CRS `EPSG:4326` i natychmiast konwertuje do `EPSG:2180` (PUWG 1992).
- Zwraca: `GeoDataFrame` z geometrią punktową w układzie PUWG 1992.

### `get_meteo_metadata() -> GeoDataFrame`

- Opis: Pobiera dane dotyczące meteorologicznych stacji pomiarowych ze wskazanego źródła.
- Tworzy kolumnę `geometry` na podstawie `lat` i `lon`.
- Przypisuje CRS `EPSG:4326` i konwertuje do `EPSG:2180`.
- Zwraca: `GeoDataFrame` z geometrią punktową w układzie PUWG 1992.

---

> 📌 **Uwaga**: Konwersja do EPSG:2180 umożliwia bezpośrednie połączenie i wizualizację danych ze statycznymi warstwami granic administracyjnych Polski, które również są w tym układzie współrzędnych.
