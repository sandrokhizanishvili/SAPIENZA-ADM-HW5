def dijkstra_all_paths(source,graph,adjacency_list):

    '''to calculate the shortest distances and paths from a node to the others we will use the dijkstra algorithm
    with the addition of the use of heapq library to manage a priority queue'''
    
    from heapq import heappop, heappush
    distances = {node: float('inf') for node in graph.nodes} # initialize the distances dictionary, they are initialized to nfinity as required by the algorithm 
    paths = {node: [] for node in graph.nodes} # initialize the paths dictionary
    paths[source] = [[source]] 
    distances[source] = 0

    priority_queue = [(0, source)]  # (distance, node) it's initialized to the source node

    while priority_queue: #stops when there are no more nodes to process
        
        current_dist, current_node = heappop(priority_queue)

        # we can skip processing if this is not the shortest distance to the node
        if current_dist > distances[current_node]:
            continue

        for neighbor in adjacency_list[current_node]: #this would have been also possible by using the graph.neighbors function
            edge_weight = graph.edges[current_node, neighbor]['weight']  # Keep edge weight lookup
            new_dist = current_dist + edge_weight

            if new_dist < distances[neighbor]: #if we found a shorter distance we update the dictionary entry
                distances[neighbor] = new_dist
                paths[neighbor] = [path + [neighbor] for path in paths[current_node]] # and also update the paths by extending the current node's paths to include the neighbor.
                heappush(priority_queue, (new_dist, neighbor)) #pushes to priority queue
            elif new_dist == distances[neighbor]:
                paths[neighbor].extend(path + [neighbor] for path in paths[current_node]) # in this case we just want to update the paths

    return paths, distances

def all_shortest_paths(graph,adjacency_list):

    """This function computes all the shortest paths and distances for every source-taget pairs in the graph.
    This is probably a very unefficient way to go about olving this exercise but makes the subsequent calculations much easier"""
    
    all_paths = [] # empty list of lists
    all_distances = {source: {} for source in graph.nodes} #at the end we will have a dictionary of dictionaries of the form {source: {target_1 : distance, target_2: distance}} etc
    for source in graph.nodes:

        source_paths, source_distances = dijkstra_all_paths(source, graph,adjacency_list) 
        for target, target_paths in source_paths.items():
            if target_paths and any(len(path) > 1 for path in target_paths): # we can filter out trivial paths
                meaningful_paths = [path for path in target_paths if len(path) > 1] 
                all_paths.append(meaningful_paths)
            all_distances[source][target] = source_distances[target] #we update the dictionary of dictionaries

    return all_paths, all_distances

def betweenness_centrality(graph, shortest_paths):

    from collections import defaultdict
    import networkx as nx
    
    centrality = defaultdict(float) 
    N = len(graph.nodes) #total number of nodes

    for paths in shortest_paths:
        path_count = len(paths)  # Number of equivalent shortest paths
        node_contributions = defaultdict(float) 

        for path in paths:
            for node in path[1:-1]:  # we of course need to exclude the source and target nodes
                node_contributions[node] += 1 / path_count #each other node gets a +1 in the count

        for node, contribution in node_contributions.items():
            centrality[node] += contribution #update the centrality dict

    # to compute the final centrality score we need to apply normalization
    scale = (N - 1) * (N - 2) # normalization term for directed graphs
    for node in centrality:
        centrality[node] /= scale

    return dict(centrality) #we convert the defaultdict to a normal dict

def closeness_centrality(all_distances):

    centrality = {}
    #we will implement the formulation we found on wikipedia:

    for node, distances in all_distances.items():
        if len(distances.values()) > 1:
            centrality[node] = sum([1 / x for x in distances.values() if x != 0])
        else:
            centrality[node] = 0.0

    return centrality

def in_degree_centrality_adj(adjacency_list):

    # initialize in-degree counts for each node
    in_degree = {node: 0 for node in adjacency_list.keys()}
    total_nodes = len(adjacency_list)

    # count incoming edges for each node
    for source, targets in adjacency_list.items():
        for target in targets:
            in_degree[target] += 1

    # Calculate in-degree centrality
    centrality = {
        node: in_degree[node] / (total_nodes - 1) 
        for node in adjacency_list
    }

    return centrality

def compute_pagerank(graph, adjacency_list, damping_factor=0.85, max_iterations=100, tolerance=1e-6):

    '''
    dumping factor: probability of following links
    max_iterations: Maximum number of iterations for the algorithm 
    tolerance: Convergence threshold for the scores
    '''

    nodes = list(adjacency_list.keys())
    N = len(nodes)
    pagerank = {node: 1 / N for node in nodes}  # we initialize the nodes' scores to 1/N assuming a uniform distribution 
    new_pagerank = pagerank.copy() # this is just to save the updated scores as a separate object

    for iteration in range(max_iterations):
        for node in nodes:
            # Calculate the weighted sum of incoming edges
            incoming_sum = 0
            for source in adjacency_list:
                if node in adjacency_list[source]:  # we need to check if `source -> node` is a valid step
                    # we need to scale the contribution  
                    weight = graph.edges[source, node]['weight'] 
                    # Total weight of outgoing edges from `source`
                    total_outgoing_weight = sum(graph.edges[source, neighbor]['weight'] for neighbor in adjacency_list[source])
                    # Add contribution to the sum
                    # I should add code to check for "no outgoing edges"
                    incoming_sum += pagerank[source] * (weight / total_outgoing_weight)

            # we implement the PageRank calculation
            new_pagerank[node] = (1 - damping_factor) / N + damping_factor * incoming_sum

        # Check for convergence
        if all(abs(new_pagerank[node] - pagerank[node]) < tolerance for node in nodes): #check condition on all iterables and return true only if all are true
            break

        # Update the PageRank scores for the next iteration
        pagerank = new_pagerank.copy()
        # if got time try parallelization...
    return new_pagerank

def plot_centrality_distributions(final_scores):
        """
        Plot the histograms of centrality distributions using 30 bins 
        """
        import matplotlib.pyplot as plt
        for metric, scores in final_scores.items():
            values = list(scores.values())
            plt.figure(figsize=(8, 6))
            plt.hist(values, bins=30, alpha=0.7, edgecolor='black')
            plt.title(f"Distribution of {metric}")
            plt.xlabel("Centrality Value")
            plt.ylabel("Frequency")
            plt.grid(axis='y', alpha=0.75)
            plt.show()


