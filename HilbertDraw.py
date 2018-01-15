'''
Module to take a picture and make a representation using Hilbert pseudo-curves.

Author : Matthew McGonagle
'''

import numpy as np
import random

class SquareSymmetry:
    '''
        Class for representing rotations and reflections of sub-squares that are used in the
        iterative process of generating the Hilbert pseudo-curves.
        
        Members
        -------
        self.rotation : Int
            The amount the sub-square is rotated relative to the standard orientation. Is either
            0, 1, 2, or 3 to represent 4 possible rotations of 0, 90, 180, and 270 degrees.
        self.reflection : Int
            Represents whether there is a reflection. Has value 0 for NO reflection and value 1 if there
            is a reflection.
    '''

    # rotation^k * reflection

    def __init__(self, rotation, reflection):
    	self.rotation = rotation % 4
    	self.reflection = reflection % 2

    def times(self, symmetry):
    	newrotation = symmetry.rotation
    	if self.reflection:
    		newrotation = (4 - newrotation) % 4
    	newreflection = (self.reflection + symmetry.reflection) % 2
    	newrotation = (newrotation + self.rotation) % 4
    	return SquareSymmetry(newrotation, newreflection)

    def getreflection(self):
    	return self.reflection

    def action(self, vector):
    	newvector = vector.copy()
    	if self.rotation > 0:
    		for i in range(self.rotation):
    			holder = newvector[0]
    			newvector[0] = -newvector[1]
    			newvector[1] = holder
    	if self.reflection:
    		newvector[0] *= -1
    	return newvector

    def actindex(self, index):
    	newindex = (self.rotation + index) % 4
    	if self.reflection > 0:
    		newindex = (3*(newindex+1)) % 4
    	return newindex

class HilbertTree:

    def __init__(self, symmetry, level):
    	self.symmetry = symmetry
    	self.level = level
    	self.children = []

    def generatechildren(self, numlevels):
    	if self.level > numlevels:
    		return
    	elif self.children:
    		return

    	newlevel = self.level + 1
    	newsymmetry = self.symmetry.times(SquareSymmetry(3,1))
    	self.children.append(HilbertTree(newsymmetry, newlevel))

    	newsymmetry = self.symmetry
    	self.children.append(HilbertTree(newsymmetry, newlevel))
    	self.children.append(HilbertTree(newsymmetry, newlevel))

    	newsymmetry = self.symmetry.times(SquareSymmetry(1,1))
    	self.children.append(HilbertTree(newsymmetry, newlevel))

    	for i in range(4):
    		self.children[i].generatechildren(numlevels)

    def generatepositions(self, currentlist, myposition, mywidth):
    	if not self.children:
    		currentlist.append(myposition)
    		return
    	newwidth = mywidth/2
    	offsets = [[0,0], [0,newwidth], [newwidth,newwidth], [newwidth,0]]
    	for i in range(4):
    		newi = self.symmetry.actindex(i)
    		newposition = myposition.copy()
    		for j in range(2):
    			newposition[j] += offsets[newi][j]
    		self.children[i].generatepositions(currentlist, newposition, newwidth) 

class HilbertTreeMaxed(HilbertTree):

    def __init__(self, symmetry, level, position, width, height, maxfunc):
    	super().__init__(symmetry, level)
    	self.position = position
    	self.width = width
    	self.height = height
    	self.maxfunc = maxfunc

    def generatechildren(self, numlevels):
    	if self.level > numlevels or self.level > self.maxfunc(self.position, self.width, self.height):
    		return
    	elif self.children:
    		return

    	newwidth = self.width/2.0
    	newheight = self.height/2.0
    	offsets = [[0,0], [0,newheight], [newwidth,newheight], [newwidth,0]]
    	newpositions = [self.position.copy() for i in range(4)]
    	for i in range(4):
    		newi = self.symmetry.actindex(i)
    		for j in range(2):
    			newpositions[i][j] += offsets[newi][j]

    	newlevel = self.level + 1
    	newsymmetries = [self.symmetry for i in range(4)]
    	newsymmetries[0] = self.symmetry.times(SquareSymmetry(3,1))
    	newsymmetries[3] = self.symmetry.times(SquareSymmetry(1,1))
    	for i in range(4):
    		self.children.append(HilbertTreeMaxed(newsymmetries[i], newlevel, newpositions[i], newwidth, newheight, self.maxfunc))
    	
    	for i in range(4):
    		self.children[i].generatechildren(numlevels)
    	
    def generatepositions(self, currentlist):
    	if (not self.children):
    		currentlist.append(self.position)
    		return

    	for i in range(4):
    		self.children[i].generatepositions(currentlist)


class ImageProcessing:

    def invertcolor(ba):
    	if ba[1] == 0:
    		return 0 
    	else:
    		return 255 - ba[0]
    
    def bwtolevels(bw, minlevel, maxlevel):
    	base = 2.5
    	maxbw = 0
    	for i in range(len(bw)):
    		testmax = max(bw[i])
    		if testmax > maxbw:
    			maxbw = testmax
    
    	if maxbw == 0:
    		maxbw = 1.0
    
    	for i in range(len(bw)):
    		for j in range(len(bw[0])):
    			level = bw[i][j]/maxbw
    			level *= base**maxlevel - base**minlevel 
    			level += base**minlevel 
    			level = np.log(level)/np.log(base)
    			bw[i][j] = level

class LevelFilter:

    def __init__(self, levels):
    	self.levels = levels
    	self.imwidth = len(levels[0])
    	self.imheight = len(levels)
    	self.x0 = 0
    	self.x1 = self.imwidth
    	self.y0 = 0
    	self.y1 = self.imheight

    def filterfunc(pos, width, height):
    	return 0

    def setupxy(self, pos, width, height):
    	self.x0 = int(pos[0])
    	self.x0 = max(self.x0, 0)
    	self.x1 = int(self.x0 + width)
    	self.x1 = min(self.x1, self.imwidth)

    	self.y0 = int(pos[1])
    	self.y0 = max(self.y0, 0)
    	self.y1 = int(self.y0 + height)
    	self.y1 = min(self.y1, self.imheight)

class UseMax(LevelFilter):

    def filterfunc(self, pos, width, height):
    	floorlevel = 0
    	levelsmax = 0
    	self.setupxy(pos, width, height)
    	
    	for i in range(self.x0, self.x1, 1):
    		for j in range(self.y0, self.y1, 1):
    			if self.levels[j][i] > levelsmax:
    				levelsmax = self.levels[j][i]
    	if levelsmax < floorlevel:
    		return floorlevel
    	else:
    		return levelsmax 

class UseAverage(LevelFilter):

    def filterfunc(self, pos, width, height):
    	dx = 1
    	dy = 1
    	average = 0
    	nvalues = 0
    	self.setupxy(pos, width, height)

    	for i in range(self.x0, self.x1, dx):
    		for j in range(self.y0, self.y1, dy):
    			average += self.levels[j][i]
    			nvalues += 1
    	if nvalues > 0:
    		average /= nvalues
    	else:
    		average = 0

    	return average 

class UseMajority(LevelFilter):

    def __init__(self, levels, numlevels):
    	super().__init__(levels)
    	self.numlevels = numlevels

    def filterfunc(self, pos, width, height):
    	floorpercent = 0.99
    	minreturn = 0 # numlevels-3 
    
    	dx = 1
    	dy = 1
    	self.setupxy(pos, width, height)
    	
    	frequency = [0 for i in range(self.numlevels+1)]
    	nvalues = 0
    	for i in range(self.x0, self.x1, dx):
    		for j in range(self.y0, self.y1, dy):
    			k = self.levels[j][i]
    			k = max(0.0, k)
    			k = int(k)
    			k = min(len(frequency), k)
    			frequency[k] += 1
    			nvalues += 1
    	result = 0
    	maxfrequency = 0
    	someabovefloor = False
    	floor = nvalues * floorpercent
    	for i in range(len(frequency)):
    		if frequency[i] >= maxfrequency:
    			maxfrequency = frequency[i]
    			result = i
    		if frequency[i] > floor:
    			someabovefloor = True
    	if someabovefloor:
    		if result > minreturn:
    			return result
    		else:
    			return minreturn
    	else:
    		return self.numlevels+1

class CircleFilter(LevelFilter):

    def __init__(self, levels, maxlevel, treewidth, treeheight):

    	super().__init__(levels)

    	maxradius = np.sqrt(treewidth**2 + treeheight**2) / 3.0
    	floor = 3
    	self.circles = []
    	for i in range(15):
    		radius = random.random()* maxradius
    		xcenter = random.random()*treewidth
    		ycenter = random.random()*treeheight
    		circlelevel = maxlevel - floor + random.random() * floor
    		self.circles.append([xcenter, ycenter, radius, circlelevel])
    
    def circlepointmax(self, pos):
    	result = 0
    	for i in range(len(self.circles)):
    		thiscircle = self.circles[i]
    		dist = 0.0
    		for j in range(2):
    			dist += (pos[j] - thiscircle[j])**2
    		dist = np.sqrt(dist)
    		if dist < thiscircle[2] and thiscircle[3]>result:
    			result = thiscircle[3]
    	return result
    
    def filterfunc(self, pos, width, height):
    	ncheck = 5
    	result = 0
    	dx = width / ncheck	
    	dy =  height / ncheck 

    	checkx = pos[0]
    	checky = pos[1]
    	for i in range(ncheck):
    		for j in range(ncheck):
    			checkpos = [checkx, checky]
    			circlelevel = self.circlepointmax(checkpos) 
    			if circlelevel > result:
    				result = circlelevel 
    			checky += dy
    		checkx += dx

    	return result


