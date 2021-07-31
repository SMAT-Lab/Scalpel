#!/usr/bin/env python
# coding: utf-8
# In[3]:
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
# This is a bit of magic to make matplotlib figures appear inline in the notebook
# rather than in a new window.
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
# Some more magic so that the notebook will reload external python modules;
# see http://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
# In[25]:
# Read in the image and print out some stats
image = mpimg.imread('test.jpg')
print('This image is: ',type(image), 
         'with dimensions:', image.shape)
# Grab the x and y size and make a copy of the image
ysize = image.shape[0]
xsize = image.shape[1]
# Note: always make a copy rather than simply using "="
color_select = np.copy(image)
# Define our color selection criteria
# Note: if you run this code, you'll find these are not sensible values!!
# But you'll get a chance to play with them soon in a quiz
red_threshold = 200
green_threshold = 200
blue_threshold = 200
rgb_threshold = [red_threshold, green_threshold, blue_threshold]
# Identify pixels below the threshold
thresholds = (image[:,:,0] < rgb_threshold[0])             | (image[:,:,1] < rgb_threshold[1])             | (image[:,:,2] < rgb_threshold[2])
color_select[thresholds] = [0,0,0]
# Display the R, G, and B channels of the image separately
plt.subplot(1,3,1)
plt.title("Red")
plt.imshow(color_select[:,:,0])
plt.subplot(1,3,2)
plt.title("Green")
plt.imshow(color_select[:,:,1])
plt.subplot(1,3,3)
plt.title("Blue")
plt.imshow(color_select[:,:,2])
plt.show()
# In[46]:
# Read in the image
image = mpimg.imread('test.jpg')
# Grab the x and y sizes and make two copies of the image
# With one copy we'll extract only the pixels that meet our selection,
# then we'll paint those pixels red in the original image to see our selection 
# overlaid on the original.
ysize = image.shape[0]
xsize = image.shape[1]
color_select= np.copy(image)
line_image = np.copy(image)
# Define our color criteria
red_threshold = 200
green_threshold = 200
blue_threshold = 200
rgb_threshold = [red_threshold, green_threshold, blue_threshold]
# Define a triangle region of interest (Note: if you run this code, 
# Keep in mind the origin (x=0, y=0) is in the upper left in image processing
# you'll find these are not sensible values!!
# But you'll get a chance to play with them soon in a quiz ;)
# Based on the shape of the image, just move the left and right bottoms to the bottom coordinates
left_bottom = [0, 539]
right_bottom = [960, 539] 
apex = [480, 320] # Place this at the point under the green highway sign
# np.polyfit(x coordinates, y coordinates, degree of polyfit=1, aka linear)
fit_left = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), 1)
fit_right = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)
# Mask pixels below the threshold
color_thresholds = (image[:,:,0] < rgb_threshold[0]) |                     (image[:,:,1] < rgb_threshold[1]) |                     (image[:,:,2] < rgb_threshold[2])
# Find the region inside the lines
# Produce a "meshgrid" of the image. Print out the meshgrid if you don't understand what this is.
XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
region_thresholds = (YY > (XX*fit_left[0] + fit_left[1])) &                     (YY > (XX*fit_right[0] + fit_right[1])) &                     (YY < (XX*fit_bottom[0] + fit_bottom[1]))
# Mask color selection
color_select[color_thresholds] = [0,0,0]
# Find where image is both colored right and in the region, and color it completely red
line_image[~color_thresholds & region_thresholds] = [255,0,0]
# Display our two output images
plt.subplot(2,1,1)
plt.imshow(color_select)
plt.subplot(2,1,2)
plt.imshow(line_image)