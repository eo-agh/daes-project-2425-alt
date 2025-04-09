import pandas as pd
import geopandas as gpd
import requests
import io
import zipfile
import chardet
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
    gdf.columns = ["Station Code","Station Name","Lon","Lat","geometry"] 
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



def get_hydro_data(first, last):
    
    hydro_data = pd.DataFrame()
    for i in range(first,last+1):
        for j in range(1,13):
            if i != 2023:
                sep = ","
                if j < 10:
                    url = f"https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_hydrologiczne/dobowe/{i}/codz_{i}_0{j}.zip" 
                else:
                    url = f"https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_hydrologiczne/dobowe/{i}/codz_{i}_{j}.zip" 
            else:
                url = f"https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_hydrologiczne/dobowe/{i}/codz_{i}.zip" 
                sep = ";"
            
            response = requests.get(url)
            if response.status_code == 200:
                zip_file = zipfile.ZipFile(io.BytesIO(response.content))  
            
                with zip_file.open(zip_file.namelist()[0]) as file:
                    content = file.read() 
                    encoding = chardet.detect(content)["encoding"]
                    raw_data = content.decode(encoding, errors="replace")  
                    data = io.StringIO(raw_data)
                    data_month = pd.read_csv(data, header=None, encoding=encoding, sep=sep, lineterminator="\n")
                    hydro_data = pd.concat([hydro_data, data_month])
                if i == 2023:
                    break
            else:
                print(f"Nie udało się pobrać pliku ZIP.") 
    
    hydro_data.columns = ['Station Code','Station Name','Name','Hydro Year','Hydro Month','Day','Water Level','Flow','Water Temp','Calendar Month']
    return hydro_data