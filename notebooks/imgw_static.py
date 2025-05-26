import pandas as pd
import geopandas as gpd

def get_map_wojewodztwa():
    return gpd.read_file("../static_data/wojewodztwa")

def get_map_rzeki():
    return gpd.read_file("../static_data/Rzeki").to_crs("EPSG:2180")

def get_static_data_hydro():
    return pd.read_parquet("../static_data/hydro_data.parquet.gzip")

def get_map_zlewnie():
    return gpd.read_file('../static_data/zlewnie/zlewnie_1.gpkg')

def get_static_data_meteo():
    return pd.read_parquet("../static_data/meteo_opad_data.parquet.gzip")

