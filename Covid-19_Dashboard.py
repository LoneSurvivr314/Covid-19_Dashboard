#import libraries
import COVID19Py
import json
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.tile_providers import CARTODBPOSITRON_RETINA, WIKIMEDIA, STAMEN_TERRAIN_RETINA, get_provider
import pandas as pd
import numpy as np
import random as rand

#New Computer
    #cd C:\\Users\\BUILD-01\\Desktop\\coronavirus-tracker-api-master & pipenv run dev
#Old Computer
    #cd C:\\Users\Old_02\coronavirus-tracker-api & pipenv run dev

#Returns a dict {Dates: List of bokeh-format dates, Confirmed: timeline of cases, Deaths: timeline of deaths}
def timeline(country):
    location_data = covid19.getLocationByCountryCode(str(country), timelines=True)
    return({
        'Dates': pd.to_datetime(list(location_data[0]['timelines']['confirmed']['timeline'].keys())),
        'Confirmed': list(location_data[0]['timelines']['confirmed']['timeline'].values()),
        'Deaths': list(location_data[0]['timelines']['deaths']['timeline'].values()),
        })

#Returns a dict{Deaths: list of deaths, Confirmed: list of cases, Latitude: list of latitudes, Longitude: list of longitudes}
#Data should be from covid19.getLocations()
def world_data(data):
    #Sets up lists
    death_list = [] 
    case_list = []
    lat_list = []
    long_list = []
    population_list = []
    country_list = []
    province_list = []
    update_list = []

    for country in data:
        if country['country_code'] != 'US':
            #Adds deaths and cases
            death_list.append(country['latest']['deaths'])
            case_list.append(country['latest']['confirmed'])

            #Converts lat and long to web mercator coordinates
            if country['coordinates']['longitude'] != '' and country['coordinates']['latitude'] != '':
                long_list.append(float(country['coordinates']['longitude']) * (6378137 * np.pi/180.0))
                lat_list.append(np.log(np.tan((90 + float(country['coordinates']['latitude'])) * np.pi/360.0)) * 6378137)
            else:
                long_list.append(float(0))
                lat_list.append(float(0))

            #Adds Country + Province name and population
            population_list.append(country['country_population'])
            country_list.append(country['country'])
            if country['province'] == '':
                province_list.append('N/A')
            else:
                province_list.append(country['province'])

            #Adds last updated date
            update_list.append(pd.to_datetime(country['last_updated']))

    return({
        'Deaths': death_list,
        'Confirmed': case_list,
        'Latitude': lat_list,
        'Longitude': long_list,
        'Population': population_list,
        'Country': country_list,
        'Province': province_list,
        'Last_Updated': update_list,
        'Death_Size': list(map(lambda x: np.log(x+1) * 2, death_list)),
        'Case_Size': list(map(lambda x: np.log(x+1) * 2, case_list))
        })
    
#Sets up plot
#output_file('covid_map.html')

#Setps up geo data
geo_data = get_provider(CARTODBPOSITRON_RETINA)
m = figure(x_axis_type = 'mercator', y_axis_type = 'mercator', x_range=(-2000000, 6000000), y_range=(-1000000, 7000000))
m.add_tile(geo_data)

#sets up covid19 data to display on map, not US
covid19 = COVID19Py.COVID19('http://127.0.0.1:8000', data_source='jhu')

raw_data = covid19.getLocations()

with open(r'C:\Users\BUILD-01\Desktop\covidfile.txt', 'w') as file:
    file.write(str(raw_data))

covid_data = world_data(raw_data)

#Sets up ColumnDataSource for Bokeh
bokeh_covid_data = ColumnDataSource(data = covid_data)

#Plots data on the map
m.circle(name = 'Cases', x = 'Longitude', y = 'Latitude', size = 'Case_Size', fill_color = (255, 125, 0, 1), line_color = (0, 0, 0, 0), source = bokeh_covid_data)
m.circle(name = 'Deaths', x = 'Longitude', y = 'Latitude', size = 'Death_Size', fill_color = (255, 0, 0, .7), source = bokeh_covid_data)

m.add_tools(HoverTool(
    tooltips = 
    [
    ('Cases', '@Confirmed{0,0}'),
    ('Deaths', '@Deaths{0,0}'),
    ('Country', '@Country'),
    ('Province', '@Province'),
    ('Country Population', '@Population{0,0}'),
    ('Last Updated', '@Last_Updated{%B %d, %Y}')
    ],
    #Format 'Dates' column as a date
    formatters = 
    {
        '@Last_Updated': 'datetime'
    },
    names = 
    [
        'Cases'
    ]
))

show(m)