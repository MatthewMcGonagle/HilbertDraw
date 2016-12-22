import HilbertDraw as hd
import matplotlib.pyplot as plt
import pylab
import numpy as np
import scipy
import random 
from PIL import Image
import PIL.ImageOps

initsymmetry = hd.SquareSymmetry(0,0)
initlevel = 0
numlevels = 7
treewidth = 2**numlevels

circles = []
for i in range(15):
	radius = random.random()*treewidth/3
	xcenter = random.random()*treewidth
	ycenter = random.random()*treewidth
	weight = numlevels - 3 + random.random()*4
	circles.append([xcenter, ycenter, radius, weight])

def circlepointmax(pos):
	result = 0
	for i in range(len(circles)):
		thiscircle = circles[i]
		dist = 0
		for j in range(2):
			dist += (pos[j] - thiscircle[j])**2
		dist = np.sqrt(dist)
		if dist < thiscircle[2] and thiscircle[3]>result:
			result = thiscircle[3]
	return result

def circlemax(pos, width, height):
	ncheck = 4
	result = 0
	for i in range(ncheck):
		for j in range(ncheck):
			checkx = pos[0] + i*width/ncheck
			checky = pos[1] + j*width/ncheck
			checkpos = [checkx, checky]
			weight = circlepointmax(checkpos) 
			if weight > result:
				result = weight 
	return result

def maxfunc(pos, width, height):
	return (numlevels+1)*(pos[0]/treewidth/2+pos[1]/treewidth/2)

####################################################

myimage = Image.open('name.png').convert('LA')
flatlist = list(myimage.getdata())
(imwidth, imheight) = myimage.size
def invertcolor(ba):
	if ba[1] == 0:
		return 0 
	else:
		return 255 - ba[0]

bwvalues = [[invertcolor(flatlist[imwidth*i + j]) for j in range(imwidth)] for i in range(imheight)]
plt.imshow(bwvalues, cmap = plt.cm.gray)
plt.show()

treewidth = imwidth
treeheight = imheight

def picmax(pos, width, height):
	ncheck = 1
	result = 0
	nvalues = 0
	x0 = int(pos[0])
	x1 = min(x0 + width, imwidth)
	x1 = int(x1)
	y0 = int(pos[1])
	y1 = min(y0 + height, imheight)
	y1 = int(y1)
	for i in range(x0, x1, ncheck):
		for j in range(y0, y1, ncheck):
			result += bwvalues[j][i]
			nvalues += 1
	if nvalues > 0:
		result /= nvalues
	else:
		result = 0
	result /= 255
	offset = 2
	result = offset + result* (numlevels - offset+1)
	return result

squarelevels = numlevels
squaretree = hd.HilbertTree(initsymmetry, 0) 
squaretree.generatechildren(numlevels)
positions = []
squaretree.generatepositionswithmax(positions, [0,0], treewidth, treeheight, picmax)

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


plt.savefig("Output.png", bbox_inches = "tight", dpi = 100)
plt.show()

