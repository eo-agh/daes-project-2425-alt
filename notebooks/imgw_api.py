import pandas as pd

def get_hydro_metadata():
    hydro_url = "http://danepubliczne.imgw.pl/api/data/hydro2/"
    hydro_stat = pd.read_json(hydro_url)
    return hydro_stat.iloc[:, 0:4]

def get_meteo_metadata():
    meteo_url = "http://danepubliczne.imgw.pl/api/data/meteo/"
    meteo_stat = pd.read_json(meteo_url)
    return meteo_stat.iloc[:, 0:4]
