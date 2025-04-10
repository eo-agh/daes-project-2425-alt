import pandas as pd
import numpy as np
import geopandas as gpd
import requests
import io
import zipfile
import chardet
from shapely.geometry import Point
from bs4 import BeautifulSoup


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
    """
    Wczytuje dane hydrologiczne ze wskazanego zakresu dat z adresu URL (API IMGW)
    i zwraca je jako DataFrame.
    """
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


def get_meteo_data(first, last):
    """
    Wczytuje dane meteorologiczne ze wskazanego zakresu dat z adresu URL (API IMGW)
    i zwraca je jako DataFrame.
    """
    meteo_data = pd.DataFrame()
    for i in range(first,last+1):
        url = f"https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/synop/{i}/"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            href_links = [link.get('href') for link in links if link.get('href') is not None and link.get('href')[0:4] == str(i)]
        else: print(f"Strona meteo nie odpowiada.")


        for link in href_links:
            response = requests.get(url + link)
            if response.status_code == 200:
                zip_file = zipfile.ZipFile(io.BytesIO(response.content))  
                for name in zip_file.namelist():
                    if "s_d_t" not in name:
                        with zip_file.open(name) as file:
                            content = file.read()
                            if chardet.detect(content)["encoding"] != None:
                                encoding = chardet.detect(content)["encoding"]
                            else: ecoding = 'uknown-8bit'
                            raw_data = content.decode(encoding, errors="replace")
                            data = io.StringIO(raw_data)
                            data_station = pd.read_csv(data, header=None, encoding=encoding, sep=',', lineterminator="\n")
                            meteo_data = pd.concat([meteo_data, data_station])
            else:
                print(f"Nie udało się pobrać pliku ZIP.") 

    meteo_data = meteo_data.map(lambda x: str(x).replace('\r', '').replace('\n', '').strip() if isinstance(x, str) else x)
    meteo_data.replace(['', 'nan', 'NaN', 'None', '-', 'null'], np.nan, inplace=True)
    
    meteo_data.columns = [
    'Station Code',
    'Station Name',
    'Year',
    'Month',
    'Day',
    'Max Daily Temp',
    'TMAX Status',
    'Min Daily Temp',
    'TMIN Status',
    'Avg Daily Temp',
    'Avg Daily Temp Status',
    'Min Ground Temp',
    'Min Ground Temp Status',
    'Daily Precip Sum',
    'Daily Precip Sum Status',
    'Type of Precip',
    'Snow Cover Height',
    'Snow Cover Height Status',
    'Snow Water Equivalent',
    'Snow Water Equivalent Status',
    'Sunshine Duration',
    'Sunshine Duration Status',
    'Rain Duration',
    'Rain Status',
    'Snowfall Duration',
    'Snowfall Status',
    'Duration of Rain and Snowfall',
    'Rain and Snowfall Status',
    'Hail Duration',
    'Hail Status',
    'Fog Duration',
    'Fog Status',
    'Haze Duration',
    'Haze Status',
    'Soot Duration',
    'Soot Status',
    'Glaze Duration',
    'Glaze Status',
    'Duration of Low Snowstorm',
    'Low Snowstorm Status',
    'Duration of High Snowstorm',
    'High Snowstorm Status',
    'Duration of Turbidity',
    'Turbidity Status',
    'Duration of Wind >=10m/s',
    'FF10 Status',
    'Duration of Wind >15m/s',
    'FF15 Status',
    'Duration of Thunderstorm',
    'Thunderstorm Status',
    'Duration of Dew',
    'Dew Status',
    'Duration of Frost',
    'Frost Status',
    'Snow Cover Occurrence',
    'Snow Cover Status',
    'Lightning Occurrence',
    'Lightning Status',
    'Ground Condition',
    'Lower Isotherm',
    'Lower Isotherm Status',
    'Upper Isotherm',
    'Upper Isotherm Status',
    'Actinometry',
    'Actinometry Status'
    ]
    meteo_data['Actinometry Status'] = pd.to_numeric(meteo_data['Actinometry Status'], errors='coerce')

    return meteo_data