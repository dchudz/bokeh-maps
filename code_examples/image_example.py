# This shows how to generate an "image" in bokeh.
# (Could be used to display map. Could also be used similarly to geom_tile in ggplot2)
import numpy as np
from bokeh.plotting import *

N = 1000
x = np.linspace(0, 10, N)
y = np.linspace(0, 10, N)
xx, yy = np.meshgrid(x, y)
d = np.sin(xx)*np.cos(yy)

output_file("image_example.html")
p = figure(x_range=[0, 10], y_range=[0, 10])
p.image(image=[d], x=[0], y=[0], dw=[10], dh=[10], palette="Spectral11")

show(p)
