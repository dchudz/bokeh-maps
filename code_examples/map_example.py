from bokeh.plotting import *
from PIL import Image
import numpy as np
import pandas as pd
import pyproj
from MapArea import rgba_to_array2d, get_stamen_maptile, add_maparea_to_plot

def get_world_capitals():
    world_capitals = pd.read_html("http://www.lab.lmnixon.org/4th/worldcapitals.html", header=0)[0]
    world_capitals = world_capitals.dropna(axis=0)
    return(world_capitals)

def destring_lat_or_lon(input_str):
    abs_val = float(input_str[:-1])
    if input_str[-1] in ["N", "E"]:
        output= abs_val
    elif input_str[-1] in ['S', 'W']:
        output= -1 * abs_val
    return output

def convert_lat_lon_to_x_y(lon, lat):
    #output is currently in meters.  Need to convert it to the right units (adjusted degrees?)
    #tiles.mapbox.com uses EPSG:3857
    web_mercator=pyproj.Proj("+init=EPSG:3857")
    return(web_mercator(lon, lat))


world_capitals = get_world_capitals()
world_capitals['lat_numerical'] = world_capitals.Latitude.apply(lambda x: destring_lat_or_lon(x))
world_capitals['lon_numerical'] = world_capitals.Longitude.apply(lambda x: destring_lat_or_lon((x)))
#convert_lat_lon_to_x_y(list(world_capitals.lon_numerical), list(world_capitals.lat_numerical))
maparea1 = get_stamen_maptile(4, 6, 4, "jpg")
output_file("png_to_bokeh_image.html")

p = figure(tools = "pan, box_zoom, reset, wheel_zoom", width=500, height=500,
               x_range=[maparea1.min_lon, maparea1.max_lon],
               y_range = [maparea1.min_lat,maparea1.max_lat])

add_maparea_to_plot(p, maparea1)
#plot just washington DC (as test)
p.rect([-77], [39], width=1, height=1, fill_color="black", fill_alpha=0.7,
    line_color="black")
#plot all world capitals
#p.rect(world_capitals.lon_numerical, world_capitals.lat_numerical, width=1, height=1, fill_color="black", fill_alpha=0.7,
#    line_color="black")

show(p)
