"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching
"""

# python -m search input.json

# Libraries
from asyncio import queues
from collections import defaultdict
import json
from queue import PriorityQueue

from numpy import Infinity
from search.util import print_board, print_coordinate #print_coordinate
import sys

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
    startState = set()
    for entry in inputBoard:
        startState.add((entry[1], entry[2]))
    
    # Perform A* algorithm, returning the list of nodes from start to goal
    nodes = aStar(startState, start, goal, n)
    print(len(nodes))
    for node in nodes:
        print(node)

# A* function
def aStar(blockedPositions, start, goal, n):
    # keep track of all nodes parents
    parents = defaultdict(tuple)

    # default all nodes distances to infinity
    def defaultValue():
        return sys.maxint

    # g score
    gCosts = defaultdict(defaultValue)
    gCosts[start] = 0

    # f score
    fCosts = defaultdict(defaultValue)
    fCosts[start] = 0
    for block in blockedPositions:
        fCosts[block] = "-----"

    # heap has O(1) pop performance
    queue = PriorityQueue()
    # set has O(1) search performance
    queueSet = set()
    
    queue.put(start, 0)
    queueSet.add(start)

    # expand on lowest costing
    while not queue.empty():
        # Get the top node in the queue
        print_board(n, fCosts)
        current = queue.get()
        queueSet.remove(current)

        # Return the path from the origin to the target
        if current == goal:
            return reconstruct(parents, goal)

        # Go through all neighbours, updating node distances and pushing to the queue & set
        for neighbour in validNeighbours(blockedPositions, queueSet, current, n):
            # + 1 for distance from current node to new node
            newCostFromOrigin = gCosts[current] + 1
            if neighbour not in fCosts or newCostFromOrigin < gCosts[neighbour]:
                parents[neighbour] = current
                gCosts[neighbour] = newCostFromOrigin
                fCosts[neighbour] = newCostFromOrigin + h(current, goal)
                
                # This check is O(n) which is poopy
                # Could add a set of elems in frontier as well to avoid this check time complexity
                if neighbour not in queueSet:
                    queue.put(neighbour, fCosts[neighbour])
                    queueSet.add(neighbour)
    
    return None


def reconstruct(parents, goal):
    path = [goal]
    while parents[path[-1]]:
        path.append(parents[path[-1]])
    return path[::-1]

def validNeighbours(blockedPositions, queueSet, current, n):
    moves = [(-1, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, 0)]
    out = []
    for move in moves:
        cur = tuple(map(sum, zip(current, move)))
        if cur not in queueSet and cur not in blockedPositions and inBorders(cur, n):
            out.append(cur)
    return out

def inBorders(pos, n):
    return 0 <= pos[0] < n and 0 <= pos[1] < n

def h(cur, goal):
    return abs(cur[0]-goal[0]) + abs(cur[1] - goal[1])



# class State:
#     def __init__(self, visited, costs):
#         self.visited = visited
#         self.costs = costs
    
#     def canMove(self, pos):
#         return self.visited.contains(pos)

#     def getNeighbours(graph, current):

            
#     def i


# def move(board, parent, pos):
#     for relativeMove in possibleMoves:
#         newPos = (pos[0] + relativeMove[0], pos[1] + relativeMove[1])
#         if isValidMove(board[(newPos[0], newPos[1])])
        
        
#         not board[(newPos[0], newPos[1])]:
#             move(parent, )
#     return




# def isValidMove(board, parent, pos)):
    




'''

- create functions for each action
- create list of actions
- create function to validate move
- create graph traversal algorithm
- create list for storing nodes
- print final board
- make heuristic function
- make cost path function
- make goal tester
- for each node store state, actions, cost to there and heuristic
- goal counter




- run a star from start node
- check all possible moves
- make all possible moves

make move:
- keep track of parent
- 

'''