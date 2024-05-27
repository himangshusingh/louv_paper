import louvain as comm_dec

def louvain(G):
    # Use the community_louvain package to find the best partition
    partition = comm_dec.best_partition(G)
    
    # Convert partition format to a list of sets for consistency
    communities = {}
    for node, comm_id in partition.items():
        communities.setdefault(comm_id, set()).add(node)
    
    # Convert the communities dict to a list of sets
    final_communities = list(communities.values())
    
    return final_communities