from node import *
# Importing all definitions and functions from the 'node' module.
# This includes the Node class and the Distance function, which calculates
# the Euclidean distance between two nodes.


class Segment():
   # This class represents a segment in a graph, connecting two nodes (n1 and n2).
   def __init__(self, n1, n2):
       # Initializes a Segment object with the origin node, destination node, and cost.
       # n1: Origin node of the segment.
       # n2: Destination node of the segment.
       self.origin = n1  # The starting point of the segment (node n1).
       self.destination = n2  # The endpoint of the segment (node n2).
       self.cost = Distance(n1, n2)
       # The cost of the segment, calculated as the Euclidean distance
       # between the origin (n1) and destination (n2) nodes using the
       # Distance function from the 'node' module.


