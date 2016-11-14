import numpy as np

LOWLEFTSTART = 0
UPLEFTSTART = 1
UPRIGHTSTART = 2
LOWRIGHTSTART = 3

CLOCKWISE = 1
COUNTERCLOCKWISE = -1

class SquareSymmetry:

	# reflection rotation^k

	def __init__(self, reflection, rotation):
		self.rotation = rotation % 4
		self.reflection = reflection % 2

	def times(self, symmetry):
		newrotation = self.rotation
		newreflection = self.reflection
		if symmetry.reflection:
			newrotation = (4 - newrotation) % 4
			newreflection = (newreflection + symmetry.reflection) % 2
		newrotation = (newrotation + symmetry.rotation) % 4
		return SquareSymmetry(newreflection, newrotation)

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

class HilbertSquare2:

	def __init__(self, symmetry, position, logwidth, level, backwards):
		self.symmetry = symmetry
		self.position = position.copy()
		self.logwidth = logwidth
		self.level = level
		self.backwards = backwards 
		self.children = []

	def addoffset(self, offset):
		newposition = [0,0]
		for i in range(2):
			newposition[i] = self.position[i]+offset[i]
		return newposition

	def generatechildren(self, level):
		self.children = []
		if level > 0:
			newlog = self.logwidth - 1
			newwidth = 2**newlog
			width = 2**self.logwidth
			newlevel = level - 1
			newbackwards = self.backwards

			newsymmetry = self.symmetry.times(SquareSymmetry(1,1))
			offset = [0,0]
			newposition = self.addoffset(offset)
			self.children.append(HilbertSquare2(newsymmetry, newposition, newlog, newlevel, newbackwards))

			newsymmetry = self.symmetry
			offset = [0, newwidth]
			offset = self.symmetry.action(offset)
			newposition = self.addoffset(offset)
			self.children.append(HilbertSquare2(newsymmetry, newposition, newlog, newlevel, newbackwards))

			newsymmetry = self.symmetry#.times(SquareSymmetry(1,0))
			offset = [newwidth, newwidth]
			offset = self.symmetry.action(offset)
			newposition = self.addoffset(offset)
			#newbackwards = (self.backwards + 1) % 2
			self.children.append(HilbertSquare2(newsymmetry, newposition, newlog, newlevel, newbackwards))

			newsymmetry = self.symmetry.times(SquareSymmetry(1,3))
			offset = [width, newwidth]
			offset = self.symmetry.action(offset)
			newposition = self.addoffset(offset)
			self.children.append(HilbertSquare2(newsymmetry, newposition, newlog, newlevel, newbackwards))

			for i in range(len(self.children)):
				self.children[i].generatechildren(newlevel)

			
	def getpositions(self, currentpositions):
		if not self.children:
			width = 2**(self.logwidth)
			newwidth = 2**(self.logwidth-1)
			#height = 2**(self.logwidth)
			#spacing = 2**(self.logwidth-2) 
			#offsets = [[spacing,spacing], [spacing, height-spacing], [width-spacing,height-spacing], [width-spacing,spacing] ]
			#offsets = [[0,0], [0, height-spacing], [width-spacing,height-spacing], [width-spacing,0] ]
			#numoffsets = len(offsets)
			#if not self.backwards:
			#	for i in range(numoffsets):
			#		newposition = self.addoffset(self.symmetry.action(offsets[i]))
			#		currentpositions.append(newposition)
			#else:
			#	for i in range(numoffsets):
			#		newposition = self.addoffset(self.symmetry.action(offsets[numoffsets-1-i]))
			#		currentpositions.append(newposition)
		#else:
			#if not self.backwards:
			#	for i in range(4):
			#		self.children[i].getpositions(currentpositions)
			#else:
			#	for i in range(4):
			#		self.children[3-i].getpositions(currentpositions)
			offsets = [[0,0], [0,newwidth], [newwidth, newwidth], [newwidth, 0]] 
			for i in range(len(offsets)):
				newposition = self.symmetry.action(offsets[i])
				newposition = self.addoffset(newposition)
				currentpositions.append(newposition)
		else:
			for i in range(4):
				self.children[i].getpositions(currentpositions)	
		
class HilbertConfig:

	def __init__( self, start, orientation, position, drawposition, logwidth):
		self.start = start
		self.orientation = orientation
		self.position = position
		self.drawposition = drawposition
		self.logwidth = logwidth

	def gettransformed(self, fourarray, index):
		if self.orientation == COUNTERCLOCKWISE:
			newindex = (index + self.start) % 4
		else:
			newindex = (4 - index + self.start) % 4
		return fourarray[newindex]

	def getoffsets(self, size):
		return [ [0,0], [0, size], [size, size], [size,0] ]



	def subconfig(self, index):
		index = index % 4
		if index == 0:
			newstart = self.start
			neworientation = self.orientation * -1
		elif index == 1 or index == 2:
			newstart = self.start
			neworientation = self.orientation 
		else:
			newstart = (self.start + 2) % 4
			neworientation = self.orientation * -1 
		newwidth = 2**(self.logwidth-1)
		newoffsets = self.getoffsets(newwidth)
		#newoffsets = [ [0,0], [0, newwidth], [newwidth, newwidth], [newwidth,0] ]
		#if self.orientation == COUNTERCLOCKWISE:
		#	newposition = newoffsets[(self.start + index) % 4]
		#else:
		#	newposition = newoffsets[(self.start + 4 - index) % 4]
		newposition = self.gettransformed(newoffsets, index)
		for i in range(2):
			newposition[i] += self.position[i]

		newheight = newwidth
		newwidth = 2**(self.logwidth)-1
		newoffsets = self.getoffsets(newwidth)
		newoffsets = [[0,0], [0, newheight], [newwidth, newheight], [newwidth, 0]]
		newdrawposition = self.gettransformed(newoffsets, index)
		for i in range(2):
			newdrawposition[i] += self.position[i]

		
		
		return HilbertConfig(newstart, neworientation, newposition, newdrawposition, self.logwidth - 1)

class HilbertSquare:

	def __init__( self, parent, config):
		self.parent = parent
		self.config = config
		self.children = []
		self.floor = 0

	def generatechildren(self, level):
		if level > 0:
			for i in range(4):
				newconfig = self.config.subconfig(i)
				self.children.append(HilbertSquare(self, newconfig))
				self.children[i].generatechildren(level-1)

	def generatewithmin(self, level, maxfunc):
		self.floor = maxfunc(self.config.position, self.config.logwidth)
		if level > 0 and level > self.floor:
			for i in range(4):
				newconfig = self.config.subconfig(i)
				self.children.append(HilbertSquare(self, newconfig))
				self.children[i].generatewithmin(level-1, maxfunc)


	def getpositions(self, currentpositions):
		if not self.children:
			currentpositions.append(self.config.drawposition)
		else:
			for i in range(4):
				self.children[i].getpositions(currentpositions)

	def getpositionswithmin(self, currentpositions):
		if not self.children and self.floor < self.config.logwidth:
			currentpositions.append(self.config.position)
		else:
			level = self.config.logwidth
			offset = 2**(level-1)
			offset = 2**level - 1
			centers = [[offset-1, offset-1],
				   [offset-1, offset],
				   [offset,offset],
				   [offset,offset-1]]
			for i in range(4):
				if self.children[i].floor < level:
					self.children[i].getpositions(currentpositions)
				else:
					print("Jump")

				#if self.children[i].floor > 2: #level - 4:
				#	print("Jump")
				#	newposition = centers[(self.config.orientation+i)%4]
				#	for k in range(2):
				#		newposition[k] += self.config.position[k]
				#	currentpositions.append(newposition.copy())
				#else:
				#	self.children[i].getpositions(currentpositions)

class FourSquares:

	def __init__(self, parent, start, orientation):
		self.parent = parent
		self.start = start
		self.orientation = orientation
		self.children = []

	def generatechildren(self):
		newstart = self.start 
		neworientation = self.orientation * -1
		self.children.append( FourSquares(self, newstart, neworientation) )

		neworientation *=  -1
		self.children.append( FourSquares(self, newstart, neworientation) )
		self.children.append( FourSquares(self, newstart, neworientation) )

		newstart = (newstart + 2) % 4
		neworientation *= -1 
		self.children.append( FourSquares(self, newstart, neworientation) )

def generatesquaretree(currentsquare, level):
	if(level < 1):
		return
	currentsquare.generatechildren()
	for i in range(4):
		generatesquaretree(currentsquare.children[i], level-1)

def printsquaretree(currentsquare, level):
	print(level, end="")
	for i in range(level):
		print(". . . . . . ", end = "")
	print("Start = ", currentsquare.start, end = "")
	print(", Orientation = ", currentsquare.orientation)
	if not currentsquare.children:
		return
	else:
		for i in range(4):
			printsquaretree(currentsquare.children[i], level+1)
		return

def generatepositions(poslist, currentpos, currentsquare, level, onlyint = False):
	if not currentsquare.children: 
		poslist.append(currentpos)
		return

	if level<0 and onlyint:
		print("Error generatepositions: level = ", level)
		return

	offset = 2**level
	if(currentsquare.orientation == COUNTERCLOCKWISE):
		outoforderoffset = [[0, 0],
				 [0, offset],
				 [offset, offset],
				 [offset, 0]]
		newoffset = [outoforderoffset[(i+currentsquare.start)%4] for i in range(4)]
	else:
		outoforderoffset = [[0, 0],
				 [offset, 0],
				 [offset, offset],
				 [0, offset]]
		newoffset = [outoforderoffset[(i+currentsquare.start)%4] for i in range(4)]
	
	for i in range(4):
		newpos = currentpos.copy()
		for j in range(2):
	        	newpos[j] = newoffset[i][j] + currentpos[j]		
		generatepositions(poslist, newpos, currentsquare.children[i], level-1)

	return

def paintpositions(coord, pos1, pos2):
	if pos1[0] != pos2[0]:
		j = pos1[1]
		change = pos2[0] - pos1[0]
		if change > 0: 
			start = pos1[0]
		else:
			start = pos2[0]
			change *= -1
		for i in range(change+1):
			k = start + i 
			coord[k][j] = "*" 
	if pos1[1] != pos2[1]:
		i = pos1[0]
		change = pos2[1] - pos1[1]
		if change > 0: 
			start = pos1[1]
		else:
			start = pos2[1]
			change *= -1
		for j in range(change+1):
			k = start + j 
			coord[i][k] = "*" 

	return
		

def HilbertDraw( coord, level):
	size = len(coord)
	if( len(coord[0]) != size ):
		print("Error HilbertDraw: coord not square array.")
		return

	power = np.log2(size)
	if( int(power) != power):
		print("Error HilbertDraw: dimensions coord are not integer power of two.")
		return
	power = int(power)
	
	if(level > power):
		print("Error HilbertDraw: level > power")
		return

	
