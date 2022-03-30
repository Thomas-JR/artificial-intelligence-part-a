"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching
"""

# python -m search input.json

# Libraries
import heapq
import json
import sys

from collections import defaultdict
from numpy import Infinity

from search.util import print_board, print_coordinate #print_coordinate

MOVES = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]

# Determine shortest path from start to end nodes on game board
def main():
    # Open file
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
    blockedPositions = set()
    for entry in inputBoard:
        blockedPositions.add((entry[1], entry[2]))
    
    # Perform A* algorithm, returning the list of nodes from start to goal
    nodes = aStar(blockedPositions, start, goal, n)
    if nodes == None:
        return
    print(len(nodes))
    for node in nodes:
        print(node)

# A* function
def aStar(explored, start, goal, n):
    # keep track of all nodes parents
    parents = defaultdict(tuple)
    
    def defaultValue():
        return sys.maxsize

    # g score
    gCosts = defaultdict(defaultValue)
    gCosts[start] = 0

    # f score
    fCosts = dict()
    fCosts[start] = h(start, goal)
    for block in explored:
        fCosts[block] = "-----"
    
    # heap has O(log(n)) pop performance
    frontier = []
    # set has O(1) search performance
    frontierSet = set()
    
    heapq.heappush(frontier, (0, start))
    frontierSet.add(start)

    # Expand on lowest costing
    while len(frontier) > 0:
        # Get the node with the min f cost from the heap
        child = heapq.heappop(frontier)[1]
        frontierSet.remove(child)
        print_board(n, fCosts)

        # Return the path from the origin to the target
        if child == goal:
            return reconstruct(parents, goal)

        # Go through all neighbours, updating node distances and pushing to the queue & set
        for neighbour in validNeighbours(child, n):
            # + 1 for distance from current node to new node
            neighbourGCost = gCosts[child] + 1
            if neighbour not in explored and neighbourGCost < gCosts[neighbour]:
                parents[neighbour] = child
                gCosts[neighbour] = neighbourGCost
                fCosts[neighbour] = neighbourGCost + h(neighbour, goal)
                
                # Could add a set of elems in frontier as well to avoid this check time complexity
                if neighbour not in frontierSet:
                    heapq.heappush(frontier, (fCosts[neighbour], neighbour))
                    frontierSet.add(neighbour)
    
    return None

def reconstruct(parents, goal):
    path = [goal]
    while parents[path[-1]]:
        path.append(parents[path[-1]])
    return path[::-1]

def validNeighbours(current, n):
    out = []
    for move in MOVES:
        newPos = (current[0] + move[0], current[1] + move[1])
        if inBorders(newPos, n):
            out.append(newPos)
    return out

def inBorders(pos, n):
    return 0 <= pos[0] < n and 0 <= pos[1] < n

# Returns the manhatten distance between cur and goal
def h(cur, goal):
    dx = goal[0]-cur[0]
    dy = goal[1]-cur[1]
    if (dx < 0 and dy < 0) or (dx >= 0 and dy >= 0):
        return abs(dx + dy)
    else:
        return max(abs(dx), abs(dy))