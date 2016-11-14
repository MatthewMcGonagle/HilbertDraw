import HilbertDraw as hd
import matplotlib.pyplot as plt
import pylab
import numpy as np
import random 

power = 7
coord = [[power+1 for j in range(2**power)] for i in range(2**power)] 

def paintcircle(center, radius, value):
	for i in range(2**power):
		for j in range(2**power):
			distance = (center[0]-i)**2 + (center[1] - j)**2
			distance = np.sqrt(distance)
			if distance < radius:
				coord[i][j] = value
#for i in range(2**power):
#	for j in range(2**power):
#		coord[i][j] = i+j
#		coord[i][j] *= 2**(-power-1)
#		coord[i][j] = 1 - coord[i][j]
#		coord[i][j] *= power
#		coord[i][j] = np.sin(i*2**(-power)*9*np.pi)
#		coord[i][j] *= np.sin(j*2**(-power)*5*np.pi)
#		coord[i][j] += 1
#		coord[i][j] *= 1/2
#		coord[i][j] *= i*(2**(power)-i)*2**(-power+1)*(2**(power)-2**(power-1))**-1
#		coord[i][j] *= power 

paintcircle([0,0], 1.5*2**(power-1), 0)
paintcircle([2**(power-1), 2**(power-1)], 2**(power-2)-1, 2)
paintcircle([2**(power),2**(power)], 2**(power-1), 1)

#for i in range(20):
#	centerx =  int(2**power*random.random())
#	centery = int(2**power*random.random())
#	radius = int(2**(power-2)*random.random())
#	value = 2* random.random() 
#	paintcircle([centerx, centery], radius, value)

squarelevels = 7
def floorfunc(position, logwidth):
	offset = 2**logwidth
	result = position[0]**2 + position[1]**2
	result *= 2**(-2*squarelevels-0) 
	result *= squarelevels
	result -= 1
	return result

def floorfunc2(position, logwidth):
	offset = int(2**logwidth)
	i0 = int(position[0])
	j0 = int(position[1])
	minimum = squarelevels 
	for i in range(i0, i0+offset):
		for j in range(j0, j0+offset):
			if coord[i][j] < minimum:
				minimum = coord[i][j]
	return minimum

initconfig = hd.HilbertConfig(hd.LOWLEFTSTART, hd.COUNTERCLOCKWISE, [0,0], [0,0], squarelevels)
squaretree = hd.HilbertSquare(None, initconfig)
#squaretree.generatechildren(squarelevels)
squaretree.generatewithmin(squarelevels, floorfunc2)
positions = []
#squaretree.getpositionswithmin(positions)
squaretree.getpositions(positions)

level = 1 
logwidth = power-1 
initsymmetry = hd.SquareSymmetry(0,0)
initposition = [0,0]
backwards = 0
squaretree2 = hd.HilbertSquare2(initsymmetry, initposition, logwidth, level, backwards)
squaretree2.generatechildren(level)
positions = []
squaretree2.getpositions(positions)
print("Hilbert Curve generation done")

#squaretree = hd.FourSquares(None, hd.LOWLEFTSTART, hd.COUNTERCLOCKWISE)

#hd.generatesquaretree(squaretree, 4)
#positions = []
#initialpos = [0,0]
#hd.generatepositions(positions, initialpos, squaretree, 4)

xpoints = [positions[i][0] for i in range(len(positions))]
ypoints = [positions[i][1] for i in range(len(positions))]

fig = plt.figure(figsize = (2*8.6,2*3.2), dpi = 100, frameon = False)
plt.plot(xpoints, ypoints, color = "blue")
plt.axis([-1, 2**squarelevels, -1, 2**squarelevels])
ax = plt.gca()
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)


plt.savefig("Output.png", bbox_inches = "tight", dpi = 100)
plt.show()

