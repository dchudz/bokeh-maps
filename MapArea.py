import numpy as np
from PIL import Image
from bokeh.plotting import *


class BoundingBox:
    def __init__(self, min_lon, max_lon, min_lat, max_lat):
        self.min_lon = min_lon
        self.min_lat = min_lat
        self.max_lon = max_lon
        self.max_lat = max_lat
        self.range_lon = max_lon - min_lon
        self.range_lat = max_lat - min_lat


class MapArea:
    def __init__(self, image, bbox):
        self.image = image
        self.bbox = bbox


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
    p.image_rgba(image=[rotated_2d], x=[maparea.bbox.min_lon], y=[maparea.bbox.min_lat], dw=[maparea.bbox.range_lon], dh=[maparea.bbox.range_lat])


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
    output_file("image_example.html")
    bbox = BoundingBox(10,20,30,40) # this is the wrong bounding box for this tile
    img = Image.open("images/tile.png").convert('RGBA')
    maparea = MapArea(img, bbox)
    p = figure()
    add_maparea_to_plot(p, maparea)
    show(p)
