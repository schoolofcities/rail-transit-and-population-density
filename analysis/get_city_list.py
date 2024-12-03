import numpy as np
import pandas as pd
import geopandas as gpd


SUBURBS = [
    "Long Beach",  # Los Angeles
    "Irvine",  # Los Angeles
    "Fort Lauderdale",  # Miami
    "Santos",  # Sao Paolo
    "El Giza",  # Cairo
    "Omdurman",  # Khartoum
    "Benoni",  # Johannesburg
    "Haora",  # Kolkata
    "Kalyan",  # Mumbai
    "Bekasi",  # Jakarta
    "Quezon City",  # Manila
    "Dongguan",  # Guangzhou
    "Zhangzhou",  # Xiamen
    "Wuxi",  # Shanghai
    "Xiangtan",  # Changsha
    "Jianmen",  # Xiantao
    "Taian",  # Jinan
    "New Taipei",  # Taipei
    "Zhongli",  # Taipei
    "Tainan",  # Kaohsiung
    "Incheon",  # Seoul
    "Kobe",  # Osaka
    "Kyoto",  # Osaka
    "Yokohama",  # Tokyo
]

ERROR_CITIES = [
    "Kabul",  # Afghanistan
    "Belem",  # Brazil
    "Sanaa",  # Yemen
    "Port-au-Prince",  # Haiti
    "Beirut",  # Lebanon
    "Manaus",  # Brazil
    "Tashkent",  # Uzbekistan, due to geographic error
    "Haikou",  # China, processing error 
]

REGIONS = {
    'Japan': 'East Asia',
    'United States': 'US & Canada',
    'Mexico': 'Latin America & Caribbean',
    'India': 'South & Central Asia',
    'Brazil': 'Latin America & Caribbean',
    'China': 'East Asia',
    'Bangladesh': 'South & Central Asia',
    'Argentina': 'Latin America & Caribbean',
    'Chile': 'Latin America & Caribbean',
    'Pakistan': 'South & Central Asia',
    'Egypt': 'Middle East & North Africa',
    'Philippines': 'South East Asia & Oceania',
    'Russia': 'Europe',
    'Turkey': 'Middle East & North Africa',
    'French Republic': 'Europe',
    'Korea, South': 'East Asia',
    'Nigeria': 'Sub Saharan Africa',
    'Indonesia': 'South East Asia & Oceania',
    'Iran': 'Middle East & North Africa',
    'Congo (Kinshasa)': 'Sub Saharan Africa',
    'Colombia': 'Latin America & Caribbean',
    'Taiwan': 'East Asia',
    'Thailand': 'South East Asia & Oceania',
    'Peru': 'Latin America & Caribbean',
    'Bolivia': 'Latin America & Caribbean',
    'Kingdom of Spain': 'Europe',
    'Vietnam': 'South East Asia & Oceania',
    'Canada': 'US & Canada',
    'Singapore': 'South East Asia & Oceania',
    'Angola': 'Sub Saharan Africa',
    'Iraq': 'Middle East & North Africa',
    'Venezuela': 'Latin America & Caribbean',
    'Sudan': 'Middle East & North Africa',
    'Saudi Arabia': 'Middle East & North Africa',
    'Romania': 'Europe',
    'Myanmar': 'South East Asia & Oceania',
    'Ivory Coast': 'Sub Saharan Africa',
    'South Africa': 'Sub Saharan Africa',
    'Germany': 'Europe',
    'Algeria': 'Middle East & North Africa',
    'Italy': 'Europe',
    'Korea, North': 'East Asia',
    'Afghanistan': 'South & Central Asia',
    'Morocco': 'Middle East & North Africa',
    'Israel': 'Middle East & North Africa',
    'Ethiopia': 'Sub Saharan Africa',
    'Kenya': 'Sub Saharan Africa',
    'United Republic of Tanzania': 'Sub Saharan Africa',
    'Portugal': 'Europe',
    'Poland': 'Europe',
    'Syria': 'Middle East & North Africa',
    'Ukraine': 'Europe',
    'Senegal': 'Sub Saharan Africa',
    'Ecuador': 'Latin America & Caribbean',
    'United Kingdom': 'Europe',
    'Dominican Republic': 'Latin America & Caribbean',
    'Tunisia': 'Middle East & North Africa',
    'Austria': 'Europe',
    'Greece': 'Europe',
    'Uzbekistan': 'South & Central Asia',
    'Cuba': 'Latin America & Caribbean',
    'Azerbaijan': 'Middle East & North Africa',
    'Ghana': 'Sub Saharan Africa',
    'Kuwait': 'Middle East & North Africa',
    'Yemen': 'Middle East & North Africa',
    'Haiti': 'Latin America & Caribbean',
    'Cameroon': 'Sub Saharan Africa',
    'Paraguay': 'Latin America & Caribbean',
    'Australia': 'South East Asia & Oceania',
    'Lebanon': 'Middle East & North Africa',
    'Libya': 'Middle East & North Africa',
    'Belarus': 'Europe',
    'Belgium': 'Europe',
    'Madagascar': 'Sub Saharan Africa',
    'Hungary': 'Europe',
    'Guatemala': 'Latin America & Caribbean',
    'Honduras': 'Latin America & Caribbean',
    'Zimbabwe': 'Sub Saharan Africa',
    'Uruguay': 'Latin America & Caribbean',
    'Malaysia': 'South East Asia & Oceania',
}


def get_city_list(N=300):
    """ Save a GPKG of the top N cities, ranked by the population. Include the
    geometric points for those cities and other relevant information (country,
    country code, region, etc).
    """
    gdf_places = gpd.read_file('./data/ne_10m_populated_places/ne_10m_populated_places.shp')
    gdf_places = gdf_places.sort_values(by='POP_MAX', ascending=False)

    # Select relevant subset of data
    gdf_places = gdf_places[['NAMEASCII', 'SOV0NAME', 'SOV_A3', 'POP_MAX', 'geometry']]
    gdf_places = gdf_places.rename(columns={'NAMEASCII': 'NAME'})
    gdf_places = gdf_places.head(N)

    # Remove duplicates, suburbs, and cities without transit, or other issues
    gdf_places = gdf_places.drop_duplicates(subset='NAME').reset_index(drop=True)
    gdf_places = gdf_places[~gdf_places['NAME'].isin(SUBURBS)].reset_index(drop=True)
    gdf_places = gdf_places[~gdf_places['NAME'].isin(ERROR_CITIES)].reset_index(drop=True)

    # Add regional classifier
    gdf_places['REGION'] = gdf_places['SOV0NAME'].apply(lambda x: REGIONS[x])

    # Fix columns and save
    gdf_places = gdf_places.rename(columns={'SOV0NAME': 'COUNTRY', 'SOV_A3': 'COUNTRY_CODE', 'POP_MAX': 'SRC_POP'})

    cols = gdf_places.columns.to_list()
    cols = cols[:-2] + [cols[-1]] + [cols[-2]]
    gdf_places = gdf_places[cols]
    gdf_places.to_file("./data/city_list.gpkg", driver="GPKG")


if __name__ == "__main__":
    get_city_list()
