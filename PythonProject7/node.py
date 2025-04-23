import math
# The math module is imported to use mathematical functions, such as calculating the square root.


class Node:
   # This class represents a node with a name, coordinates (x and y), and a list of neighbors.
   def __init__(self, name, x, y):
       # Initializes the attributes of the Node class.
       # name: A string representing the name of the node.
       # x, y: Floats representing the coordinates of the node.
       # neighbors: An empty list initialized to store neighboring nodes.
       self.name = name
       self.x = x
       self.y = y
       self.neighbors = []


def AddNeighbor(n1, n2):
   # Adds node 'n2' to the list of neighbors of node 'n1'.
   # Returns False if 'n2' is already in the neighbors list, avoiding duplicate entries.
   # Returns True if 'n2' was successfully added as a neighbor.
   if n2 in n1.neighbors:  # Checks if 'n2' is already in 'n1's neighbor list.
       return False  # If it is, no action is taken, and False is returned.
   else:
       n1.neighbors.append(n2)  # Adds 'n2' to 'n1's neighbors list.
       return True  # Returns True to indicate the operation was successful.


def Distance(n1, n2):
   # Calculates the Euclidean distance between two nodes, 'n1' and 'n2'.
   # Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2), which measures the straight-line distance between two points in 2D space.
   return math.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2)
