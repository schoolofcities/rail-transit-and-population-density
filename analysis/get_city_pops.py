import numpy as np
import pandas as pd
import geopandas as gpd


def get_city_pops(N=300):
    """ Save a GeoJSON of the top N cities, ranked by population. Include the 
    geometric points for those cities.  
    """
    cities_gdf = gpd.read_file('./data/ne_10m_populated_places/ne_10m_populated_places.shp')
    cities_gdf = cities_gdf[['NAME', 'POP_MAX', 'geometry']].sort_values(by='POP_MAX', ascending=False).head(300)
    print(cities_gdf)

    # https://geopandas.org/en/stable/docs/user_guide/io.html#writing-spatial-data
    cities_gdf.to_file("./data/cities.gpkg", driver="GPKG")

if __name__ == "__main__":
    get_city_pops()
