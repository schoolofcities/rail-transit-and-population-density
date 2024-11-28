import os 
import numpy as np
import pandas as pd
from tqdm import tqdm

import geopandas as gpd
from shapely.geometry import Point

tqdm.pandas()
PROJ_CRS = 3857


def save_city_water_polys(row, gdf_water):
    city_name = row.NAME.lower()
    city_geom = row.geometry
    city_point = Point(city_geom.x, city_geom.y)

    max_dist = 300

    edge_cases = ["montreal", "istanbul", "chicago"]
    if city_name in edge_cases:
        max_dist = 1000

    gdf_water["distance"] = gdf_water["centroid"].distance(city_point) / 1000  # Convert to km
    gdf_water[gdf_water["distance"] <= max_dist].drop(["centroid", "distance"], axis=1).to_file(f'./data/city_water/{city_name}_water.gpkg', driver="GPKG")

def get_city_water_polys():
    """ Save all polygons whose centerpoint is within 300km of the center of 
    a city. They should be individual GPKG files. 
    """
    print("Loading cities...")
    gdf_city_list = gpd.read_file('./data/city_list.gpkg')
    gdf_city_list = gdf_city_list.to_crs(PROJ_CRS)  

    print("Loading water...")
    gdf_water = gpd.read_file('./data/src_water/water_simp.gpkg')
    gdf_water = gdf_water.to_crs(PROJ_CRS)
    gdf_water["centroid"] = gdf_water.centroid

    print("Collecting water within 300km of a city...")
    gdf_city_list.progress_apply(lambda x: save_city_water_polys(x, gdf_water), axis=1)


if __name__ == "__main__":
    get_city_water_polys()
