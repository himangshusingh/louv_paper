import json
import networkx as nx

def convert_to_undirected_with_nodes_and_edges(input_json_path, output_json_path):
    with open(input_json_path, 'r') as file:
        data = json.load(file)
    
    G = nx.DiGraph()
    for entry in data:
        G.add_edge(entry['Source'], entry['Target'])
    
    undirected_graph = G.to_undirected()
    unique_nodes = list(undirected_graph.nodes())
    edges = list(undirected_graph.edges())

    output_data = {
        "Nodes": unique_nodes,
        "Edges": [{"Source": edge[0], "Target": edge[1]} for edge in edges]
    }
    
    with open(output_json_path, 'w') as file:
        json.dump(output_data, file, indent=4)

# Example usage
convert_to_undirected_with_nodes_and_edges('src/dataset/undirected.json', 'undirected_02.json')