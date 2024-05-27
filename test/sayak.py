import networkx as nx
import random
import matplotlib.pyplot as plt


class CommunityDetectionApp:
    def _init_(self):
        print("Welcome to Community Detection App")
        print("-----------------------------------")
        self.graphs = {
            "Karate Club": nx.karate_club_graph(),
            "Davis Southern Women": nx.davis_southern_women_graph(),
            "Les Misérables": nx.les_miserables_graph(),
            "Florentine Families": nx.florentine_families_graph()
        }
        self.selected_graph = None

    def display_menu(self):
        print("1. Select Dataset")
        print("2. Detect Communities")
        print("3. Enter Query")
        print("4. Exit")

    def select_dataset(self):
        print("\nSelect Dataset:")
        for i, dataset in enumerate(self.graphs.keys(), start=1):
            print(f"{i}. {dataset}")
        choice = int(input("Enter dataset number: "))
        if 1 <= choice <= len(self.graphs):
            self.selected_graph = list(self.graphs.values())[choice - 1]
            print(f"Dataset selected: {list(self.graphs.keys())[choice - 1]}")
        else:
            print("Invalid choice. Please try again.")

    def detect_communities(self):
        if self.selected_graph:
            communities = self.label_propagation_community_detection(self.selected_graph)
            self.visualize_communities(self.selected_graph, communities)
        else:
            print("Please select a dataset first.")

    def label_propagation_community_detection(self, graph):
        communities = list(nx.algorithms.community.label_propagation_communities(graph))
        return communities

    def visualize_communities(self, graph, communities):
        pos = nx.spring_layout(graph)
        plt.figure(figsize=(10, 8))
        nx.draw(graph, pos, with_labels=True, node_color="#A0CBE2", node_size=700)
        cmap = plt.cm.tab10
        colors = [cmap(i) for i in range(len(communities))]
        for color, community in zip(colors, communities):
            nx.draw_networkx_nodes(graph, pos, nodelist=list(community), node_color=color, node_size=500)
        plt.title("Community Detection using Label Propagation Algorithm")
        plt.show()

    def enter_query(self):
        query = input("\nEnter your query: ")
        if query:
            print(f"\nQuery entered: {query}")
        else:
            print("No query entered.")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.select_dataset()
            elif choice == '2':
                self.detect_communities()
            elif choice == '3':
                self.enter_query()
            elif choice == '4':
                print("Exiting Community Detection App. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


# Create an instance of the CommunityDetectionApp and run it
app = CommunityDetectionApp()
app.run()