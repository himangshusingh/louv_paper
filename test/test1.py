import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import networkx as nx
import community.community_louvain as community_louvain  # Correct import for Louvain method
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CommunityDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Community Detection App")

        # Create a frame for dataset selection
        self.dataset_frame = ttk.LabelFrame(root, text="Select Dataset")
        self.dataset_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Dataset selection dropdown
        self.dataset_label = ttk.Label(self.dataset_frame, text="Choose Dataset:")
        self.dataset_label.grid(row=0, column=0, padx=5, pady=5)
        self.datasets = ["Karate Club", "Davis Southern Women", "Les Misérables", "Florentine Families", "Citation",
                         "Facebook", "Zachary's Karate Club", "Custom"]
        self.dataset_combobox = ttk.Combobox(self.dataset_frame, values=self.datasets, state="readonly")
        self.dataset_combobox.current(0)
        self.dataset_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Dataset selection button
        self.select_dataset_button = ttk.Button(self.dataset_frame, text="Select File", command=self.select_dataset_file)
        self.select_dataset_button.grid(row=0, column=2, padx=5, pady=5)

        # Algorithm selection dropdown
        self.algorithm_frame = ttk.LabelFrame(root, text="Select Algorithm")
        self.algorithm_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.algorithm_label = ttk.Label(self.algorithm_frame, text="Choose Algorithm:")
        self.algorithm_label.grid(row=0, column=0, padx=5, pady=5)
        self.algorithms = ["Louvain Method", "Label Propagation"]
        self.algorithm_combobox = ttk.Combobox(self.algorithm_frame, values=self.algorithms, state="readonly")
        self.algorithm_combobox.current(0)
        self.algorithm_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Detect communities button
        self.detect_button = ttk.Button(root, text="Detect Communities", command=self.detect_communities)
        self.detect_button.pack(pady=5)

        # Query processing section
        self.query_label = ttk.Label(root, text="Enter Query:")
        self.query_label.pack(pady=5)

        self.query_entry = ttk.Entry(root, width=40)
        self.query_entry.pack(pady=5)

        self.process_query_button = ttk.Button(root, text="Process Query", command=self.process_query)
        self.process_query_button.pack(pady=5)

        # Output canvas for visualization
        self.output_canvas = FigureCanvasTkAgg(plt.figure(figsize=(8, 6)), master=root)
        self.output_canvas.get_tk_widget().pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def select_dataset_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.dataset_combobox.set("Custom")
            self.custom_dataset = file_path

    def detect_communities(self):
        selected_dataset = self.dataset_combobox.get()
        selected_algorithm = self.algorithm_combobox.get()

        graph = self.load_dataset(selected_dataset)
        if not graph:
            return

        partition = self.apply_algorithm(graph, selected_algorithm)
        if partition is not None:
            self.visualize_communities(graph, partition)

    def load_dataset(self, dataset):
        if dataset == "Custom" and hasattr(self, "custom_dataset"):
            file_path = self.custom_dataset
            try:
                graph = nx.read_edgelist(file_path)
                return graph
            except FileNotFoundError:
                messagebox.showerror("Error", f"File '{file_path}' not found.")
                return None
        else:
            try:
                if dataset == "Karate Club":
                    return nx.karate_club_graph()
                elif dataset == "Davis Southern Women":
                    return nx.davis_southern_women_graph()
                elif dataset == "Les Misérables":
                    return nx.les_miserables_graph()
                elif dataset == "Florentine Families":
                    return nx.florentine_families_graph()
                elif dataset == "Citation":
                    return nx.read_edgelist("citation_graph.txt")
                elif dataset == "Facebook":
                    return nx.read_edgelist("facebook_combined.txt")
                elif dataset == "Zachary's Karate Club":
                    return nx.karate_club_graph()
            except FileNotFoundError:
                messagebox.showerror("Error", f"File for dataset '{dataset}' not found.")
                return None

    def apply_algorithm(self, graph, algorithm):
        if algorithm == "Louvain Method":
            return community_louvain.best_partition(graph)
        elif algorithm == "Label Propagation":
            partition = nx.algorithms.community.label_propagation.label_propagation_communities(graph)
            return {node: idx for idx, com in enumerate(partition) for node in com}
        return None

    def visualize_communities(self, graph, partition):
        plt.clf()
        pos = nx.spring_layout(graph)
        nx.draw_networkx(graph, pos, node_color=list(partition.values()), cmap=plt.cm.tab20, with_labels=True,
                         node_size=300)
        plt.title("Communities Detected")
        self.output_canvas.draw()

    def process_query(self):
        query = self.query_entry.get().lower()  # Convert query to lowercase for case-insensitive matching
        if query:
            # Clear previous content on the canvas
            plt.clf()

            # Parse the query to extract dataset and algorithm information
            dataset_keywords = ["karate", "davis", "women", "les", "miserables", "florentine", "citation", "facebook", "zachary"]
            algorithm_keywords = ["louvain", "label propagation"]

            dataset = None
            algorithm = None

            for keyword in dataset_keywords:
                if keyword in query:
                    dataset = keyword
                    break

            for keyword in algorithm_keywords:
                if keyword in query:
                    algorithm = keyword
                    break

            if not dataset:
                messagebox.showerror("Error", "Dataset not found in query.")
                return

            if not algorithm:
                messagebox.showerror("Error", "Algorithm not found in query.")
                return

            # Load selected dataset
            dataset_map = {
                "karate": "Karate Club",
                "davis": "Davis Southern Women",
                "women": "Davis Southern Women",
                "les": "Les Misérables",
                "miserables": "Les Misérables",
                "florentine": "Florentine Families",
                "citation": "Citation",
                "facebook": "Facebook",
                "zachary": "Zachary's Karate Club"
            }
            dataset = dataset_map.get(dataset, None)
            graph = self.load_dataset(dataset)
            if not graph:
                return

            # Perform community detection
            partition = self.apply_algorithm(graph, algorithm)
            if partition is not None:
                self.visualize_communities(graph, partition)

# Create the main application window
root = tk.Tk()
app = CommunityDetectionApp(root)
root.mainloop()