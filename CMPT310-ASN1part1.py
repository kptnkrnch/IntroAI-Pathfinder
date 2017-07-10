############################################################################
# Project: Pathfinding for shortest path
# Author: Joshua Campbell
# Student Number: 301266191
# Date: October 10, 2016
############################################################################
import time
import sys
# Tile class, used for representing nodes on the grid
class Tile:
    def __init__(self, x, y, name=None):
        self.x = x  # x location on the grid
        self.y = y  # y location on the grid
        self.solid = False  # boolean for checking if this tile is a wall or not
        self.parent = None  # Parent tile for this tile
        self.cost = 0  # The current cost to get to the node so far
        self.heuristic = 0  # The heuristic cost to a goal point
        self.estimate = 0  # The estimated cost to a goal point (cost + heuristic)
        self.onPath = False  # boolean flag for whether this tile node is part of the path or not
        self.name = name  # name of the tile (if it has one, ie a landmark)

    def setSolid(self, solid):
        self.solid = solid

    def setEstimate(self, estimate):
        self.estimate = estimate

    def getEstimate(self):
        return self.estimate

    # Calculates the estimated cost by adding the current cost with the heuristic
    def calculateEstimate(self):
        self.estimate = self.cost + self.heuristic

    def setCost(self, cost):
        self.cost = cost
        self.calculateEstimate()

    def getCost(self):
        return self.cost

    def setHeuristic(self, heuristic):
        self.heuristic = heuristic

    def getHeuristic(self):
        return self.heuristic

    # Calculates the heuristic as the minimum number of moves needed to get from one point to another.
    # This calculation is essentially the x distance plus the y distance between two points.
    # For example, (5,5) and (8,9) would be 8-5 = 3 for the x distance and 9-5 = 4 for the y distance.
    # Therefore, the heuristic would be 3 + 4 = 7 which would be the minimum number of moves to get to (8,9).
    def generateHeuristic(self, goalX, goalY):
        self.heuristic = abs(goalX - self.x) + abs(goalY - self.y)

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def isSolid(self):
        return self.solid

    # Used for taking a peek at a new estimate for a node without storing that new estimate
    def peekEstimate(self, cost):
        return self.heuristic + cost

# shortcut function for calculating and setting the heuristics for all of the tile nodes on the map
def calculateHeuristics(_goalX, _goalY, _searchMap):
    for x in range(gridWidth):
        for y in range(gridHeight):
            tempnode = searchMap[x][y]
            tempnode.generateHeuristic(_goalX, _goalY)
            searchMap[x][y] = tempnode

# finds the lowest costing node (based on current cost in path and its heuristic) and returns the index of the node
# in the openNodes list.
def findLeastCostNode(_openNodes):
    leastCostNode = None
    leastCostIndex = 0
    currentIndex = 0
    for node in _openNodes:
        node.calculateEstimate()
        if leastCostNode is None:
            leastCostNode = node
            leastCostIndex = currentIndex
        else:
            if node.getEstimate() < leastCostNode.getEstimate():
                leastCostNode = node
                leastCostIndex = currentIndex
        currentIndex = currentIndex + 1

    return leastCostIndex

# visitNeighbours expands the tiles to the north, east, south, and west of the current node.
# If one of these nodes has not been visited, it is added on to the openNodes list. If it has been visited and if
# it is in either the openNodes or the closedNodes list, the algorithm checks if there if the cost from the current node
# is less than the previous cost. If it is, it is added back into the openNodes list.
def visitNeighbours(_node, _goalX, _goalY, _searchMap, _openNodes, _closedNodes):
    global frontierCount
    _x = _node.x
    _y = _node.y
    if _x - 1 >= 0:
        temp = _searchMap[_x - 1][_y]
        if isGoalNode(temp, _goalX ,_goalY): # If the node is the goal node, set the current node as its parent and return it
            temp.setParent(_node)
            return temp

        # if temp is a traversable node and it is not in the closed or open lists, set its cost and add it to the opennodes list
        if temp not in _openNodes and temp not in _closedNodes and not temp.isSolid():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
            _openNodes.append(temp)
            frontierCount += 1
        # else if temp is in the openNodes list, but the cost of getting there from the current node is less than before, update its cost
        elif temp in _openNodes and temp.peekEstimate(_node.getCost() + 1) < temp.getEstimate():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
        # else if temp is in the closedNodes list, but the cost of getting there from the current node is less than before, update
        # its cost and add it back into the openNodes list.
        elif temp in _closedNodes and temp.peekEstimate(_node.getCost() + 1) < temp.getEstimate():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
            _openNodes.append(temp)
            _closedNodes.remove(temp)

    if _x + 1 <= (gridWidth - 1):
        temp = _searchMap[_x + 1][_y]
        if isGoalNode(temp, _goalX ,_goalY): # If the node is the goal node, set the current node as its parent and return it
            temp.setParent(_node)
            return temp

        # if temp is a traversable node and it is not in the closed or open lists, set its cost and add it to the opennodes list
        if temp not in _openNodes and temp not in _closedNodes and not temp.isSolid():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
            _openNodes.append(temp)
            frontierCount += 1
        # else if temp is in the openNodes list, but the cost of getting there from the current node is less than before, update its cost
        elif temp in _openNodes and temp.peekEstimate(_node.getCost() + 1) < temp.getEstimate():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
        # else if temp is in the closedNodes list, but the cost of getting there from the current node is less than before, update
        # its cost and add it back into the openNodes list.
        elif temp in _closedNodes and temp.peekEstimate(_node.getCost() + 1) < temp.getEstimate():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
            _openNodes.append(temp)
            _closedNodes.remove(temp)

    if _y - 1 >= 0:
        temp = _searchMap[_x][_y - 1]
        if isGoalNode(temp, _goalX ,_goalY): # If the node is the goal node, set the current node as its parent and return it
            temp.setParent(_node)
            return temp

        # if temp is a traversable node and it is not in the closed or open lists, set its cost and add it to the opennodes list
        if temp not in _openNodes and temp not in _closedNodes and not temp.isSolid():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
            _openNodes.append(temp)
            frontierCount += 1
        # else if temp is in the openNodes list, but the cost of getting there from the current node is less than before, update its cost
        elif temp in _openNodes and temp.peekEstimate(_node.getCost() + 1) < temp.getEstimate():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
        # else if temp is in the closedNodes list, but the cost of getting there from the current node is less than before, update
        # its cost and add it back into the openNodes list.
        elif temp in _closedNodes and temp.peekEstimate(_node.getCost() + 1) < temp.getEstimate():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
            _openNodes.append(temp)
            _closedNodes.remove(temp)

    if _y + 1 <= (gridHeight - 1):
        temp = _searchMap[_x][_y + 1]
        if isGoalNode(temp, _goalX ,_goalY): # If the node is the goal node, set the current node as its parent and return it
            temp.setParent(_node)
            return temp

        # if temp is a traversable node and it is not in the closed or open lists, set its cost and add it to the opennodes list
        if temp not in _openNodes and temp not in _closedNodes and not temp.isSolid():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
            _openNodes.append(temp)
            frontierCount += 1
        # else if temp is in the openNodes list, but the cost of getting there from the current node is less than before, update its cost
        elif temp in _openNodes and temp.peekEstimate(_node.getCost() + 1) < temp.getEstimate():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
        # else if temp is in the closedNodes list, but the cost of getting there from the current node is less than before, update
        # its cost and add it back into the openNodes list.
        elif temp in _closedNodes and temp.peekEstimate(_node.getCost() + 1) < temp.getEstimate():
            temp.setParent(_node)
            temp.setCost(_node.getCost() + 1)
            _openNodes.append(temp)
            _closedNodes.remove(temp)

    return None

# Checks if a Tile node is the goal point
def isGoalNode(_node, _goalX, _goalY):
    if _node.x == _goalX and _node.y == _goalY:
        return True
    else:
        return False

# findPath is the main body for the pathfinding algorithm (A*).
# findPath returns the path it found between the start and the goal.
# findPath also labels the nodes on the map as being "onPath" for printing purposes.
def findPath(_startX, _startY, _goalX, _goalY, _searchMap):
    openNodes = []
    closedNodes = []

    openNodes.append(searchMap[_startX][_startY]) # appending the starting node
    calculateHeuristics(_goalX, _goalY, _searchMap) # calculates the heuristics for all nodes in the map

    path = []

    while len(openNodes) > 0:
        index = findLeastCostNode(openNodes) # get the index of the lowest cost node in the openNodes list
        node = openNodes.pop(index) # remove the lowest costing node from the openNodes list

        # Expand the neighbours of the lowest costing node and add them to the openNodes list
        goal = visitNeighbours(node, _goalX, _goalY, _searchMap, openNodes, closedNodes)
        if goal is not None: # if the goal node is found, we are done
            temp = goal

            # once the goal node is found, backtrack from that node to its parent and its parents parent, etc
            # until we get back to the starting node. Add all of these nodes/parents to the path list.
            while temp.getParent() is not None:
                path.append(temp)
                temp = temp.getParent()
            path.append(temp)
            break
        closedNodes.append(node)

    # setting the path node flag for nodes in the map for printing purposes
    for node in path:
        node.onPath = True

    return path

def readMapFile(_fileName):
    readSize = False
    with open(_fileName) as f:
        content = f.readlines()
    global gridWidth
    global gridHeight
    gridHeight = len(content)
    currentY = gridHeight - 1
    for line in content:
        curline = line.split()
        if curline:
            lineTiles = [int(i) for i in curline]
            if not readSize:
                readSize = True
                gridWidth = len(lineTiles)
                searchMap = [[Tile(x, y) for y in range(gridHeight)] for x in range(gridWidth)]

            if len(lineTiles) > gridWidth:
                return None
            currentX = 0
            if readSize:
                for tile in lineTiles:
                    if tile == 1:
                        searchMap[currentX][currentY].setSolid(True)
                    currentX += 1
        currentY -= 1

    return searchMap


gridWidth = 18
gridHeight = 18
global frontierCount
frontierCount = 0
searchMap = []
isValidInput = True
if len(sys.argv) == 1:
    # Generating an 18x18 map
    searchMap = [[Tile(x, y) for y in range(gridHeight)] for x in range(gridWidth)]

    # Setting up the walls on the map
    searchMap[7][5].setSolid(True)
    searchMap[7][6].setSolid(True)
    searchMap[7][7].setSolid(True)
    searchMap[7][8].setSolid(True)
    searchMap[7][9].setSolid(True)
    searchMap[10][13].setSolid(True)
    searchMap[11][13].setSolid(True)
    searchMap[12][13].setSolid(True)
    searchMap[13][13].setSolid(True)
    searchMap[14][13].setSolid(True)
    searchMap[15][13].setSolid(True)
    searchMap[15][12].setSolid(True)

    # Start point and goal point
    startX = 0
    startY = 0
    goalX = 17
    goalY = 17
elif len(sys.argv) == 5:
    # Start point and goal point via Command Line arguments
    startX = int(sys.argv[1])
    startY = int(sys.argv[2])
    goalX = int(sys.argv[3])
    goalY = int(sys.argv[4])

    # Generating an 18x18 map
    searchMap = [[Tile(x, y) for y in range(gridHeight)] for x in range(gridWidth)]

    # Setting up the walls on the map
    searchMap[7][5].setSolid(True)
    searchMap[7][6].setSolid(True)
    searchMap[7][7].setSolid(True)
    searchMap[7][8].setSolid(True)
    searchMap[7][9].setSolid(True)
    searchMap[10][13].setSolid(True)
    searchMap[11][13].setSolid(True)
    searchMap[12][13].setSolid(True)
    searchMap[13][13].setSolid(True)
    searchMap[14][13].setSolid(True)
    searchMap[15][13].setSolid(True)
    searchMap[15][12].setSolid(True)

    if searchMap[startX][startY].isSolid():
        print "Error: the starting point cannot be a wall."
        isValidInput = False

    if searchMap[goalX][goalY].isSolid():
        print "Error: the goal point cannot be a wall."
        isValidInput = False

    if goalX < 0 or goalY < 0 or startX < 0 or startY < 0:
        isValidInput = False
    if goalX > gridWidth - 1 or startX > gridWidth - 1:
        isValidInput = False
    if goalY > gridHeight - 1 or startY > gridHeight - 1:
        isValidInput = False
elif len(sys.argv) == 6:
    # Start point and goal point via Command Line arguments
    startX = int(sys.argv[1])
    startY = int(sys.argv[2])
    goalX = int(sys.argv[3])
    goalY = int(sys.argv[4])
    # Generating Map from Map File
    searchMap = readMapFile(sys.argv[5])
    if searchMap is None:
        print "Error loading map file!"
        isValidInput = False

    if searchMap[startX][startY].isSolid():
        print "Error: the starting point cannot be a wall."
        isValidInput = False

    if searchMap[goalX][goalY].isSolid():
        print "Error: the goal point cannot be a wall."
        isValidInput = False

    if goalX < 0 or goalY < 0 or startX < 0 or startY < 0:
        isValidInput = False
    if goalX > gridWidth - 1 or startX > gridWidth - 1:
        isValidInput = False
    if goalY > gridHeight - 1 or startY > gridHeight - 1:
        isValidInput = False
else:
    # Program Usage
    isValidInput = False
    print "Usage 1: python CMPT310-ASN1part1.py"
    print "Usage 3: python CMPT310-ASN1part1.py <startX> <startY> <goalX> <goalY>"
    print "Usage 2: python CMPT310-ASN1part1.py <startX> <startY> <goalX> <goalY> <mapFile>"

if isValidInput:
    # Finding the shortest path between the start point and the goal point
    start_time = time.time()
    finalPath = findPath(startX, startY, goalX, goalY, searchMap)
    end_time = time.time()
    finalPath.reverse()

    # Reversing the map so that the printing matches the specified map in the Assignment
    searchMap.reverse()
    for x in range(gridWidth):
        searchMap[x].reverse()
    searchMap.reverse()

    # Printing the map and the path (+ symbols)
    print "Map: (0's are traversable nodes, 1's are nontraversable nodes, +'s are path nodes)"
    for y in range(gridHeight):
        for x in range(gridWidth):
            if searchMap[x][y].isSolid():
                print 1, ' ',
            elif searchMap[x][y].onPath:
                print '+', ' ',
            else:
                print 0, ' ',
        print

    print
    print "Length of path:", len(finalPath)
    print "Total number of nodes expanded:", frontierCount
    if len(finalPath) > 0:
        print "Path: [",
        for node in finalPath:
            print "(%d, %d), " % (node.x, node.y),
        print "]"
    else:
        print "Path: no path could be found"
    print "Execution Time: %g seconds" % (end_time - start_time)
