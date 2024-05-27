import os
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import layout as ly
pio.templates
 
def visualize_communities(graph, communities, output_file=None):

    pio.templates.default = "plotly_dark"
    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter3d'}]])

    #pos = nx.random_layout(graph,dim=3)                   #very clumsy network

    #very clean
    pos = ly.spring_layout(graph, dim=3, iterations=50)  # Generate positions in 3D with adjusted iterations

    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
    # colors = ['darkred', 'darkblue', 'darkgreen', 'goldenrod', 'darkorange', 'darkviolet']

    for i, community in enumerate(communities):
        subgraph = graph.subgraph(community)
        edge_x = []
        edge_y = []
        edge_z = []
        for edge in subgraph.edges():
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])

        edge_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            # line=dict(width=0.5, color=colors[i % len(colors)]),
            line=dict(width=2, color=colors[i % len(colors)]),  # Increase line width from 0.5 to 2
            hoverinfo='none',
            mode='lines',
            name=f"Community {i + 1} Edges"
        )

        fig.add_trace(edge_trace)

        node_x = []
        node_y = []
        node_z = []
        node_labels = []
        for node in subgraph.nodes():
            x, y, z = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_z.append(z)
            node_labels.append(str(node))

        node_trace = go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers+text',
            text=node_labels,
            textposition='bottom center',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='twilight',
                size=12,
                colorbar=dict(
                    thickness=20,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                )
            ),
            name=f"Community {i + 1} Nodes"
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
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        scene=dict(
            xaxis=dict(showgrid=True, zeroline=True, showticklabels=False),
            yaxis=dict(showgrid=True, zeroline=True, showticklabels=False),
            zaxis=dict(showgrid=True, zeroline=True, showticklabels=False)
        ),
        height=1200,
        width=2400,
        scene_camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    )

    if output_file is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(current_dir, 'static', 'output', 'graph_visualization.html')

    fig.write_html(output_file)

    return output_file
