#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().system('pip install bokeh')
# In[4]:
from bokeh.plotting import figure
from bokeh.io import show, output_notebook
# Create a blank figure with labels
p = figure(plot_width = 600, plot_height = 600, 
           title = 'Example Glyphs',
           x_axis_label = 'X', y_axis_label = 'Y')
# Example data
squares_x = [1, 3, 4, 5, 8]
squares_y = [8, 7, 3, 1, 10]
circles_x = [9, 12, 4, 3, 15]
circles_y = [8, 4, 11, 6, 10]
# Add squares glyph
p.square(squares_x, squares_y, size = 12, color = 'navy', alpha = 0.6)
# Add circle glyph
p.circle(circles_x, circles_y, size = 12, color = 'red')
# Set to output the plot in the notebook
output_notebook()
# Show the plot
show(p)
#p = figure()
#p.cirle(iris.petal_length, iris.sepal_length)
#show(p)