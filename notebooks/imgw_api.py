import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def get_hydro_metadata() -> gpd.GeoDataFrame:
    """
    Wczytuje metadane hydrologiczne ze wskazanego URL (np. API IMGW)
    i zwraca je jako GeoDataFrame w układzie EPSG:2180 (PUWG 1992).
    """
    hydro_url = "http://danepubliczne.imgw.pl/api/data/hydro2/"
    hydro_stat = pd.read_json(hydro_url)
    df = hydro_stat.iloc[:, 0:4]
    
    # Tworzenie geometrii
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs="EPSG:4326"
    )
    
    # Konwersja do układu PL (PUWG 1992)
    gdf = gdf.to_crs("EPSG:2180")
    
    return gdf


def get_meteo_metadata() -> gpd.GeoDataFrame:
    """
    Wczytuje metadane meteorologiczne ze wskazanego URL (np. API IMGW)
    i zwraca je jako GeoDataFrame w układzie EPSG:2180 (PUWG 1992).
    """
    meteo_url = "http://danepubliczne.imgw.pl/api/data/meteo/"
    meteo_stat = pd.read_json(meteo_url)
    df = meteo_stat.iloc[:, 0:4]
    
    # Tworzenie geometrii
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs="EPSG:4326"
    )
    
    # Konwersja do układu PL (PUWG 1992)
    gdf = gdf.to_crs("EPSG:2180")
    
    return gdf
