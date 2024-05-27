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

