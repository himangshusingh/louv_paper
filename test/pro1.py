import json
import networkx as nx

def load_dblp_citation_graph(path_to_dblp_json):
    G = nx.DiGraph()  # Use DiGraph if you care about the direction of citations
    with open(path_to_dblp_json, 'r') as f:
        data = json.load(f)  # Load the entire JSON array
        for entry in data:
            node_id = entry.get('Id')
            source = entry.get('Source')
            target = entry.get('Target')
            if node_id is None or source is None or target is None:
                continue  # Skip entries with missing information
            G.add_node(node_id, **{k: entry[k] for k in entry if k not in ['Id', 'Source', 'Target']})
            G.add_edge(source, target)  # Add an edge from source to target
    return G

input_path = 'src/dataset/dataset.json'


# Load the directed graph from JSON
directed_graph = load_dblp_citation_graph(input_path)

# Convert to an undirected graph
undirected_graph = directed_graph.to_undirected()

# Convert the graph to a JSON format
graph_json = nx.node_link_data(undirected_graph)

# Save the graph to a JSON file
with open('undirected_graph.json', 'w') as f:
    json.dump(graph_json, f, indent=4)

