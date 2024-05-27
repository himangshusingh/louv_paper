#this is the old 2D visualize.py
#use it as reference if needed


import os
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx

def visualize_communities(graph, communities, output_file=None):

    pio.templates.default = "ggplot2"
    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])

    pos = nx.spring_layout(graph)


    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']

    for i, community in enumerate(communities):
        subgraph = graph.subgraph(community)
        edge_x = []
        edge_y = []
        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color=colors[i % len(colors)]),
            hoverinfo='none',
            mode='lines',
            name=f"Community {i + 1} Edges"  # Add a name for the legend
        )

        fig.add_trace(edge_trace)

        node_x = []
        node_y = []
        node_labels = []
        for node in subgraph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_labels.append(str(node))

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_labels,
            textposition='bottom center',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                )
            ),
            name=f"Community {i + 1} Nodes"  # Add a name for the legend
        )

        fig.add_trace(node_trace)

        node_adjacencies = []
        node_text = []
        for adjacencies in subgraph.adjacency():
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append('# of connections: '+str(len(adjacencies[1])))

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

    fig.update_layout(
        showlegend=True,  # Ensure the legend is shown
        legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),     #positon of legends
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=1080,
        width=1920,
    )

    # If no output_file is provided, use a default absolute path
    #this is explicitly for backup purposes, currently output path is provided in main.py
    if output_file is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(current_dir, 'static','output', 'graph_visualization.html')

    # Save the figure to the HTML file
    fig.write_html(output_file)

    return output_file
