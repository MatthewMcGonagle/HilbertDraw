import numpy as np

class SquareSymmetry:

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

	def generatepositionswithmax(self, currentlist, myposition, mywidth, myheight, maxfunc):
		if (not self.children) or self.level > maxfunc(myposition, mywidth, myheight):  
			currentlist.append(myposition)
			return
		newwidth = mywidth/2
		newheight = myheight/2
		offsets = [[0,0], [0,newheight], [newwidth,newheight], [newwidth,0]]
		for i in range(4):
			newi = self.symmetry.actindex(i)
			newposition = myposition.copy()
			for j in range(2):
				newposition[j] += offsets[newi][j]
			self.children[i].generatepositionswithmax(currentlist, newposition, newwidth, newheight, maxfunc) 

