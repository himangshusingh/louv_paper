from matplotlib import pyplot as plt
import networkx as nx


# Define the nodes as a list
nodes = list(range(1, 11))

# Create a dictionary to store connections for each node
connections = {node: [] for node in nodes}

# Add bidirectional connections between each node pair
for i in nodes:
    for j in nodes:
        if i != j:
            connections[i].append(j)
            connections[j].append(i)

# Print the connections dictionary
print(connections)



# Create a NetworkX graph object
G = nx.Graph()

# Add nodes and edges based on the connections dictionary
for node, neighbors in connections.items():
    G.add_node(node)
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# Draw the graph
nx.draw_circular(G, with_labels=True)
plt.show()
