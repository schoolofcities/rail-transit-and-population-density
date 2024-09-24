import os 

import numpy as np
import pandas as pd
from tqdm import tqdm

import geopandas as gpd
import rasterio as rio
import geopy.distance
from shapely.geometry import Point
from shapely.geometry import Polygon


# === HELPERS ===
def binary_search_lon(src, max_idx, lon_val):
    """ Given the raster mapping (src) and the number of pixels (max_idx),
    return the index which is closest to the target lon_val. 
    """
    # src.xy(i,j) --> (lon,lat), s.t. i --> lat, j --> lon
    low, high, mid = 0, max_idx - 1, 0

    while low <= high:
        mid = (high + low) // 2

        if src.xy(0,mid)[0] < lon_val:
            low = mid + 1
        elif src.xy(0,mid)[0] > lon_val:
            high = mid - 1

    # Return the one of low/high index which reports a closer number
    low_val, high_val = src.xy(0,low)[0], src.xy(0,high)[0]
    if abs(lon_val - low_val) < abs(lon_val - high_val):
        return low
    return high

def binary_search_lat(src, max_idx, lon_val):
    """ Given the raster mapping (src) and the number of pixels (max_idx),
    return the index which is closest to the target lat_val. 
    """
    # src.xy(i,j) --> (lon,lat), s.t. i --> lat, j --> lon
    low, high, mid = 0, max_idx - 1, 0

    while low <= high:
        mid = (high + low) // 2

        if src.xy(mid,0)[1] > lon_val:
            low = mid + 1
        elif src.xy(mid,0)[1] < lon_val:
            high = mid - 1

    # Return the one of low/high index which reports a closer number
    low_val, high_val = src.xy(low,0)[1], src.xy(high,0)[1]
    if abs(lon_val - low_val) < abs(lon_val - high_val):
        return low
    return high

def find_radius_bounds(src, lon_center_idx, lat_center_idx, radius):
    """ Return the indices that are no more than radius km N,S,E,W from the center.
    """
    idxs = {'N': lat_center_idx, 'S': lat_center_idx, 'E': lon_center_idx, 'W': lon_center_idx}
    center_coords = src.xy(lat_center_idx,lon_center_idx)

    # Grow the boundaries until they pass the radius
    while geopy.distance.distance(center_coords[::-1], src.xy(idxs['N'],lon_center_idx)[::-1]).km < radius:
        idxs['N'] -= 1
    while geopy.distance.distance(center_coords[::-1], src.xy(idxs['S'],lon_center_idx)[::-1]).km < radius:
        idxs['S'] += 1
    while geopy.distance.distance(center_coords[::-1], src.xy(lat_center_idx,idxs['W'])[::-1]).km < radius:
        idxs['W'] -= 1
    while geopy.distance.distance(center_coords[::-1], src.xy(lat_center_idx,idxs['E'])[::-1]).km < radius:
        idxs['E'] += 1

    # Compensate for overshooting by 1
    idxs['N'] += 1
    idxs['S'] -= 1
    idxs['W'] += 1
    idxs['E'] -= 1

    return idxs

def collect_idxs_in_radius(src, lon_center_idx, lat_center_idx, bound_idxs, radius):
    """ Given the maximal boundaries, return all the idxs within the rectangle 
    which are no further than the radius. 
    """
    center_coords = src.xy(lat_center_idx,lon_center_idx)

    radius_idxs = []
    for i in range(bound_idxs['N'], bound_idxs['S'] + 1, 1):
        for j in range(bound_idxs['W'], bound_idxs['E'] + 1, 1):
            if geopy.distance.distance(center_coords[::-1], src.xy(i,j)[::-1]).km < radius:
                radius_idxs.append((i,j))  # double check this
    
    return radius_idxs

def get_city_coords_gdf(src, band1, lon_center_idx, lat_center_idx, radius_idxs):
    """
    """
    d = {
        "row_idx": [],
        "col_idx": [],
        "pop_count": [],
        "is_center": [],
        "geometry": [],
    }

    for i,j in radius_idxs:
        cur_coords = src.xy(i,j)
        x, y = cur_coords[0], cur_coords[1]

        d["row_idx"].append(i)
        d["col_idx"].append(j)
        d["pop_count"].append(band1[i,j])
        d["is_center"].append((lat_center_idx == i) and (lon_center_idx == j))
        d["geometry"].append(Point(x, y))
    
    gdf = gpd.GeoDataFrame(d, crs="EPSG:4326")
    gdf = gdf[gdf['pop_count'] > 0]
    gdf = gdf.sort_values(['row_idx', 'col_idx'])
    
    return gdf

# === MAIN ===
def load_raster_file():
    """
    """
    file_name = './data/ppp_2020_1km_Aggregated.tif'
    src = rio.open(file_name)
    width, height = src.width, src.height
    print(f'width (lon_max): {width}, height (lat_max): {height}')

    band1 = src.read(1)

    return src, band1, width, height 

def get_city_pop_tiles(src, band1, lon_max, lat_max, cities_gdf, radius):
    """
    """
    # src.xy(i,j) --> (lon,lat), s.t. i --> lat, j --> lon
    # band1[i,j] --> dens. 

    for index, row in tqdm(cities_gdf.iterrows(), total=cities_gdf.shape[0]):
        city, pop, coords = row['NAME'].lower(), row['POP_MAX'], row['geometry']

        if os.path.exists(f'./data/pop_tiles/{city}_coords.gpkg'):
            continue

        # Identify the pair of indices that has the center point
        # print(lon_max, lat_max)
        # print(coords)

        lon_center_idx = binary_search_lon(src, lon_max, coords.x)
        lat_center_idx = binary_search_lat(src, lat_max, coords.y)

        # print(f'lon idx: {lon_center_idx}')
        # print(f'lat idx: {lat_center_idx}')
        # print(src.xy(lat_center_idx,lon_center_idx))

        # Identify the indices that are +- 50km from the center point
        bound_idxs = find_radius_bounds(src, lon_center_idx, lat_center_idx, radius)
        # print(bound_idxs)

        # Iterate through all indices in that range, record those which are <= 50km 
        radius_idxs = collect_idxs_in_radius(src, lon_center_idx, lat_center_idx, bound_idxs, radius)
        # print(len(radius_idxs))

        # Create a gdf, sort, and save. 
        coords_gdf = get_city_coords_gdf(src, band1, lon_center_idx, lat_center_idx, radius_idxs)
        coords_gdf = coords_gdf.sort_values(['row_idx', 'col_idx'])
        # print(gdf)
        coords_gdf.to_file(f'./data/pop_tiles/{city}_coords.gpkg', driver="GPKG")

def compute_city_density(cities_gdf, pop_floor):
    """ Compute raw density, density with a floor, for each city, and save. 
    """
    # NOTE: The 'geometry' is not the center point here
    cities_gdf[['raw_total_pop', 'floor_total_pop', 'raw_total_area', 'floor_total_area', 'raw_dens', 'floor_dens']] = np.nan

    for i, row_i in tqdm(cities_gdf.iterrows(), total=cities_gdf.shape[0]):
        city = row_i['NAME'].lower()
        coords_gdf = gpd.read_file(f'./data/pop_tiles/{city}_coords.gpkg')

        raw_polys, floor_polys = [], []
        for j, row_j in coords_gdf.iterrows():
            x, y = row_j['geometry'].x, row_j['geometry'].y
            offset = 1 / 240  # 0.004166666666666667
            L = [(x+offset,y+offset), (x-offset,y+offset), (x-offset,y-offset), (x+offset,y-offset), (x+offset,y+offset)]
            poly = Polygon(L)

            if row_j['pop_count'] > pop_floor:
                floor_polys.append(poly)
            raw_polys.append(poly)

        raw_total_pop = coords_gdf['pop_count'].sum()
        floor_total_pop = coords_gdf[coords_gdf['pop_count'] > pop_floor]['pop_count'].sum()

        raw_total_area = gpd.GeoSeries(raw_polys, crs=4326).to_crs(3857).area.sum() / (10 ** 6)
        floor_total_area = gpd.GeoSeries(floor_polys, crs=4326).to_crs(3857).area.sum() / (10 ** 6)

        raw_dens = raw_total_pop / raw_total_area
        floor_dens = floor_total_pop / floor_total_area

        cities_gdf.at[i,'raw_total_pop'] = raw_total_pop
        cities_gdf.at[i,'floor_total_pop'] = floor_total_pop
        cities_gdf.at[i,'raw_total_area'] = raw_total_area
        cities_gdf.at[i,'floor_total_area'] = floor_total_area
        cities_gdf.at[i,'raw_dens'] = raw_dens
        cities_gdf.at[i,'floor_dens'] = floor_dens
    
    cities_gdf.to_file("./data/cities_dens.gpkg", driver="GPKG")

def get_urban_density():
    """ Save the data points of (lat, long, density) for a 50km range for each
    of the cities. Each city should be its own csv. 
    """
    # process_raster_file()

    # Load the raster file and methods for querying
    src, band1, lon_max, lat_max = load_raster_file()

    # Load the set of cities and their key coordinates
    cities_gdf = gpd.read_file('./data/cities.gpkg')

    # Identify the data points of (lat, long, density) for a 50km radius around the city coordinate, and save them 
    get_city_pop_tiles(src, band1, lon_max, lat_max, cities_gdf, 50)

    # Compute the urban density using different metrics for each of these cities 
    compute_city_density(cities_gdf, 100)


if __name__ == "__main__":
    get_urban_density()