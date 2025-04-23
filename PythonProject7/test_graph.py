from graph import Graph, AddNode, AddSegment, SaveGraphToFile, FindShortestPath, LoadGraphFromFile, Plot, PlotNode, GetClosest
from node import Node

# ------- Grafo oficial del proyecto -------
def CreateGraph_1():
    G = Graph()
    AddNode(G, Node("A", 1, 20))
    AddNode(G, Node("B", 8, 17))
    AddNode(G, Node("C", 15, 20))
    AddNode(G, Node("D", 18, 15))
    AddNode(G, Node("E", 2, 4))
    AddNode(G, Node("F", 6, 5))
    AddNode(G, Node("G", 12, 12))
    AddNode(G, Node("H", 10, 3))
    AddNode(G, Node("I", 19, 1))
    AddNode(G, Node("J", 13, 5))
    AddNode(G, Node("K", 3, 15))
    AddNode(G, Node("L", 4, 10))
    AddSegment(G, "AB", "A", "B")
    AddSegment(G, "AE", "A", "E")
    AddSegment(G, "AK", "A", "K")
    AddSegment(G, "BA", "B", "A")
    AddSegment(G, "BC", "B", "C")
    AddSegment(G, "BF", "B", "F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DG", "D", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "FG", "F", "G")  # este segmento para que F conozca a G
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JI", "J", "I")
    AddSegment(G, "KA", "K", "A")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LK", "L", "K")
    AddSegment(G, "LF", "L", "F")
    return G

# ------- Pruebas -------
print("Creando el grafo...")
G = CreateGraph_1()
SaveGraphToFile(G, "grafo_oficial.txt")
print("Grafo guardado como 'grafo_oficial.txt'")

# ------- Prueba: Camino más corto -------
print("\nBuscando camino más corto entre F y D...")
path = FindShortestPath(G, "F", "D")

if path:
    print("Camino más corto:", [n.name for n in path.nodes])
    print(" Coste total:", round(path.TotalCost(), 2))
else:
    print(" No se encontró camino.")
