import os
import json

import requests
from osm2geojson import json2geojson
import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import geojson

QUERY_STATION = """[out:json];
nwr[railway=station]["construction:railway"!~"station"](around:50000.00,{lat},{lon});
out center;
"""

QUERY_RAIL = """[out:json];
(
nwr["railway"~"^(rail|subway|light_rail)$"]["service"!~"yard|spur|sliding|siding|crossover"]["usage"!~"industrial"]["railway:traffic_mode"!~"freight"](around:50000.00,{lat},{lon}); 
nwr[passenger=suburban](around:50000.00,{lat},{lon});
nwr[usage=main]["railway"!~"abandoned"]["railway:traffic_mode"!~"freight"](around:50000.00,{lat},{lon});
);
out geom;
"""

# stations need to be run with 'center', rest with 'geom'
QUERY_RAW = """[out:json];
(
nwr[railway=station]["construction:railway"!~"station"](around:50000.00,{lat},{lon}); 
nwr["railway"~"^(rail|subway|light_rail)$"]["service"!~"yard|spur|sliding|siding|crossover"]["usage"!~"industrial"]["railway:traffic_mode"!~"freight"](around:50000.00,{lat},{lon}); 
nwr[passenger=suburban](around:50000.00,{lat},{lon});
nwr[usage=main]["railway"!~"abandoned"]["railway:traffic_mode"!~"freight"](around:50000.00,{lat},{lon});
);
out geom;
"""

OVERPASS_URL = 'https://overpass-api.de/api/interpreter'


def run_query(query, lat, lon):
    """ Query the OpenStreetMap API and return the parsed result in GeoJSON format
    """
    response = requests.get(OVERPASS_URL, params={'data': query.format(lat=lat, lon=lon)})
    result = json2geojson(response.json())
    return result

def query_osm():
    """ Query each of our ciites for relevant data, and save them as GeoJSONs. 
    https://pybit.es/articles/openstreetmaps-overpass-api-and-python/
    """
    gdf_city_list = gpd.read_file('./data/city_list.gpkg')

    for i, row_i in tqdm(gdf_city_list.iterrows(), total=gdf_city_list.shape[0]):
        city = row_i['NAME'].lower()

        out_station_path = f'./data/osm_data/{city}_station_osm.geojson'
        out_rail_path = f'./data/osm_data/{city}_rail_osm.geojson'
        if os.path.exists(out_station_path) and os.path.exists(out_rail_path):
            continue

        lon, lat = row_i['geometry'].x, row_i['geometry'].y
        try:
            res_station = run_query(QUERY_STATION, lat, lon)
            res_rail = run_query(QUERY_RAIL, lat, lon)
        except:
            print(f'{city} failed!')
            continue

        # https://gis.stackexchange.com/a/292255
        # https://gis.stackexchange.com/a/362044
        with open(out_station_path, 'w') as f:
            geojson.dump(res_station, f)
        with open(out_rail_path, 'w') as f:
            geojson.dump(res_rail, f)


if __name__ == "__main__":
    query_osm()