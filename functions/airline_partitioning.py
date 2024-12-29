import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

def airline_partitioning(flights_df):
    """
    Partition the airline flight network into two disconnected subgraphs by removing the minimum number of flights.

    Args:
        flights_df (pd.DataFrame): DataFrame with columns ['Origin_airport', 'Destination_airport', 'Distance'].

    Returns:
        removed_edges (list): List of flights removed to partition the graph.
        graph_before (dict): Original graph representation.
        graph_after (dict): Graph after removing the minimum cut edges.
    """
    # Build the graph
    graph = {}
    for _, row in flights_df.iterrows():
        origin, destination, distance = row['Origin_airport'], row['Destination_airport'], row['Distance']
        if origin not in graph:
            graph[origin] = {}
        # Add directed edge with its distance
        graph[origin][destination] = distance

    # Step 2: Ford-Fulkerson Algorithm to find the minimum cut
    def ford_fulkerson(graph, source, sink):
        """
        Implement the Ford-Fulkerson algorithm to find the maximum flow in a graph.

        Args:
            graph (dict): The directed graph with capacities as edge weights.
            source (str): The source node.
            sink (str): The sink node.

        Returns:
            max_flow (int): The value of the maximum flow.
            residual_graph (dict): The residual graph after finding the maximum flow.
        """
        # Create a residual graph
        residual_graph = {u: neighbors.copy() for u, neighbors in graph.items()}
        max_flow = 0
        parent = {}

        def bfs(source, sink):
            """Find augmenting path using BFS."""
            visited = set()
            queue = [source]
            parent.clear()
            while queue:
                current = queue.pop(0)
                visited.add(current)
                for neighbor, capacity in residual_graph.get(current, {}).items():
                    if neighbor not in visited and capacity > 0:
                        parent[neighbor] = current
                        if neighbor == sink:
                            return True
                        queue.append(neighbor)
            return False

        # Augment flow while there is a path from source to sink
        while bfs(source, sink):
            # Find the minimum residual capacity along the path
            path_flow = float('Inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, residual_graph[parent[s]][s])
                s = parent[s]
            
            # Update residual capacities
            v = sink
            while v != source:
                u = parent[v]
                residual_graph[u][v] -= path_flow
                residual_graph[v][u] = residual_graph.get(v, {}).get(u, 0) + path_flow
                v = parent[v]

            max_flow += path_flow

        return max_flow, residual_graph

    # Find the minimum cut
    def find_min_cut(graph, source, residual_graph):
        """
        Identify the edges to remove to partition the graph.

        Args:
            graph (dict): Original graph with capacities as edge weights.
            source (str): The source node.
            residual_graph (dict): The residual graph after computing max flow.

        Returns:
            cut_edges (list): List of edges to be removed for partitioning.
        """
        visited = set()

        def dfs(node):
            """Mark all reachable nodes from the source."""
            visited.add(node)
            for neighbor, capacity in residual_graph.get(node, {}).items():
                if neighbor not in visited and capacity > 0:
                    dfs(neighbor)

        dfs(source)
        cut_edges = []
        for u in graph:
            for v, capacity in graph[u].items():
                if u in visited and v not in visited:
                    cut_edges.append((u, v))

        return cut_edges

    # Choose arbitrary source and sink
    airports = list(graph.keys())
    source, sink = airports[0], airports[1]

    max_flow, residual_graph = ford_fulkerson(graph, source, sink)
    removed_edges = find_min_cut(graph, source, residual_graph)

    # Visualize the graph

    def visualize_graph(graph, removed_edges=None, title="Airline Network"):
        """
        Visualize the graph using networkx for better layouts.

        Args:
            graph (dict): The graph representation as an adjacency list.
            removed_edges (list): List of edges to highlight as removed (optional).
            title (str): Title for the plot.
        """
        # Create a networkx graph
        G = nx.Graph()
        
        # Add edges to the graph
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        # Draw the graph
        pos = nx.spring_layout(G)  # Use spring layout for better visualization
        plt.figure(figsize=(12, 8))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
        nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')
        
        # Draw edges
        if removed_edges:
            # Highlight removed edges in red
            remaining_edges = [edge for edge in G.edges if edge not in removed_edges and edge[::-1] not in removed_edges]
            nx.draw_networkx_edges(G, pos, edgelist=remaining_edges, edge_color='blue', width=1.5)
            nx.draw_networkx_edges(G, pos, edgelist=removed_edges, edge_color='red', style='dashed', width=2)
        else:
            nx.draw_networkx_edges(G, pos, edge_color='blue', width=1.5)

        plt.title(title)
        plt.show()

    visualize_graph(graph)
    visualize_graph(graph, removed_edges, title='Airline Network After Removing The Connections')

    # Return the result
    return removed_edges, graph, residual_graph