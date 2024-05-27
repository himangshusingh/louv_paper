
The mathematical expression for modularity, as implemented in the Louvain package, can be derived from the `modularity` function in the `comm_dec.py`. Here's the relevant code snippet:


```python
#code from comm_dec.py


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


This function calculates the modularity of a partition of a graph. The modularity is given by the formula:
$$
Q = \sum_{c \in C} \left[ \frac{inc_c}{m} - \left( \frac{deg_c}{2m} \right)^2 \right]
$$
where:
- \(Q\) is the modularity of the partition,
- \(C\) is the set of communities,
- \(inc_c\) is the sum of the weights of the links inside community \(c\),
- \(deg_c\) is the sum of the degrees of the nodes in community \(c\),
- \(m\) is the sum of the weights of all the links in the graph.

This formula is implemented in the code through the calculation of `inc`, `deg`, and `links` (where `links` corresponds to \(m\) in the formula), and the final computation of `res` (which corresponds to \(Q\)).




---

just for future purposes

![[Pasted image 20240422001244.png]]