"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

Find lowest cost path from `start` to `goal` coordinates on Cachex board of size `n` while avoiding already blocked cells
"""

''' THINGS TO DELETE BEFORE UPLOADING
    - Indicated lines in main.py
    - util.py
    - _pycache (?)
    - _main_.py (?)
    - .gitignore
    - input.json
    - sample_output.txt
    - This comment

    CHECK WITH TOM
    - Question about frontier
    - Could add set of elemetns in frontier
    - Moved block check to valid neighbours functions

    MISC
    - Test
    - Test cases
    - Upload
    - Report
'''

# python -m search input.json # DELETE BEFORE UPLOADING

# Libraries
import heapq
import json
import sys
from collections import defaultdict
from search.util import print_board, print_coordinate # REMOVE LINE BEFORE UPLOADING

# Constants
MOVES = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]

'''Find lowest cost path from `start` to `goal` coordinates on Cachex board of size `n` while avoiding blocked cells'''
def main():

    # Open file containing board size, occupied cells and end coordinates
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # Read file contents
    n = int(data["n"])
    inputBoard = data["board"]
    start = tuple(data["start"])
    goal = tuple(data["goal"])

    # Initialise board
    blockedCells = set()
    for cell in inputBoard:
        blockedCells.add((cell[1], cell[2]))
    
    # Perform A* search and display found path
    path = aStar(blockedCells, start, goal, n)
    
    # IS THIS NECESSARY?
    if path == None:
        return
    
    print(len(path))
    for node in path:
        print(f"({node[0]},{node[1]})")

'''Optimally determine lowest cost path from `start` to `goal` by exhausting all possible best paths from evaluation function'''
def aStar(blockedCells, start, goal, n):

    # Store parent node for each explored child
    parents = defaultdict(tuple)

    # Store g(x) (total cost of path from `start`) for each explored node
    gCosts = defaultdict(lambda:sys.maxsize)
    gCosts[start] = 0

    # Store f(x) = g(x) + h(x) for each explored node
    fCosts = dict()
    fCosts[start] = h(start, goal)

    # CHNAGE BEFORE UPLOADING
    for block in blockedCells:
        fCosts[block] = "-----"
    # CHNAGE BEFORE UPLOADING
    
    # Store priortity queue containing expanded but unexplored nodes with associated f(x)
    frontier = []
    frontierSet = set()
    heapq.heappush(frontier, (0, start))
    frontierSet.add(start)

    # Exhaust all possible best paths
    while len(frontier) > 0:

        # Select node from frontier with lowest f(x)
        node = heapq.heappop(frontier)[1]
        frontierSet.remove(node)
        print_board(n, fCosts) # REMOVE BEFORE UPLOADING

        # Return lowest cost path once applicable
        if node == goal:
            return reconstructPath(parents, goal)

        # Iterate through valid neighbours of current node while updating distances and frontier set accordingly
        for neighbour in validNeighbours(node, n):

            # Record parent, lowest g(x) and f(x) of each neighbour
            neighbourGCost = gCosts[node] + 1
            if neighbour not in blockedCells and neighbourGCost < gCosts[neighbour]:
                parents[neighbour] = node
                gCosts[neighbour] = neighbourGCost
                fCosts[neighbour] = neighbourGCost + h(neighbour, goal)
                
                # Could add a set of elems in frontier as well to avoid this check time complexity
                if neighbour not in frontierSet:
                    heapq.heappush(frontier, (fCosts[neighbour], neighbour))
                    frontierSet.add(neighbour)

    # Return nothing if no path exists from `start` to `goal`
    return None

'''Reconstruct order of cells in determined optimal path from `start` to `goal`'''
def reconstructPath(parents, goal):
    path = [goal]
    while parents[path[-1]]:
        path.append(parents[path[-1]])
    return path[::-1]

'''Return list of cells that can be traversed from current cell'''
def validNeighbours(currentCell, n):
    cells = []
    for move in MOVES:
        newCell = (currentCell[0] + move[0], currentCell[1] + move[1])
        if inBorders(newCell, n):
            cells.append(newCell)
    return cells

'''Determine whether generated cell lies within boundaries of Cachex board'''
def inBorders(cell, n):
    return 0 <= cell[0] < n and 0 <= cell[1] < n

'''Calculate Manhattan distance between current cell and goal cell'''
def h(currentCell, goal):
    x = goal[0] - currentCell[0]
    y = goal[1] - currentCell[1]
    if (x < 0 and y < 0) or (x >= 0 and y >= 0):
        return abs(x + y)
    else:
        return max(abs(x), abs(y))