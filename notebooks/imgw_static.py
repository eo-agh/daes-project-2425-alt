def get_map_wojewodztwa():
    return gpd.read_file("../static_data/wojewodztwa")

def get_map_rzeki():
    return gpd.read_file("../static_data/Rzeki").to_crs("EPSG:2180")
