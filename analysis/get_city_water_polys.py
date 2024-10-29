import os 
import numpy as np
import pandas as pd
from tqdm import tqdm

import geopandas as gpd
import geopy.distance
from shapely.geometry import Point
from shapely.geometry import Polygon

tqdm.pandas()
PROJ_CRS = 3857


def save_city_water_polys(row, water_gdf):
    city_name = row.NAME.lower()
    city_geom = row.geometry
    city_point = Point(city_geom.x, city_geom.y)

    water_gdf["distance"] = water_gdf["centroid"].distance(city_point) / 1000  # km
    water_gdf[water_gdf["distance"] <= 300].drop(["centroid", "distance"], axis=1).to_file(f'./data/city_water/{city_name}_water.gpkg', driver="GPKG")

def get_city_water_polys():
    """ Save all polygons whose centerpoint is within 300km of the center of 
    a city. They should be individual GPKG files. 
    """
    print("Loading cities...")
    cities_dens_gdf = gpd.read_file('./data/cities_dens.gpkg')
    cities_dens_gdf = cities_dens_gdf.to_crs(PROJ_CRS)  

    print("Loading water...")
    water_gdf = gpd.read_file('./gis/water_simp.gpkg')
    water_gdf = water_gdf.to_crs(PROJ_CRS)
    water_gdf["centroid"] = water_gdf.centroid

    print("Collecting water within 300km of a city...")
    cities_dens_gdf.progress_apply(lambda x: save_city_water_polys(x, water_gdf), axis=1)
    


if __name__ == "__main__":
    get_city_water_polys()
