import os 
import numpy as np
import pandas as pd
from tqdm import tqdm
import json

import geopandas as gpd
import rasterio as rio
import geopy.distance
import shapely
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.ops import unary_union

from geog import propagate

URBAN_POP_FLOOR = 100
# tqdm.pandas()
# np.seterr(all='raise')

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

def binary_search_lat(src, max_idx, lat_val):
    """ Given the raster mapping (src) and the number of pixels (max_idx),
    return the index which is closest to the target lat_val. 
    """
    # src.xy(i,j) --> (lon,lat), s.t. i --> lat, j --> lon
    low, high, mid = 0, max_idx - 1, 0

    while low <= high:
        mid = (high + low) // 2
        if src.xy(mid,0)[1] > lat_val:
            low = mid + 1
        elif src.xy(mid,0)[1] < lat_val:
            high = mid - 1

    # Return the one of low/high index which reports a closer number
    low_val, high_val = src.xy(low,0)[1], src.xy(high,0)[1]
    if abs(lat_val - low_val) < abs(lat_val - high_val):
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

def get_area_in_sqkm(polys):
    """ Given a list of polygons, return the area in sqkm.
    """
    return gpd.GeoSeries(polys, crs=4326).to_crs(3857).area.sum() / (10 ** 6)

def get_poly_tile(x, y):
    offset = 1 / 240  # 0.004166666666666667
    L = [(x+offset,y+offset), (x-offset,y+offset), (x-offset,y-offset), (x+offset,y-offset), (x+offset,y+offset)]
    return Polygon(L)

def get_station_density(src, band1, lon_max, lat_max, row):
    """ Return the area and population contained within a 1km radius of an
    inputted transit station. The population is the weighted sum derived from 
    intersections of each tiles with the circle around the station. 
    """
    lon_station = row['geometry'].x
    lat_station = row['geometry'].y

    # 1a. Identify the tile that the station belongs to
    lon_station_idx = binary_search_lon(src, lon_max, lon_station)
    lat_station_idx = binary_search_lat(src, lat_max, lat_station)
    
    # 1b. Obtain the tiles within 3km of the station
    bound_idxs = find_radius_bounds(src, lon_station_idx, lat_station_idx, 3)
    radius_idxs = collect_idxs_in_radius(src, lon_station_idx, lat_station_idx, bound_idxs, 3)   

    # 2a. Create a 1km radius circle Polygon using geog
    p = [lon_station, lat_station]
    n_points = 50
    d = 1000 # meters
    angles = np.linspace(0, 360, n_points)
    poly_station = Polygon(propagate(p, angles, d))
    area_station = get_area_in_sqkm([poly_station])

    # 2b. Intersect it with each tile, and store the percent overlap and population
    tile_info = []  # [(pct_intersect, pop)]
    for i,j in radius_idxs:
        cur_coords = src.xy(i,j)
        x, y = cur_coords[0], cur_coords[1]
        poly_tile = get_poly_tile(x, y)
        pop_tile = band1[i,j]

        prop_intersect = poly_tile.intersection(poly_station).area / poly_tile.area
        if prop_intersect > 0 and pop_tile > 0:
            tile_info.append((prop_intersect, pop_tile))

    # 2c. Compute the population within the circle -- population of tiles weighted by percent intersection
    pop_station = 0
    for prop, pop in tile_info:
        pop_station += pop * prop
    
    # 2d. Compute the density -- population over area
    return pop_station, area_station, pop_station / area_station, poly_station

def get_transit_proportions(row, mpoly_stations):
    """ Given a row containing information about a tile within the 50km radius
    of a city (including coordinates and population), return the proportional
    population and the area overlap for the tile. Compute this only if the tile
    represents an urban area (>100). 
    """
    if row['pop_count'] >= URBAN_POP_FLOOR:
        x, y = row['geometry'].x, row['geometry'].y
        poly_tile = get_poly_tile(x, y)
        poly_tile_subset = poly_tile.intersection(mpoly_stations)

        subset_area = get_area_in_sqkm([poly_tile_subset])
        total_area = get_area_in_sqkm([poly_tile])

        return (row['pop_count'] * (subset_area / total_area)), subset_area
    return 0, 0

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
        lon_center_idx = binary_search_lon(src, lon_max, coords.x)
        lat_center_idx = binary_search_lat(src, lat_max, coords.y)

        # Identify the indices that are +- 50km from the center point
        bound_idxs = find_radius_bounds(src, lon_center_idx, lat_center_idx, radius)

        # Iterate through all indices in that range, record those which are <= 50km 
        radius_idxs = collect_idxs_in_radius(src, lon_center_idx, lat_center_idx, bound_idxs, radius)

        # Create a gdf, sort, and save. 
        coords_gdf = get_city_coords_gdf(src, band1, lon_center_idx, lat_center_idx, radius_idxs)
        coords_gdf = coords_gdf.sort_values(['row_idx', 'col_idx'])
        coords_gdf.to_file(f'./data/pop_tiles/{city}_coords.gpkg', driver="GPKG")

def compute_city_density(src, band1, lon_max, lat_max, cities_gdf):
    """ Compute raw density, density with a floor, for each city, and save. 
    """
    cities_gdf[['raw_total_pop', 'raw_total_area', 'raw_dens', 
                'urban_total_pop', 'urban_total_area', 'urban_dens',
                'station_total_pop', 'station_total_area', 'station_dens',
                'transit_pop_prop', 'transit_area_prop', 'transit_ratio']] = 0.0

    for i, row_i in tqdm(cities_gdf.iterrows(), total=cities_gdf.shape[0]):
        city = row_i['NAME'].lower()
        # if city != 'toronto':
        #     continue

        # 1. Get non-transit density
        # NOTE: Consider refactoring below into a helper function for simplicity
        coords_gdf = gpd.read_file(f'./data/pop_tiles/{city}_coords.gpkg')
        
        raw_polys, urban_polys = [], []
        for j, row_j in coords_gdf.iterrows():
            x, y = row_j['geometry'].x, row_j['geometry'].y
            poly = get_poly_tile(x, y)

            if row_j['pop_count'] >= URBAN_POP_FLOOR:
                urban_polys.append(poly)
            raw_polys.append(poly)

            if row_j['is_center']:
                cities_gdf.at[i,'geometry'] = Point(x, y)

        raw_total_pop = coords_gdf['pop_count'].sum()
        urban_total_pop = coords_gdf[coords_gdf['pop_count'] >= URBAN_POP_FLOOR]['pop_count'].sum()

        raw_total_area = get_area_in_sqkm(raw_polys)
        urban_total_area = get_area_in_sqkm(urban_polys)

        raw_dens = raw_total_pop / raw_total_area
        urban_dens = urban_total_pop / urban_total_area

        cities_gdf.at[i,'raw_total_pop'] = raw_total_pop
        cities_gdf.at[i,'urban_total_pop'] = urban_total_pop
        cities_gdf.at[i,'raw_total_area'] = raw_total_area
        cities_gdf.at[i,'urban_total_area'] = urban_total_area
        cities_gdf.at[i,'raw_dens'] = raw_dens
        cities_gdf.at[i,'urban_dens'] = urban_dens

        # 2. Get transit density
        # TOD: Compute the population density within a 1km radius of a station
        stations_gdf = gpd.read_file(f'./data/osm_data/{city}_station_osm.geojson')
        if not stations_gdf.empty:  # already has 0 values otherwise
            # Iterate through the set of stations for a given city, and compute density using the lat and long
            stations_gdf['stats'] = stations_gdf.apply(lambda x: get_station_density(src, band1, lon_max, lat_max, x), axis=1)
            stations_gdf[['pop', 'area', 'dens', 'poly_station']] = pd.DataFrame(stations_gdf['stats'].tolist(), index=stations_gdf.index)

            # Take the mean density for all stations, which is TOD for a city.
            cities_gdf.at[i,'station_total_pop'] = stations_gdf['pop'].sum()
            cities_gdf.at[i,'station_total_area'] = stations_gdf['area'].sum()
            cities_gdf.at[i,'station_dens'] = stations_gdf['dens'].mean()

        # print(stations_gdf['pop'].sum(), stations_gdf['area'].sum(), stations_gdf['dens'].mean())

        # 3. Get population and area proportions near stations
        if not stations_gdf.empty:
            # Merge the station circles for this city into one big MultiPolygon
            mpoly_stations = unary_union(stations_gdf['poly_station'].to_list())

            coords_gdf['stats'] = coords_gdf.apply(lambda x: get_transit_proportions(x, mpoly_stations), axis=1)
            coords_gdf[['pop', 'area']] = pd.DataFrame(coords_gdf['stats'].tolist(), index=coords_gdf.index)
            
            # Compute their proportions
            transit_pop_pct = (coords_gdf['pop'].sum() / coords_gdf['pop_count'].sum()) * 100
            transit_area_pct = (coords_gdf['area'].sum() / raw_total_area) * 100

            cities_gdf.at[i,'transit_pop_pct'] = transit_pop_pct
            cities_gdf.at[i,'transit_area_pct'] = transit_area_pct
            cities_gdf.at[i,'transit_ratio'] = transit_pop_pct / transit_area_pct

        # print(cities_gdf.loc[[i]])
    
    # print(cities_gdf)

    cities_gdf = cities_gdf.drop_duplicates(subset='NAME').reset_index(drop=True)  
    cities_gdf.to_file("./data/cities_dens.gpkg", driver="GPKG")

    # Save as JSON format as well for web processing
    cities_gdf = cities_gdf.drop(columns='geometry')
    cities_gdf = cities_gdf.set_index('NAME')
    cities_gdf.to_json('./data/cities_dens.json', orient='index')

def get_urban_density():
    """ Save the data points of (lat, long, density) for a 50km range for each
    of the cities. Each city should be its own csv. 
    """
    # Load the raster file and methods for querying
    src, band1, lon_max, lat_max = load_raster_file()

    # Load the set of cities and their key coordinates
    cities_gdf = gpd.read_file('./data/cities.gpkg')

    # Identify the data points of (lat, long, density) for a 50km radius around the city coordinate, and save them 
    # get_city_pop_tiles(src, band1, lon_max, lat_max, cities_gdf, 50)

    # Compute the urban density using different metrics for each of these cities 
    compute_city_density(src, band1, lon_max, lat_max, cities_gdf)


if __name__ == "__main__":
    get_urban_density()