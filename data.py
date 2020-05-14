import pandas as pd
import numpy as np
import json

def  list_to_options(series):
    options = [{'value': index, 'label':value} for index, value in series.items()]
    return options 

df_mobility = pd.read_csv('https://github.com/ActiveConclusion/COVID19_mobility/raw/master/google_reports/Global_Mobility_Report.csv', low_memory=False)
iso3 = pd.read_json('iso3.json', typ='series')
df_mobility.country_region_code = df_mobility.country_region_code.map(iso3) #ISO2 -> ISO3


df_cases_country = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv").set_index('ISO3', drop=False)
df_cases_country = df_cases_country[df_cases_country.index.isin(df_mobility.country_region_code.dropna().unique())]

df_mobility = df_mobility[pd.isna(df_mobility.sub_region_1)].set_index('country_region_code', drop=False)

country_list = list_to_options(df_cases_country.Country_Region)

# GeoJSON for map
with open('countries.json') as json_file:
    geo = json.load(json_file)

# Dict with forman "AUS": 16 to get country id in geojson file
map_features = {geo["features"][i]["properties"]['ISO_A3']: i for i in range(len(geo["features"]))}
