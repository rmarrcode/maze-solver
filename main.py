import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import heapq

#represents a Node for a graph search
#each node is a place in the graph where the direction thru the graphcan be changed
#each node records the path to get to the node so that it can be retraced and colored blue
class Node(object):

    def __init__(self, i, j, val, prev, path):
        self.i = i
        self.j = j
        self.val = val
        self.prev = prev
        self.path = path

    def __lt__(self, other):
        return self.val < other.val

    def getPos(self):
        return (self.i, self.j)
    
    def getVal(self):
        return self.val
    
    def updateVal(self, val):
        self.val = val

    def getPrev(self):
        return self.prev
    
    def getPath(self):
        return self.path


#represents the state of the Maze
#stores the maze image and the coordinates of the first point
#stores the heap that sorts the nodes to perforn Dijsktra's algorithm
#also uses a dictionary to keep track of the nodes   
class Maze(object):

    def __init__(self, img):
        self.img = img
        self.starti = -1
        self.startj = -1
        self.heap = []
        self.seenPos = dict()

    #procudure if solution is found 
    #retraces the path and prints the path in blue
    def foundSoln(self, iterNode):
        while (iterNode != None):
            (i, j) = iterNode.getPos()
            self.img[i][j] = [0,0,1]
            for loc in iterNode.getPath():
                self.img[loc[0]][loc[1]] = [0,0,1]
            iterNode = iterNode.getPrev()
     
    def inBounds(self, i , j):
        if (i < 0 or i >= self.img.shape[0] or j < 0 or j >= self.img.shape[1]):
            return False
        return True

    #a pixel is a node iff there is multiple ways to move from that pixel
    def isNode(self, i, j):
        placesToMove = 0
        if (not self.inBounds(i, j)):
            return False
        if ( (i,j) in self.seenPos ):
            return False
        if (self.img[i][j] == [0,0,0]).all():
            return False
        if ( i-1 >= 0):
            if not ((self.img[i-1][j] == [0,0,0]).all()):
                placesToMove = placesToMove+1
        if ( i+1 < self.img.shape[0]):
            if not ((self.img[i+1][j] == [0,0,0]).all()):
                placesToMove = placesToMove+1
        if ( j-1 >= 0):
            if not ((self.img[i][j-1] == [0,0,0]).all()):
                placesToMove = placesToMove+1
        if ( j+1 < self.img.shape[1]):
            if not ((self.img[i][j+1] == [0,0,0]).all()):
                placesToMove = placesToMove+1
        if (placesToMove > 2):
            return True
        else: return False
        
    #performs the action of moving through the graph    
    def move(self, direction, i , j, steps):
        print(str(i) + " " + str(j))
        if (not self.inBounds(i,j)):
            return None 
        if ((self.img[i][j] == [0,0,0]).all()):
            return None
        if ((self.img[i][j] == [1,0,0]).all()):
            return None
        if ((self.img[i][j] == [0,1,0]).all()):
            return (i, j, steps)
        if (self.isNode(i, j)):
            return (i, j, steps)     
        hasUp = False
        if (i-1 >= 0):
            hasUp = not (self.img[i-1][j] == [0,0,0]).all()
        hasLeft = False
        if (j-1 >= 0):
            hasLeft = not (self.img[i][j-1] == [0,0,0]).all()
        hasRight = False
        if (j+1 < self.img.shape[1]):
            hasRight = not (self.img[i][j+1] == [0,0,0]).all()
        hasDown = False
        if (i+1 < self.img.shape[0]):
            hasDown = not (self.img[i+1][j] == [0,0,0]).all()
        if (direction == "u"):
            if (hasLeft): return self.move("l", i, j-1, steps + [(i,j-1)] )
            if (hasUp): return self.move("u", i-1, j, steps + [(i-1,j)] )
            if (hasRight): return self.move("r", i, j+1, steps + [(i,j+1)] )
        elif (direction == "d"):
            if (hasLeft): return self.move("l", i, j-1, steps + [(i,j-1)] )
            if (hasDown): return self.move("d", i+1, j, steps + [(i+1, j)] )
            if (hasRight): return self.move("r", i, j+1, steps + [(i, j+1)] )
        elif (direction == "l"):
            if (hasLeft): return self.move("l", i, j-1, steps + [(i,j-1)] )
            if (hasDown): return self.move("d", i+1, j, steps + [(i+1, j)] )
            if (hasUp): return self.move("u", i-1, j, steps + [(i-1,j)] )
        elif (direction == "r"):
            if (hasDown): return self.move("d", i+1, j, steps + [(i+1,j)] )
            if (hasUp): return self.move("u", i-1, j, steps + [(i-1,j)] )
            if (hasRight): return self.move("r", i, j+1, steps + [(i,j+1)] )
        else:
            return None            

    #finds neighbors of a node by looking in each direction
    def getNeighbors(self, node):
        [i,j] = node.getPos()
        ans = []
        ans.append((self.move("u", i-1, j, [(i-1, j)] )))
        ans.append((self.move("d", i+1, j, [(i+1, j)] )))
        ans.append((self.move("r", i, j+1, [(i, j+1)] )))
        ans.append((self.move("l", i, j-1, [(i, j-1)] )))
        return ans

    #drives the search process
    #finds starting position and performs Dijkstra's algorithm
    #if the solution is found, foundSoln is called on this node
    def search(self):
        for i in range(self.img.shape[0]):
            for j in range(self.img.shape[1]):
                if ((self.img[i,j] == [1,0,0]).all()):
                    starti = i
                    startj = j
        start = Node(starti,startj,0,None, [])
        adjLst = dict()
        adjLst[start] = None
        heap = [start]
        while (len(heap) != 0):
            u = heapq.heappop(heap)
            posu = u.getPos()
            self.seenPos[posu] = True
            neighbors = self.getNeighbors(u)
            for x in range(len(neighbors)):
                if (neighbors[x] != None):
                    (i, j, path) = neighbors[x]
                    v = Node(i, j, pow(2,63)-1, u, path)
                    if (v.getVal() > u.getVal() + len(path)):
                        v.updateVal(u.getVal() + len(path))
                        heapq.heappush(heap, v)
                    if (self.img[i][j] == [0,1,0]).all():
                        self.foundSoln(v)
                        return



def main():

    img = mpimg.imread('maze.png')

    maze = Maze(img)
    maze.search()

    plt.figure(1)
    plt.imshow(img)
    plt.show()

if __name__ == "__main__":
    main()
