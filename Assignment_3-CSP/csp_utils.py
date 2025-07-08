import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def load_graph(csv_path="CSPData.csv"):
    df = pd.read_csv(csv_path, header=None)
    upper_triangle = df.iloc[1:, 2:].fillna(0).astype(int)
    size = 30
    variables = [f"X{i}" for i in range(1, size + 1)]

    adjacency_matrix = pd.DataFrame(np.zeros((size, size), dtype=int), columns=variables, index=variables)
    for i in range(size):
        for j in range(i + 1, size):
            val = upper_triangle.iat[i, j - i - 1]
            adjacency_matrix.iat[i, j] = val
            adjacency_matrix.iat[j, i] = val

    graph = {var: [] for var in variables}
    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            if adjacency_matrix.iat[i, j] == 1:
                graph[var1].append(var2)
    return graph

def count_conflicts(graph, assignment):
    return sum(
        1 for var in graph for neighbor in graph[var]
        if assignment[var] == assignment[neighbor]
    ) // 2

def visualize_coloring(graph, assignment, title):
    import networkx as nx
    G = nx.Graph()
    for var in graph:
        for neighbor in graph[var]:
            G.add_edge(var, neighbor)

    pos = nx.circular_layout(G)
    cmap = plt.cm.get_cmap('tab10', max(assignment.values()) + 1)
    node_colors = [cmap(assignment[node]) for node in G.nodes]

    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=600, font_size=8)
    plt.title(title)

    #  Sanitize filename
    safe_title = title.replace(":", "-").replace(" ", "_")
    filename = f"Fig_Data_{safe_title}.png"

    #  Save and close the figure
    plt.savefig(filename)
    print(f"Figure saved as {filename}")
    plt.close()
