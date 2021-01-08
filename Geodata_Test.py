#import libraries
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, GeoJSONDataSource, HoverTool
from bokeh.tile_providers import CARTODBPOSITRON_RETINA, WIKIMEDIA, STAMEN_TERRAIN_RETINA, get_provider
import pandas as pd
import numpy as np
import random as rand
import geopandas as gpd

shapefile = gpd.read_file(r'C:\Users\BUILD-01\Documents\GitHub\Covid-19_Dashboard\World_Countries__Generalized_-shp\World_Countries__Generalized_.shp')
print(type(shapefile['geometry'][1])