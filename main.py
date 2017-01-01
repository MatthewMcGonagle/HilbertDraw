import HilbertDraw as hd
import matplotlib.pyplot as plt
import pylab
import numpy as np
import scipy
import random 
from PIL import Image
import PIL.ImageOps
import cProfile

initsymmetry = hd.SquareSymmetry(0,0)
initlevel = 0
numlevels = 7
treewidth = 2**numlevels

myimage = Image.open('mario.png').convert('LA')
flatlist = list(myimage.getdata())
(imwidth, imheight) = myimage.size

treewidth = imwidth
treeheight = imheight
bwvalues = [ [hd.ImageProcessing.invertcolor(flatlist[imwidth*i + j]) for j in range(imwidth)] 
		for i in range(imheight)]
hd.ImageProcessing.bwtolevels(bwvalues, 0, numlevels)

#myfilter = hd.UseMax(bwvalues)
#myfilter = hd.CircleFilter(bwvalues, numlevels, treewidth, treeheight)
myfilter = hd.UseMajority(bwvalues, numlevels)

plt.imshow(bwvalues, cmap = plt.cm.gray)
plt.show()

squaretree = hd.HilbertTreeMaxed(initsymmetry, 0, [0,0], treewidth, treeheight, myfilter.filterfunc) 
squaretree.generatechildren(numlevels)

positions = []
squaretree.generatepositions(positions)

xpoints = [positions[i][0] for i in range(len(positions))]
ypoints = [treeheight-positions[i][1] for i in range(len(positions))]

fig = plt.figure(figsize = (2*8.6,2*3.2), dpi = 100, frameon = False)
plt.plot(xpoints, ypoints, color = "blue")

plt.axis([-1, treewidth+1, -1, treeheight+1])
ax = plt.gca()
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)


plt.savefig("Output.png", bbox_inches = "tight", dpi = 300)
plt.show()

