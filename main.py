import HilbertDraw as hd
import matplotlib.pyplot as plt
import pylab
import numpy as np
import scipy
import random 
from PIL import Image
import PIL.ImageOps
import cProfile

# Set up the initial orientation of the root rectangle. This is the orientation that all of the
# the other orientations will be relative to.

initsymmetry = hd.SquareSymmetry(0,0)

# Set up the level of Hilbert pseudo-curve to associate with the root rectangle.
initlevel = 0

# Set up the maximum level of Hilbert pseudo-curve to use.
numlevels = 7

# Open image as black and white image, get the pixel color data, and get image dimensions.
myimage = Image.open('hilbertcartoon.png').convert('LA')
flatlist = list(myimage.getdata())
(imwidth, imheight) = myimage.size

# The output width and height will be the same as the dimensions of the picture. 
treewidth = imwidth
treeheight = imheight

# Resize pixel data and invert the color as we go. We invert because we need larger numbers
# to be associated with darker areas in the image.
# After conversion, then do another conversion to levels data.
bwvalues = [ [hd.ImageProcessing.invertcolor(flatlist[imwidth*i + j]) for j in range(imwidth)] 
		for i in range(imheight)]
hd.ImageProcessing.bwtolevels(bwvalues, 0, numlevels)

# Take a look at the pixel values data.
plt.imshow(bwvalues, cmap = plt.cm.gray)
plt.show()

# Set up the filter to use to determine what maximum level of Hilbert pseudo-curve to associate with
# a given sub-rectangle based on the pixel level data.

#myfilter = hd.UseMax(bwvalues)
#myfilter = hd.CircleFilter(bwvalues, numlevels, treewidth, treeheight)
myfilter = hd.UseMajority(bwvalues, numlevels)

# Using the filter function, set up the root Hilbert Tree node, and then generate the rest of the tree.
squaretree = hd.HilbertTreeMaxed(initsymmetry, 0, [0,0], treewidth, treeheight, myfilter.filterfunc) 
squaretree.generatechildren(numlevels)

# Now extract the positions of the leaf node from the Hilbert tree.
positions = []
squaretree.generatepositions(positions)


# Graph line segments between adjacent leaf node positions in the positions list.
xpoints = [positions[i][0] for i in range(len(positions))]
ypoints = [treeheight-positions[i][1] for i in range(len(positions))]

fig = plt.figure(dpi = 300, frameon = False)
plt.plot(xpoints, ypoints, color = "blue")

# Format the graph for making a nice picture.

plt.axis([-1, treewidth+1, -1, treeheight+1])
ax = plt.gca()
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Save as a picture, and then display the result.
plt.savefig("Output.png", bbox_inches = "tight", dpi = 300)
plt.show()

