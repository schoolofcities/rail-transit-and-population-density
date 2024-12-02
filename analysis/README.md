## Re-running the analysis, a how-to!

OSM data is updated regularly by users, so we want to make sure that we include updated data, especially for cities which are lacking in data. 

You can do this in a few simple steps. 

### Setup

Ensure that you have the following data downloaded and named appropriately. All data should be under the folder `./data`, stored under the root directory. 
* `./data/ne_10m_populated_places/`: [Natural Earth](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/)
* `./data/ppp_2020_1km_Aggregated.tif`: [WorldPop](https://hub.worldpop.org/geodata/summary?id=24777)
* `./data/src_water/v107/`: [World Water Bodies](https://www.arcgis.com/home/item.html?id=e750071279bf450cbd510454a80f2e63)
* `./data/src_water/water_simp.gpkg`: Apply the Douglas-Peucker simplification algorithm in QGIS to the World Water Bodies layer (or something else that reduces file size)

Create these directories as well, if they don't exist already, which are used for storing intermediate stages of data. Inside `./data/`, you can run: `mkdir city_pop_tiles city_water osm_data`

### Analysis

Next, run these programs.
1. `get_city_list.py`: Selects our subset of cities and relevant fields as `city_list.gpkg` (<1m).
2. `query_osm.py`: Obtains rail and station data in GeoJSON format (~30m).
3. `get_city_water_poly.py`: Creates GPKG files containing the water layer relevant to each city (~5m).
4. `get_city_metrics.py`: Computes the metrics for all cities as `city_metrics.gpkg` and `city_metrics.json` (~5h). This can be done in 2 parts if needed:
    1. Comment out `compute_metrics`, run once (~2.5h).
    2. Comment in `compute_metrics`, comment out `get_city_pop_tiles`, run again (~2.5h). 
5. `render_maps.ipynb`: Compiles layers and generates graphs for each city (~30m).
