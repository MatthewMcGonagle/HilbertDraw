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

        Each symmetry is represented as rotation**self.rotation * reflection**self.reflection.        

        Members
        -------
        self.rotation : Int
            The amount the sub-square is rotated relative to the standard orientation. Is either
            0, 1, 2, or 3 to represent 4 possible rotations of 0, 90, 180, and 270 degrees.
        self.reflection : Int
            Represents whether there is a reflection. Has value 0 for NO reflection and value 1 if there
            is a reflection.
    '''

    def __init__(self, rotation, reflection):
        '''
        Initializer
        Parameters
        ----------
        self : self
            Implicit reference to self.
        rotation : Int
            Number of 90 degree rotations. Using modulo 4 arithmetic, it will be reduced to either 0,
            1, 2, or 3.
        reflection : Int
            Whether there is a reflection. Using modulo 2 arithmetic, it will be reduced to either 0 or 1.     
        '''
        self.rotation = rotation % 4
        self.reflection = reflection % 2

    def times(self, symmetry):
        '''
        Composes another symmetry with self.

        Parameters
        ----------
        self : self
            Implicit reference to self.
        symmetry : class SquareSymmetry
            The other symmetry to compose with self. 

        Returns
        -------
        class SquareSymmetry
            A reference to an instance of SquareSymmetry resulting from the composition.
        '''

        newrotation = symmetry.rotation
        if self.reflection:
            newrotation = (4 - newrotation) % 4
        newreflection = (self.reflection + symmetry.reflection) % 2
        newrotation = (newrotation + self.rotation) % 4
        return SquareSymmetry(newrotation, newreflection)

    def getreflection(self):
        '''
        Return the reflection.

        Parameters
        ----------
        self : self
            Implicit reference to self.
        
        Returns
        -------
        Int
            Reference to self.reflection.
        '''
        return self.reflection

    def action(self, vector):
        '''
        Applies the symmetry transformation represented by self to a 2D vector.
        
        Parameters
        ----------
        self : self
            Implicit reference to self.
        vector : Array-like Should have 2 elements. Represents the vector to be acted upon.

        Returns
        -------
        Array-like
            Has 2 element. Result of applying the symmetry transformation to the vector. 
        '''
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
        '''
        Finds the permutation of the indices 0, 1, 2, and 3 that correspond to applying the 
        symmetry transformation. So in a 2x2 square grid indexed 0 to 3 in a fixed manner, 
        this tells you which square is first to last after the transformation. 
        Paramters
        ---------
        self : self
            Implicit reference to self.
        index : Int
            Index to permute. Should be 0, 1, 2, or 3.
        
        Returns
        -------
        Int
            New permuted index. Should be 0, 1, 2, or 3.
        '''

        newindex = (self.rotation + index) % 4
        if self.reflection > 0:
            newindex = (3*(newindex+1)) % 4
        return newindex

class HilbertTree:
    '''
    Class for generating sub-square grid for Hilbert pseudo-curves. Keeps track of symmetries in
    each square and the positions associated with each sub-square. Generates this info to a certain
    level of pseudo-curves. This is class is only used to make basic Hilbert pseudo-curves.

    Each instance represents a node in the tree of sub-squares, i.e. a single square at a certain level. 
    The children of an instance are its 4 sub-squares at the next level.

    Members
    -------
    self.symmetry : SquareSymmetry
        The symmetry transformation associated with this square, that is the orientation of the 
        Hilbert pseudo-curve for this level and this square.
    self.level : Int
        The level of Hilbert pseudo-curve this node is on, i.e. the height from the root node. 
    self.children : List of HilbertTree
        The sub-squares of this square that are a part of the next level of Hilbert pseudo-curve.
    '''

    def __init__(self, symmetry, level):
        '''
        Initializer
    
        Parameters
        ----------
        self : self
            Implicit reference to self.
        symmetry : SquareSymmetry
            The symmtery transformation of the orientation of the Hilbert pseudo-curve for this square.
        level : Int
            The level of Hilbert pseudo-curve this square is associated to, i.e. the height from the
            root node of the tree.
        '''
        self.symmetry = symmetry
        self.level = level
        self.children = []

    def generatechildren(self, numlevels):
        '''
        Create children of this node. The children are part of the Hilbert pseudo-curve at the next level
        and make by dividing this square into an even 2x2 grid of sub-squares. They inherit orientations
        in a certain way from the orientation of this node.

        The function continues to recurse down the tree (depth first) to create a certain number of levels.
        Parameters
        ----------
        self : self
            Implicit reference to self.
        numlevels: Int
            The number of levels to create. Function will not beyond numlevels. 
        '''
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
        '''
        Recursively add the positions of the leaf sub-squares to a list of square positions. If
        this node is a leaf, then add it to the list of positions. Else, use the position of this 
        node to calculate the positions of the children and then recurse down.

        Parameters
        ----------
        self : self
            Implicit reference to self.
        currentlist : Array-like
            Holds a reference to the current list of positions so far.
        mypositions : Array-like
            Has 2 elements; the xy position of this square.
        mywidth : Int
            The width of this square.
        '''
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
    '''
    Class to draw a picture using different levels of Hilbert pseudo-curves. 
    To determine whether to sub-divide a sub-square into the next level, use a max function 
    f(x,y) for this sub-square. This max function gives the maximum level to descend to for 
    any sub-square with position at (x,y). 

    So for an input image, one should use a maximum function f(x,y) defined using the 
    pixel colors in the image. 

    An instance of this class represents a node in the quad-tree that gives the sub-divisions of the 
    sub-squares defining the Hilbert pseudo-curves.

    This class inherits properties from HilbertTree.

    Members
    -------
    self.symmetry : SquareSymmetry
        Represents the orientation of this sub-square relative to the standard orientation. 
    self.level : Int
        Represents the level of the Hilbert pseudo-curve that this node is a part of.
    self.position : Array-like
        Has two members. Represents the position (x,y) of this node in space.
    self.width : Int
        The width of this sub-square.
    self.height : Int
        The height of this sub-square.
    self.maxfunc : function
        A function from positions (x,y) (Array-like with two members) into Int. The function
            should give the max level of Hilbert pseudo-curve to associate with a sub-square at
            position (x,y).
    '''

    def __init__(self, symmetry, level, position, width, height, maxfunc):
        ''' 
        Initializer that calls parent initializer for HilbertTree
        
        Parameters
        ----------
        self : self
            Implicit reference to self.
        symmetry : SquareSymmetry
            Reperesents the orientation of this sub-square relative to the standard orientation.
        level : Int
            The level of Hilbert pseudo-curve to associate with this sub-square node.
        position : Array-like
            Should have two elements representing the (x,y) position of this sub-square.
        width : Int
            The width of this sub-square.
        height : Int
            The height of this sub-square.
        maxfunc : function
            The function to determine how far to sub-divide a given sub-square. Should be a function from 
            positions (x,y) (represented as array-likes with two elements) into Int. The position
            of a sub-square is used to determine whether to sub-divide further based on the output
            of this function.
        ''' 
        super().__init__(symmetry, level)
        self.position = position
        self.width = width
        self.height = height
        self.maxfunc = maxfunc

    def generatechildren(self, numlevels):
        '''
        Generates the children nodes of this sub-square. This over-rides the generatechildren of the 
        parent class HilbertTree. Now we use self.maxfunc to decide if we have reached a high enough
        level of pseudo-curve using self.position. We also put a global maximum on the levels using 
        the parameter numlevels. If we have not reached the max level for this sub-square, then 
        we sub-divide and find the children.
        
        Parameters
        ----------
        self : self
            Implicit reference to self.
        numlevels : Int
            The global maximum number of levels to make the tree. 
        '''
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
        '''
        Add the leaf sub-nodes of this node to a current list of positions. The order that they are added is the
        order they occur in the curve representing the image. This is accomplished using a depth first traversal. 
        
        Parameters
        ----------
        self : self
            Implicit reference to self.
        currentlist : Array-like
            The list of positions to add the leaf positions to.
        '''
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


