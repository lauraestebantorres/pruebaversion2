from node import Node
from path import Path

n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)
n3 = Node("C", 6, 8)

p = Path([n1])
p.AddNodeToPath(n2)
p.AddNodeToPath(n3)

print("Contiene B:", p.ContainsNode(n2))  # True
print("Coste hasta C:", p.CostToNode(n3))  # 10.0
print("Coste total:", p.TotalCost())  # 10.0
print("Último nodo:", p.LastNode().name)  # C
