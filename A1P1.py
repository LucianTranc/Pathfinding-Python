# Lucian Tranc
# 1045249
from queue import PriorityQueue

# Node class for tree structure
class Node():
    def __init__(self, state, heuristic, depth, pathCost):
        self.state = state          # The state of the Node (the letter label in our case)
        self.pathCost = pathCost    # The total path cost of reaching this node
        self.heuristic = heuristic  # The heuristic value assigned to this node
        self.depth = depth          # The depth of the node in the tree
        self.parentNode = None      # A reference to the parent Node if it has one
        self.parentEdge = None      # The edge that led to this node
    def __lt__(self, Node2): return self.state < Node2.state  # Overriding the < operation to allow Nodes to be compared
    def __gt__(self, Node2): return self.state > Node2.state  # Overriding the > operation to allow Nodes to be compared
    def __eq__(self, Node2): return self.state == Node2.state # Overriding the = operation to allow Nodes to be compared

# Problem class containing all information about the problem
class Problem():
    def __init__(self, adjacency_list, heuristics, initial, goal):
        self.adjacency_list = adjacency_list    # A list of all edges in the graph and their weights
        self.heuristics = heuristics            # A list of all the heuristic values of the nodes
        self.initial = initial                  # The starting state
        self.goal = goal                        # The goal state

# a function that prints out the path of a node back to the starting state
def Retrace(node, start):
    path = [] # a list of the states in the path
    while not node is None:
        path.append(node.state)
        node = node.parentNode
    for i in range(len(path) - 1, -1, -1): # loop over the list in reverse order and print
        if (i != 0): print(path[i], end = "-")
        else: print(path[i])

# Function that expands the node in a given problem, creates the needed child nodes and yeild returns
def Expand(problem, node):
    if node.state in problem.adjacency_list:
        for e in problem.adjacency_list[node.state]:
            newNode = Node(e[0], problem.heuristics[e[0]], node.depth + 1, node.pathCost + e[1])
            newNode.parentNode = node
            newNode.parentEdge = e[1]
            yield newNode
    else: yield

# The following 5 functions are priority functions that return the priority value needed for
# the priority queue for each type of searching algorithm
# These functions are passed as pointers to the TreeSearch function
def BFSPriority(node): return node.depth
def DFSPriority(node): return -node.depth
def UCSPriority(node): return node.pathCost
def GBFSPriority(node): return node.heuristic
def AStarPriority(node): return node.heuristic + node.pathCost

# Tree search function
def TreeSearch(problem, algoPriority, algoName):
    print(algoName) # print the name of the algorithm currently running
    node = Node(problem.initial, problem.heuristics[problem.initial], 0, 0) # create root node
    frontier = PriorityQueue() # initialize priority queue
    frontier.put((algoPriority(node), node)) # place the root node in the queue
    reached = [] # initialize list of nodes that have been reached
    while not frontier.empty(): # while there are nodes in the frontier
        while (node.state in reached): # keep getting nodes from the frontier until one is not in reached list
            if (frontier.empty()): break # check for fail state
            node = frontier.get()[1]
        reached.append(node.state) # add node to reached list
        if (node.state == problem.goal): # check for goal state
            Retrace(node, problem.initial) # retrace path to start
            return
        for child in Expand(problem, node): # for every child of the node
            if child is None: continue # if there are no children continue
            if not child.state in reached: # if the child is not in reached add it to frontier
                frontier.put((algoPriority(child), child))
    print("No path found") # failure message

adjacency_list = {
    'S': [('A', 3), ('B', 2), ('C', 5)],
    'A': [('G', 2), ('C', 3)],
    'B': [('A', 4), ('D', 6)],
    'C': [('B', 4), ('H', 3)],
    'D': [('E', 2), ('F', 3)],
    'E': [('F', 5)],
    'G': [('E', 5), ('D', 4)],
    'H': [('A', 4), ('D', 4)]
}

heuristics = {'A': 8, 'B': 9, 'C': 7, 'D': 4, 'E': 3, 'F': 0, 'G': 6, 'H': 6, 'S': 10}
problem = Problem(adjacency_list, heuristics, 'S', 'F')

TreeSearch(problem, BFSPriority, "BFS")
TreeSearch(problem, DFSPriority, "DFS")
TreeSearch(problem, UCSPriority, "UCS")
TreeSearch(problem, GBFSPriority, "Greedy BFS")
TreeSearch(problem, AStarPriority, "A*")