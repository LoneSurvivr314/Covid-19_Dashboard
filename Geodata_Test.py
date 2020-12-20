#import libraries
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, GeoJSONDataSourceHoverTool
from bokeh.tile_providers import CARTODBPOSITRON_RETINA, WIKIMEDIA, STAMEN_TERRAIN_RETINA, get_provider
import pandas as pd
import numpy as np
import random as rand
import geopandas as gpd

m = figure(x_axis_type = 'mercator', y_axis_type = 'mercator', x_range = (-2000000, 6000000), y_range = (-1000000, 7000000), sizing_mode = 'stretch_both')