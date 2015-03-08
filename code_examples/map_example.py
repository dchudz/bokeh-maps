# This seems really hacky, but I managed to get a png file I downloaded into a Bokeh plot

from bokeh.plotting import *
from PIL import Image
import numpy as np



# Convert a map to an array:
# manipulate the array so the map looks right
# tile image from: https://a.tiles.mapbox.com/v4/examples.map-i86l3621/0/0/0.png?access_token=pk.eyJ1IjoidHJpc3RlbiIsImEiOiJuZ2E5MG5BIn0.39lpfFC5Nxyqck1qbTNquQ
img = Image.open("tile.png").convert('RGBA')

# could use any other image too:
#img = Image.open("/Users/david/Dropbox/Photos/20150301 - Tahoe/anthonys_camera/20150301_142558.jpg").convert('RGBA')

# We'll want an option for black-and-white. One way to achieve this is to convert image to monochrome and then back to RGBA:
img_bw = img.convert('L')
img_bw.save("bw.png")
img_bw_rgba = img_bw.convert("RGBA")

arr = np.array(img_bw_rgba)

print(arr.shape)
print(arr)

image_2d = np.empty(arr.shape[0:2], dtype=np.uint32)
view = image_2d.view(dtype=np.uint8).reshape(arr.shape)
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        for k in range(arr.shape[2]):
            view[i, j, k] = arr[i,j,k]

rotated_2d = np.rot90(np.transpose(image_2d))
output_file("png_to_bokeh_image.html")
p = figure(x_range=[0,10], y_range=[0,10])
p.image_rgba(image=[rotated_2d], x=[0], y=[0], dw=[10], dh=[10])
show(p)