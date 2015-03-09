# This seems really hacky, but I managed to get a png file I downloaded into a Bokeh plot

from bokeh.plotting import *
from PIL import Image
import numpy as np
import pandas as pd
import pyproj

def get_world_capitals():
    world_capitals = pd.read_html("http://www.lab.lmnixon.org/4th/worldcapitals.html", header=0)[0]
    world_capitals = world_capitals.dropna(axis=0)
    return(world_capitals)

world_capitals = get_world_capitals()

def destring_lat_or_lon(input_str):
    abs_val = float(input_str[:-1])
    if input_str[-1] in ["N", "E"]:
        output= abs_val
    elif input_str[-1] in ['S', 'W']:
        output= -1 * abs_val
    return output

world_capitals['lat_numerical'] = world_capitals.Latitude.apply(lambda x: destring_lat_or_lon(x))
world_capitals['lon_numerical'] = world_capitals.Longitude.apply(lambda x: destring_lat_or_lon((x)))

def convert_lat_lon_to_x_y(lon, lat):
    #output is currently in meters.  Need to convert it to the right units (adjusted degrees?)
    web_mercator=pyproj.Proj("+init=EPSG:3857")
    return(web_mercator(lon, lat))

convert_lat_lon_to_x_y(list(world_capitals.lon_numerical), list(world_capitals.lat_numerical))



# Convert a map to an array:
# manipulate the array so the map looks right
# tile image from: https://a.tiles.mapbox.com/v4/examples.map-i86l3621/0/0/0.png?access_token=pk.eyJ1IjoidHJpc3RlbiIsImEiOiJuZ2E5MG5BIn0.39lpfFC5Nxyqck1qbTNquQ
# Mapbox uses the Web Mercator projection... commonly referred to as EPSG:900913 or EPSG:3857
img = Image.open("tile.png").convert('RGBA')

arr = np.array(img)
image_2d = np.empty(arr.shape[0:2], dtype=np.uint32)
view = image_2d.view(dtype=np.uint8).reshape(arr.shape)
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        for k in range(arr.shape[2]):
            view[i, j, k] = arr[i,j,k]

rotated_2d = np.rot90(np.transpose(image_2d))
output_file("png_to_bokeh_image.html")
p = figure(x_range=[-180,180], y_range=[-90,90])

p.image_rgba(image=[rotated_2d], x=[-180], y=[-90], dw=[360], dh=[180])

#plot just washington DC (as test)
p.rect([-77], [39], width=1, height=1, fill_color="black", fill_alpha=0.7,
    line_color="black")
#plot all world capitals
#p.rect(world_capitals.lon_numerical, world_capitals.lat_numerical, width=1, height=1, fill_color="black", fill_alpha=0.7,
#    line_color="black")

show(p)