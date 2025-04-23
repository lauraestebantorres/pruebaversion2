from node import Distance

class Path:
    def __init__(self, nodes=None):
        self.nodes = list(nodes) if nodes else []

    def AddNodeToPath(self, node):
        self.nodes.append(node)

    def ContainsNode(self, node):
        return node in self.nodes

    def CostToNode(self, node):
        if node not in self.nodes:
            return -1
        index = self.nodes.index(node)
        cost = 0
        for i in range(index):
            cost += Distance(self.nodes[i], self.nodes[i + 1])
        return cost

    def TotalCost(self):
        return self.CostToNode(self.nodes[-1]) if self.nodes else 0

    def LastNode(self):
        return self.nodes[-1] if self.nodes else None

def PlotPath(graph, path, ax):
    for i in range(len(path.nodes) - 1):
        n1 = path.nodes[i]
        n2 = path.nodes[i + 1]
        ax.plot([n1.x, n2.x], [n1.y, n2.y], 'green', linewidth=2)

        # Mostrar coste del segmento
        midpoint_x = (n1.x + n2.x) / 2
        midpoint_y = (n1.y + n2.y) / 2
        ax.text(midpoint_x, midpoint_y, round(Distance(n1, n2), 2), color="green", fontsize=8)

    # Marcar los nodos del camino
    for node in path.nodes:
        ax.plot(node.x, node.y, 'go', markersize=7)
        ax.text(node.x, node.y, node.name, color="green", fontsize=9)
