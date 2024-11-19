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
    # "Kyoto",  # Osaka
    "Yokohama",  # Tokyo
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


def clean_city_data():
    """ Post-process city density data and save updated files
     1. Use the ASCII name
     2. Remove cities which are effectively suburbs of a larger city
     3. Add a regional classifer for the city using SOV0NAME

    TODO: Integrate this as part of the regular scripts, and delete this file.
    """
    # Load data
    gdf_places = gpd.read_file('./data/ne_10m_populated_places/ne_10m_populated_places.shp')
    gdf_places = gdf_places.sort_values(by='POP_MAX', ascending=False)

    gdf_places_ascii = gdf_places.drop_duplicates(subset='NAMEASCII', keep='first', ignore_index=True)
    gdf_places = gdf_places.drop_duplicates(subset='NAME', keep='first', ignore_index=True)
    gdf_cities_dens = gpd.read_file("./data/cities_dens_old.gpkg")

    # ASCII
    gdf_cities_dens['NAME'] = gdf_cities_dens['NAME'].map(gdf_places.set_index('NAME')['NAMEASCII'])

    # Suburbs
    gdf_cities_dens = gdf_cities_dens[~gdf_cities_dens['NAME'].isin(SUBURBS)].reset_index(drop=True)

    # Regional classifier
    gdf_cities_dens['country'] = gdf_cities_dens['NAME'].map(gdf_places_ascii.set_index('NAMEASCII')['SOV0NAME'])
    gdf_cities_dens['region'] = gdf_cities_dens['country'].apply(lambda x: REGIONS[x])

    # Fix columns and save
    gdf_cities_dens = gdf_cities_dens.drop(columns='country')
    cols = gdf_cities_dens.columns.to_list()
    cols = cols[:2] + ['region'] + cols[2:-1]
    gdf_cities_dens = gdf_cities_dens[cols]

    gdf_cities_dens.to_file("./data/cities_dens.gpkg", driver="GPKG")
    gdf_cities_dens = gdf_cities_dens.drop(columns='geometry')
    gdf_cities_dens = gdf_cities_dens.set_index('NAME')
    gdf_cities_dens.to_json('./data/cities_dens.json', orient='index')

if __name__ == "__main__":
    clean_city_data()
