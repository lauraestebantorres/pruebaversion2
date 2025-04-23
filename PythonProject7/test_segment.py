from node import *
from segment import *
# Importing the Node and Segment classes. These classes define the behavior
# of nodes and segments in the graph, allowing us to create and manipulate them.


# Creating instances of Node with names and coordinates
n1 = Node("A", 1, 20)  # Node "A" at coordinates (1, 20)
n2 = Node("B", 8, 17)  # Node "B" at coordinates (8, 17)
n3 = Node("C", 15, 20) # Node "C" at coordinates (15, 20)


# Creating a Segment connecting n1 (origin) to n2 (destination)
segment = Segment(n1, n2)


# Printing the details of the segment
print(f"Origen:{segment.origin.name}")  # Displays the name of the origin node (n1)
print(f"Destí: {segment.destination.name}")  # Displays the name of the destination node (n2)
print(f"Cost: {segment.cost}")  # Displays the cost of the segment, which is the Euclidean distance between n1 and n2
