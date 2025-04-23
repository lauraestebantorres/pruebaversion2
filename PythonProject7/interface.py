import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from graph import Graph, AddNode, AddSegment, DeleteNode, DeleteSegment, LoadGraphFromFile, SaveGraphToFile
from node import Node
from segment import Segment
from graph import reachable_nodes
from graph import FindShortestPath
from path import PlotPath




class GraphInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualization Tool")
        self.root.geometry("1000x750")

        self.graph = Graph()

        self.setup_ui()
        self.setup_figure()

    def setup_ui(self):
        # Frame principal
        self.controls_frame = tk.Frame(self.root, padx=10, pady=10)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.plot_frame = tk.Frame(self.root, padx=10, pady=10)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Título
        tk.Label(self.controls_frame, text="Graph Operations",
                 font=("Arial", 14, "bold")).pack(pady=10)

        # Botones de operaciones
        buttons = [
            ("Show Example Graph", self.show_example_graph),
            ("Show Custom Graph", self.show_custom_graph),
            ("Create Empty Graph", self.create_empty_graph),
            ("Load Graph from File", self.load_graph),
            ("Save Graph to File", self.save_graph),
            ("Add Node", self.add_node_interface),
            ("Delete Node", self.delete_selected_node),
            ("Add Segment", self.add_segment_interface),
            ("Delete Segment", self.delete_segment_interface),
            ("Show Node Neighbors", self.show_node_neighbors),
            ("Show Reachable Nodes", self.show_reachable_nodes),
            ("Show Shortest Path", self.show_shortest_path),

        ]

        for text, command in buttons:
            tk.Button(self.controls_frame, text=text, command=command,
                      width=20, padx=5, pady=5).pack(pady=5)

        # Lista de nodos
        tk.Label(self.controls_frame, text="Node Selection",
                 font=("Arial", 12, "bold")).pack(pady=(20, 5))

        self.node_listbox_frame = tk.Frame(self.controls_frame)
        self.node_listbox_frame.pack(fill=tk.X, pady=5)

        self.node_listbox = tk.Listbox(self.node_listbox_frame, height=10)
        self.node_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        node_scrollbar = tk.Scrollbar(self.node_listbox_frame)
        node_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.node_listbox.config(yscrollcommand=node_scrollbar.set)
        node_scrollbar.config(command=self.node_listbox.yview)

        # Lista de segmentos
        tk.Label(self.controls_frame, text="Segment Selection",
                 font=("Arial", 12, "bold")).pack(pady=(20, 5))

        self.segment_listbox_frame = tk.Frame(self.controls_frame)
        self.segment_listbox_frame.pack(fill=tk.X, pady=5)

        self.segment_listbox = tk.Listbox(self.segment_listbox_frame, height=10)
        self.segment_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        segment_scrollbar = tk.Scrollbar(self.segment_listbox_frame)
        segment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.segment_listbox.config(yscrollcommand=segment_scrollbar.set)
        segment_scrollbar.config(command=self.segment_listbox.yview)

        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        tk.Label(self.root, textvariable=self.status_var, bd=1,
                 relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    def setup_figure(self):
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect("button_press_event", self.on_canvas_click)

    def update_node_listbox(self):
        self.node_listbox.delete(0, tk.END)
        for node in self.graph.nodes:
            self.node_listbox.insert(tk.END, node.name)

    def update_segment_listbox(self):
        self.segment_listbox.delete(0, tk.END)
        for segment in self.graph.segments:
            self.segment_listbox.insert(tk.END, segment.id)

    def plot_full_graph(self):
        self.ax.clear()

        # Dibujar segmentos
        for segment in self.graph.segments:
            self.ax.plot([segment.origin.x, segment.destination.x],
                         [segment.origin.y, segment.destination.y], 'blue')

            # Flecha y costo
            midpoint_x = (segment.origin.x + segment.destination.x) / 2
            midpoint_y = (segment.origin.y + segment.destination.y) / 2
            self.ax.text(midpoint_x, midpoint_y, round(segment.cost, 2))

            self.ax.arrow(segment.origin.x, segment.origin.y,
                          segment.destination.x - segment.origin.x,
                          segment.destination.y - segment.origin.y,
                          head_width=0.5, head_length=0.5, fc='blue', ec='blue',
                          length_includes_head=True)

        # Dibujar nodos
        for node in self.graph.nodes:
            self.ax.plot(node.x, node.y, 'ko', markersize=5)
            self.ax.text(node.x, node.y, node.name,
                         horizontalalignment='left',
                         verticalalignment='bottom',
                         color='red', fontsize=7)

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title("Graph Visualization")
        self.ax.grid(True)
        self.canvas.draw()

    def plot_single_node_view(self, node_name):
        target_node = self.graph.GetNodeByName(node_name)
        if not target_node:
            return False

        self.ax.clear()

        # Dibujar todos los nodos
        for node in self.graph.nodes:
            self.ax.plot(node.x, node.y, 'ko', markersize=5)
            self.ax.text(node.x, node.y, node.name,
                         horizontalalignment='left',
                         verticalalignment='bottom',
                         color='red')

        # Resaltar vecinos
        for neighbor in target_node.neighbors:
            for segment in self.graph.segments:
                if (segment.origin == target_node and segment.destination == neighbor) or \
                        (segment.origin == neighbor and segment.destination == target_node):
                    self.ax.plot([segment.origin.x, segment.destination.x],
                                 [segment.origin.y, segment.destination.y], 'blue')

                    self.ax.arrow(segment.origin.x, segment.origin.y,
                                  segment.destination.x - segment.origin.x,
                                  segment.destination.y - segment.origin.y,
                                  head_width=0.5, head_length=0.5, fc='blue', ec='blue',
                                  length_includes_head=True)

                    midpoint_x = (segment.origin.x + segment.destination.x) / 2
                    midpoint_y = (segment.origin.y + segment.destination.y) / 2
                    self.ax.text(midpoint_x, midpoint_y, round(segment.cost, 2))

        self.ax.set_title(f"Neighbors of node '{node_name}'")
        self.ax.grid(True)
        self.canvas.draw()
        return True

    # Métodos de operaciones
    def create_example_graph(self):
        graph = Graph()

        # Nodos
        nodes = [
            Node("A", 0, 0),
            Node("B", 5, 5),
            Node("C", 10, 0),
            Node("D", 5, -5)
        ]

        # Segmentos
        segments = [
            ("1", "A", "B"),
            ("2", "B", "C"),
            ("3", "C", "D"),
            ("4", "D", "A"),
            ("5", "A", "C")
        ]

        for node in nodes:
            AddNode(graph, node)

        for seg_id, orig, dest in segments:
            AddSegment(graph, seg_id, orig, dest)

        return graph

    def create_custom_graph(self):
        graph = Graph()

        # Nodos
        nodes = [
            Node("P", 0, 0),
            Node("Q", 8, 6),
            Node("R", 10, 0),
            Node("S", 5, -5),
            Node("T", 15, 5)
        ]

        # Segmentos
        segments = [
            ("1", "P", "Q"),
            ("2", "Q", "R"),
            ("3", "R", "S"),
            ("4", "S", "P"),
            ("5", "P", "R"),
            ("6", "Q", "T"),
            ("7", "R", "T")
        ]

        for node in nodes:
            AddNode(graph, node)

        for seg_id, orig, dest in segments:
            AddSegment(graph, seg_id, orig, dest)

        return graph

    def show_example_graph(self):
        self.graph = self.create_example_graph()
        self.update_node_listbox()
        self.update_segment_listbox()
        self.plot_full_graph()
        self.status_var.set("Example graph loaded")

    def show_custom_graph(self):
        self.graph = self.create_custom_graph()
        self.update_node_listbox()
        self.update_segment_listbox()
        self.plot_full_graph()
        self.status_var.set("Custom graph loaded")

    def create_empty_graph(self):
        self.graph = Graph()
        self.update_node_listbox()
        self.update_segment_listbox()
        self.plot_full_graph()
        self.status_var.set("Empty graph created")

    def load_graph(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            self.graph = LoadGraphFromFile(file_path)
            self.update_node_listbox()
            self.update_segment_listbox()
            self.plot_full_graph()
            self.status_var.set(f"Graph loaded from {file_path}")

    def save_graph(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            SaveGraphToFile(self.graph, file_path)
            self.status_var.set(f"Graph saved to {file_path}")

    def add_node_interface(self):
        name = simpledialog.askstring("Node Name", "Enter node name:")
        if not name:
            return

        if self.graph.GetNodeByName(name):
            messagebox.showerror("Error", "Node name already exists")
            return

        x = simpledialog.askfloat("X Coordinate", "Enter X coordinate:")
        y = simpledialog.askfloat("Y Coordinate", "Enter Y coordinate:")

        if x is None or y is None:
            return

        AddNode(self.graph, Node(name, x, y))
        self.update_node_listbox()
        self.plot_full_graph()
        self.status_var.set(f"Node {name} added at ({x}, {y})")

    def delete_selected_node(self):
        selection = self.node_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No node selected")
            return

        node_name = self.node_listbox.get(selection[0])
        if DeleteNode(self.graph, node_name):
            self.update_node_listbox()
            self.update_segment_listbox()
            self.plot_full_graph()
            self.status_var.set(f"Node {node_name} deleted")
        else:
            messagebox.showerror("Error", "Failed to delete node")

    def add_segment_interface(self):
        origin = simpledialog.askstring("Origin", "Enter origin node name:")
        dest = simpledialog.askstring("Destination", "Enter destination node name:")
        seg_id = simpledialog.askstring("Segment ID", "Enter segment ID:")

        if not origin or not dest:
            return

        if not seg_id:
            seg_id = f"{origin}-{dest}"

        try:
            AddSegment(self.graph, seg_id, origin, dest)
            self.update_segment_listbox()
            self.plot_full_graph()
            self.status_var.set(f"Segment {seg_id} added")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add segment: {str(e)}")

    def delete_segment_interface(self):
        selection = self.segment_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No segment selected")
            return

        seg_id = self.segment_listbox.get(selection[0])
        if DeleteSegment(self.graph, seg_id):
            self.update_segment_listbox()
            self.plot_full_graph()
            self.status_var.set(f"Segment {seg_id} deleted")
        else:
            messagebox.showerror("Error", "Failed to delete segment")

    def show_node_neighbors(self):
        selection = self.node_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No node selected")
            return

        node_name = self.node_listbox.get(selection[0])
        if self.plot_single_node_view(node_name):
            self.status_var.set(f"Showing neighbors of {node_name}")
        else:
            messagebox.showerror("Error", "Node not found")

    def show_reachable_nodes(self):
        selection = self.node_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No node selected")
            return

        node_name = self.node_listbox.get(selection[0])
        node = self.graph.GetNodeByName(node_name)
        if not node:
            messagebox.showerror("Error", "Node not found")
            return

        reachable = reachable_nodes(self.graph, node)
        names = [n.name for n in reachable if n != node]

        if names:
            messagebox.showinfo("Reachable Nodes", f"From {node_name} you can reach: {', '.join(names)}")
        else:
            messagebox.showinfo("Reachable Nodes", f"No reachable nodes from {node_name}")

    def show_shortest_path(self):
        if len(self.graph.nodes) < 2:
            messagebox.showwarning("Warning", "Not enough nodes to compute path")
            return

        origin = simpledialog.askstring("Origin", "Enter origin node:")
        destination = simpledialog.askstring("Destination", "Enter destination node:")

        if not origin or not destination:
            return

        path = FindShortestPath(self.graph, origin, destination)

        if path:
            self.plot_full_graph()  # Redibuja grafo limpio
            PlotPath(self.graph, path, self.ax)  # Dibuja camino
            self.canvas.draw()

            cost = path.TotalCost()
            self.status_var.set(f"Path from {origin} to {destination}. Total cost: {round(cost, 2)}")
            messagebox.showinfo("Shortest Path", f"Path: {[n.name for n in path.nodes]}\nCost: {round(cost, 2)}")
        else:
            messagebox.showinfo("Result", f"No path found from {origin} to {destination}.")

    def on_canvas_click(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            name = simpledialog.askstring("Node Name", "Enter node name:")
            if name:
                if self.graph.GetNodeByName(name):
                    messagebox.showerror("Error", "Node name already exists")
                    return

                AddNode(self.graph, Node(name, x, y))
                self.update_node_listbox()
                self.plot_full_graph()
                self.status_var.set(f"Node {name} added at ({x:.2f}, {y:.2f})")




def main():
    root = tk.Tk()
    app = GraphInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()