import numpy as np
import requests
from PIL import Image
from bokeh.plotting import *

class MapArea:
    def __init__(self, image, min_lon, max_lon, min_lat, max_lat):
        self.image = image
        self.min_lon = min_lon
        self.min_lat = min_lat
        self.max_lon = max_lon
        self.max_lat = max_lat
        self.range_lon = max_lon - min_lon
        self.range_lat = max_lat - min_lat


def rgba_to_array2d(image):
    arr = np.array(image)
    image_2d = np.empty(arr.shape[0:2], dtype=np.uint32)
    view = image_2d.view(dtype=np.uint8).reshape(arr.shape)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            for k in range(arr.shape[2]):
                view[i, j, k] = arr[i,j,k]
    return image_2d


def add_maparea_to_plot(p, maparea):
    image_array = rgba_to_array2d(maparea.image)
    rotated_2d = np.rot90(np.transpose(image_array))
    p.image_rgba(image=[rotated_2d], x=[maparea.min_lon], y=[maparea.min_lat], dw=[maparea.range_lon], dh=[maparea.range_lat])


class MapTile(MapArea):
    def __init__(self, image, x, y, zoom):
        self.image = image
        self.x = x
        self.y = y
        self.zoom = zoom
        self.min_lon, self.max_lat = tileaddress_to_lonlat(x, y, zoom)
        self.max_lon, self.min_lat = tileaddress_to_lonlat(x+1, y+1, zoom)
        self.range_lon = self.max_lon - self.min_lon
        self.range_lat = self.max_lat - self.min_lat



def get_maptile(x, y, zoom, file_extension, url_format = "http://tile.stamen.com/toner/{0}/{1}/{2}.{3}"):
    url = url_format.format(zoom, x, y, file_extension)
    print(url)
    response = requests.get(url)
    with io.BytesIO(response.content) as response_io:
        image = Image.open(response_io)
        pixels = image.load()
    image.save("tmp.jpg")
    return MapTile(image, x, y, zoom)


def get_google_maptile(x, y, zoom):
    return get_maptile(x, y, zoom, "", url_format="http://mt0.google.com/vt/lyrs=m@169000000&hl=en&x={1}&y={2}&z={0}&s=Ga")


def tileaddress_to_lonlat(tileaddress_x, tileaddress_y, zoom):
    n = 2**zoom
    lon = tileaddress_x / n * 360.0 - 180.0
    lat = (180/np.pi) * np.arcsin(np.tanh(np.pi * (1 - 2 * tileaddress_y / n)))
    # TODO: shift so that pi/2 < lat <= pi/2
    print(lon,lat)
    return lon, lat


# img = Image.open("images/tile.png").convert('RGBA')
# print(type(img))
#
# img_bw = img.convert('L')
#
# print(type(img_bw))
#
# arr = np.array(img)
#
# im2 = Image.fromarray(arr, "RGBA")
# print(im2)

if __name__=='__main__':
    output_file("png_to_bokeh_image.html")
    maparea = get_maptile(7700, 13550, 15, "png")
    print(maparea.range_lon, maparea.range_lat)
    p = figure(tools = "pan, box_zoom, reset, wheel_zoom", width=500, height=500,
               x_range=[maparea.min_lon, maparea.max_lon],
               y_range = [maparea.min_lat,maparea.max_lat])
    add_maparea_to_plot(p, maparea)
    show(p)


    #
    #

    # print(tileaddress_to_lonlat(7700, 13550, 15))