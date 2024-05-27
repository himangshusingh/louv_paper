
### Louvain Algorithm Strategy

The Louvain algorithm is a popular method for detecting communities in large networks. It is designed to optimize the modularity of a partition of the network. The algorithm proceeds in two main phases that are repeated iteratively:

1. **Modularity Maximization**: 
   - Initially, each node is assigned to its own community.
   - For each node, the algorithm evaluates the gain in modularity that would result from moving the node to the community of each of its neighbors.
   - The node is then placed in the community for which this gain is maximum (if positive).
   - This process is applied repeatedly and iteratively for all nodes until no further improvement in modularity can be achieved.

2. **Community Aggregation**: 
   - Once the first phase is complete, a new network is built. In this new network, nodes represent the communities found during the first phase.
   - The weights of the links between the new nodes are given by the sum of the weight of the links between nodes in the corresponding two communities.
   - The algorithm then applies the first phase again to this new network.

These two phases are repeated until a maximum of modularity is achieved and no further improvements can be made. The result is a hierarchy of communities, where nodes are grouped in an optimal way according to the modularity measure.


> [!NOTE] IMP
> Relevant code snippets for these phases are found in the `generate_dendrogram` function for the iterative process and the `modularity` function for calculating the modularity of a given partition



##  The iterative process of community detection and aggregation:

```python
def generate_dendrogram(graph,
                        part_init=None,
                        weight='weight',
                        resolution=1.,
                        randomize=None,
                        random_state=None):
    ...
    status_list = list()
    __one_level(current_graph, status, weight, resolution, random_state)
    new_mod = __modularity(status, resolution)
    partition = __renumber(status.node2com)
    status_list.append(partition)
    mod = new_mod
    current_graph = induced_graph(partition, current_graph, weight)
    status.init(current_graph, weight)

    while True:
        __one_level(current_graph, status, weight, resolution, random_state)
        new_mod = __modularity(status, resolution)
        if new_mod - mod < __MIN:
            break
        partition = __renumber(status.node2com)
        status_list.append(partition)
        mod = new_mod
        current_graph = induced_graph(partition, current_graph, weight)
        status.init(current_graph, weight)
    return status_list[:]
```


## Modularity calculation for a partition:

```python
def modularity(partition, graph, weight='weight'):
    ...
    inc = dict([])
    deg = dict([])
    links = graph.size(weight=weight)
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph:
        com = partition[node]
        deg[com] = deg.get(com, 0.) + graph.degree(node, weight=weight)
        for neighbor, datas in graph[node].items():
            edge_weight = datas.get(weight, 1)
            if partition[neighbor] == com:
                if neighbor == node:
                    inc[com] = inc.get(com, 0.) + float(edge_weight)
                else:
                    inc[com] = inc.get(com, 0.) + float(edge_weight) / 2.

    res = 0.
    for com in set(partition.values()):
        res += (inc.get(com, 0.) / links) - \
               (deg.get(com, 0.) / (2. * links)) ** 2
    return res
```


This strategy allows the Louvain algorithm to efficiently find high-quality community structures in large networks.