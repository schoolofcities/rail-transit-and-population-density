import numpy as np
import pandas as pd
import geopandas as gpd

# cities, that for now, are outside the top 300 that are worth adding
EXTRA_CITIES = [
    "Almaty",
    "Almaty",
    "Amsterdam",
    "Calgary",
    "Cochabamba",
    "Doha",
    "Dubai",
    "Dushanbe",
    "Edmonton",
    "Jerusalem",
    "Kuala Lumpur",
    "Marseille",
    "Ottawa",
    "Panama City",
    "Porto",
    "San Jose",
    "Stockholm",
    "Tblisi",
]

SUBURBS = [
    "Bekasi",  # Jakarta
    "Baltimore", # Washington (kindof)
    "Benoni",  # Johannesburg
    "Dongguan",  # Guangzhou
    "El Giza",  # Cairo
    "Faridabad", # Delhi
    "Fort Lauderdale",  # Miami
    "Fushun", # Shenyang
    "Ft. Worth", # Dallas
    "Haora",  # Kolkata
    "Incheon",  # Seoul
    "Irvine",  # Los Angeles
    "Jianmen",  # Xiantao
    "Kalyan",  # Mumbai
    "Karaj", # Tehran
    "Kawasaki", # Tokyo
    "Kobe",  # Osaka
    "Kyoto",  # Osaka
    "Long Beach",  # Los Angeles
    "Makkah", # Saudi Arabia
    "Neijiang", # Luzhou
    "New Taipei",  # Taipei
    "Niteroi", # Rio de Janeiro
    "Oakland", # San Francisco
    "Omdurman",  # Khartoum
    "Quezon City",  # Manila
    "Quanzhou", # Xiamen
    "Santos",  # Sao Paolo
    "Suining", # Nanchong
    "Taian",  # Jinan
    "Tainan",  # Kaohsiung
    "Tijuana", # San Diego
    "Wuxi",  # Shanghai
    "Xiangtan",  # Changsha
    "Yokohama",  # Tokyo
    "Zhangzhou",  # Xiamen
    "Zhongli",  # Taipei
]

ERROR_CITIES = [
    "Asuncion", # Paraguay, stations are abandonded
    "Bamako", # Mali, no transit
    "Barranquilla", # Colombia, no transit
    "Beirut",  # Lebanon
    "Belem",  # Brazil
    "Bogota", # Colombia, no transit (is under construction)
    "Campinas", # Brazil
    "Cincinnati", # USA, no transit
    "Curitiba", # Brazil, no transit
    "Davao", # Philippines, no transit
    "Detroit", # USA
    "Douala", # Cameroon, no transit
    "Goiania", # Brazil, no transit
    "Guayaquil", # Ecuador, no transit
    "Haikou",  # China, processing error 
    "Hechi", # China
    "Indianapolis", # USA, no transit
    "Kabul",  # Afghanistan
    "Kano", # Nigeria, no transit
    "Kuwait City", # Kuwait, no transit
    "La Paz", # Bolivia, no transit
    "Las Vegas", # USA, only has mini monorails
    "Leon", # Mexico, no transit
    "Lome", # Togo, no transit
    "Manaus",  # Brazil
    "Mianyang", # China, no transit
    "Phnom Penh", # Cambodia, no transit
    "Port-au-Prince",  # Haiti
    "Puebla", # Mexico, no transit
    "Qiqihar", # China, no transit
    "Saidu", # Pakistan, no transit
    "Sanaa",  # Yemen
    "San Antonio", # USA, no transit
    "San Salvador", # El Salvador, no transit
    "Santa Cruz", #Bolivia, no data
    "Tampa", # USA, no transit
    # "Tashkent",  # Uzbekistan, due to geographic error
    "Tripoli", #Libya, no transit
    "Virginia Beach", # USA
    "Weifang", #China, no transit
    "Xiantao", #China, odd data
    "Xinyang", #China, odd data
]

REGIONS = {
    # East Asia
    'China': 'East Asia',
    'Japan': 'East Asia',
    'Korea, North': 'East Asia',
    'Korea, South': 'East Asia',
    'Taiwan': 'East Asia',
    
    # Europe
    'Austria': 'Europe',
    'Belarus': 'Europe',
    'Belgium': 'Europe',
    'French Republic': 'Europe',
    'Germany': 'Europe',
    'Georgia': 'Europe',
    'Greece': 'Europe',
    'Hungary': 'Europe',
    'Italy': 'Europe',
    'Kingdom of Spain': 'Europe',
    'Kingdom of the Netherlands': 'Europe',
    'Poland': 'Europe',
    'Portugal': 'Europe',
    'Romania': 'Europe',
    'Russia': 'Europe',
    'Sweden': 'Europe',
    'Ukraine': 'Europe',
    'United Kingdom': 'Europe',
    
    # Latin America & Caribbean
    'Argentina': 'Latin America & Caribbean',
    'Bolivia': 'Latin America & Caribbean',
    'Brazil': 'Latin America & Caribbean',
    'Chile': 'Latin America & Caribbean',
    'Colombia': 'Latin America & Caribbean',
    'Costa Rica': 'Latin America & Caribbean',
    'Cuba': 'Latin America & Caribbean',
    'Dominican Republic': 'Latin America & Caribbean',
    'Ecuador': 'Latin America & Caribbean',
    'El Salvador': 'Latin America & Caribbean',
    'Guatemala': 'Latin America & Caribbean',
    'Haiti': 'Latin America & Caribbean',
    'Honduras': 'Latin America & Caribbean',
    'Mexico': 'Latin America & Caribbean',
    'Panama': 'Latin America & Caribbean',
    'Paraguay': 'Latin America & Caribbean',
    'Peru': 'Latin America & Caribbean',
    'Uruguay': 'Latin America & Caribbean',
    'Venezuela': 'Latin America & Caribbean',
    
    # Middle East & North Africa
    'Algeria': 'Middle East & North Africa',
    'Azerbaijan': 'Middle East & North Africa',
    'Egypt': 'Middle East & North Africa',
    'Iran': 'Middle East & North Africa',
    'Iraq': 'Middle East & North Africa',
    'Israel': 'Middle East & North Africa',
    'Kuwait': 'Middle East & North Africa',
    'Lebanon': 'Middle East & North Africa',
    'Libya': 'Middle East & North Africa',
    'Morocco': 'Middle East & North Africa',
    'Qatar': 'Middle East & North Africa',
    'Saudi Arabia': 'Middle East & North Africa',
    'Sudan': 'Middle East & North Africa',
    'Syria': 'Middle East & North Africa',
    'Tunisia': 'Middle East & North Africa',
    'Turkey': 'Middle East & North Africa',
    'United Arab Emirates': 'Middle East & North Africa',
    'Yemen': 'Middle East & North Africa',
    
    # South & Central Asia
    'Afghanistan': 'South & Central Asia',
    'Bangladesh': 'South & Central Asia',
    'India': 'South & Central Asia',
    'Kazakhstan': 'South & Central Asia',
    'Pakistan': 'South & Central Asia',
    'Tajikistan': 'South & Central Asia',
    'Uzbekistan': 'South & Central Asia',
    
    # South East Asia & Oceania
    'Australia': 'South East Asia & Oceania',
    'Cambodia': 'South East Asia & Oceania',
    'Indonesia': 'South East Asia & Oceania',
    'Malaysia': 'South East Asia & Oceania',
    'Myanmar': 'South East Asia & Oceania',
    'Philippines': 'South East Asia & Oceania',
    'Singapore': 'South East Asia & Oceania',
    'Thailand': 'South East Asia & Oceania',
    'Vietnam': 'South East Asia & Oceania',
    
    # Sub Saharan Africa
    'Angola': 'Sub Saharan Africa',
    'Cameroon': 'Sub Saharan Africa',
    'Congo (Kinshasa)': 'Sub Saharan Africa',
    'Ethiopia': 'Sub Saharan Africa',
    'Ghana': 'Sub Saharan Africa',
    'Guinea': 'Sub Saharan Africa',
    'Ivory Coast': 'Sub Saharan Africa',
    'Kenya': 'Sub Saharan Africa',
    'Madagascar': 'Sub Saharan Africa',
    'Mali': 'Sub Saharan Africa',
    'Mozambique': 'Sub Saharan Africa',
    'Nigeria': 'Sub Saharan Africa',
    'Senegal': 'Sub Saharan Africa',
    'South Africa': 'Sub Saharan Africa',
    'Togo': 'Sub Saharan Africa',
    'Uganda': 'Sub Saharan Africa',
    'United Republic of Tanzania': 'Sub Saharan Africa',
    'Zimbabwe': 'Sub Saharan Africa',
    
    # US & Canada
    'Canada': 'US & Canada',
    'United States': 'US & Canada',
}


def get_city_list(N=350):
    """ Save a GPKG of the top N cities, ranked by the population. Include the
    geometric points for those cities and other relevant information (country,
    country code, region, etc).
    """
    gdf_places = gpd.read_file('./data/ne_10m_populated_places/ne_10m_populated_places.shp')
    gdf_places = gdf_places.sort_values(by='POP_MAX', ascending=False)

    # Select relevant subset of data
    gdf_places = gdf_places[['NAMEASCII', 'SOV0NAME', 'SOV_A3', 'POP_MAX', 'geometry']]
    gdf_places = gdf_places.rename(columns={'NAMEASCII': 'NAME'})

    # Parse out extra cities
    gdf_places_extra = gdf_places[gdf_places['NAME'].isin(EXTRA_CITIES)]

    # Get top N cities
    gdf_places = gdf_places.head(N)

    gdf_places = pd.concat([gdf_places, gdf_places_extra], ignore_index=True)

    # Remove duplicates, suburbs, and cities without transit, or other issues
    gdf_places = gdf_places.drop_duplicates(subset='NAME').reset_index(drop=True)
    gdf_places = gdf_places[~gdf_places['NAME'].isin(SUBURBS)].reset_index(drop=True)
    gdf_places = gdf_places[~gdf_places['NAME'].isin(ERROR_CITIES)].reset_index(drop=True)

    # Add regional classifier
    gdf_places['REGION'] = gdf_places['SOV0NAME'].apply(lambda x: REGIONS[x])

    # Fix coordinates
    gdf_places.loc[gdf_places['NAME'] == 'Suzhou', 'geometry'] = gpd.points_from_xy([120.649], [31.406])[0]

    # Fix columns and save
    gdf_places = gdf_places.rename(columns={'SOV0NAME': 'COUNTRY', 'SOV_A3': 'COUNTRY_CODE', 'POP_MAX': 'SRC_POP'})

    cols = gdf_places.columns.to_list()
    cols = cols[:-2] + [cols[-1]] + [cols[-2]]
    gdf_places = gdf_places[cols]
    gdf_places.to_file("./data/city_list.gpkg", driver="GPKG")


if __name__ == "__main__":
    get_city_list()