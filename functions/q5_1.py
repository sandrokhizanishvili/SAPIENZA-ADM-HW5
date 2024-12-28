from collections import deque


def edge_betweenness_centrality(graph):
    """
    Calculate the edge betweenness centrality (EBC) for each edge in the given graph.
    Parameters:
        graph (networkx.Graph): The input graph for which to calculate edge betweenness centrality.
    Returns:
        dict: A dictionary where keys are edges (tuples of nodes) and values are the EBC scores.
    """
    # initialize EBC scores for each edge to zero
    ebc_scores = {tuple(sorted(edge)): 0 for edge in graph.edges}
    
    for source in graph.nodes(): # iterate on each node of the graph
        # initializes the distance from the source node to all other nodes as infinity, 
        # except for the source node itself, which has a distance of zero
        distance = {node: float('inf') for node in graph.nodes()}
        distance[source] = 0
        # initializes the number of shortest paths from the source node to all other nodes as zero, 
        # except for the source node itself, which has one shortest path
        sigma = {node: 0 for node in graph.nodes()}
        sigma[source] = 1    
        # initializes a list of predecessors for each node as an empty list 
        # to keep track of the nodes that precede it on the shortest paths.
        predecessors = {node: [] for node in graph.nodes()}
        
        # uses a breadth-first search (BFS) to find the shortest paths 
        # from the source node to all other nodes. During this process, 
        # it updates the distance, sigma, and predecessors for each node.
        queue = deque([source])
        stack = []  
        # if there are at least one element left in the queue
        while queue:
            # remove the node from the queue and add it to the stack
            current = queue.popleft()
            stack.append(current)    
            # for each neighbors of the current node
            for neighbor in graph.neighbors(current):
                # if the visted node is new, updates his distance and appends it to the queue
                if distance[neighbor] == float('inf'):
                    distance[neighbor] = distance[current] + 1
                    queue.append(neighbor)
                # updates the number of shorter paths, of the current neighbor
                if distance[neighbor] == distance[current] + 1:
                    sigma[neighbor] += sigma[current]
                    predecessors[neighbor].append(current)
        
        # it initializes a dictionary delta to store the dependency of each node on the source node
        delta = {node: 0.0 for node in graph.nodes()}
        # calculates scores
        while stack:
            node = stack.pop()
            for pred in predecessors[node]:
                contribution = (sigma[pred] / sigma[node]) * (1 + delta[node])
                edge = tuple(sorted((node, pred)))  # not oriented edges
                ebc_scores[edge] += contribution
                delta[pred] += contribution
    
    # being an undirected graph, to avoid double counting, we divide each score by 2
    for edge in ebc_scores:
        ebc_scores[edge] /= 2.0
    
    return ebc_scores




def edge_to_remove(graph):
    """
    Identifies the edge with the highest edge betweenness centrality (EBC) score in the given graph.
    Parameters:
        graph (networkx.Graph): A NetworkX graph object.
    Returns:
        tuple: A tuple representing the edge with the highest EBC score.
    """
    N_dict = edge_betweenness_centrality(graph)

    # extract the edge with highest ebc score
    max_edge = max(N_dict, key=N_dict.get) #find the key associated with the max value in the dict

    return max_edge




def connected_components(graph):
    """
    Find all connected components in an undirected graph using a depth-first search (DFS).
    Parameters:
        graph (networkx.Graph): An undirected graph represented using the NetworkX library.
    Returns:
        list: A list of sets, where each set contains the nodes of a connected component.
    """
    
    visited = set() # already visited nodes
    components = [] # will contain sets of nodes of a connected component

    def dfs(node, component):
        visited.add(node)
        component.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in graph.nodes():
        if node not in visited:
            component = set()
            dfs(node, component)
            components.append(component)

    return components




def girvan_newman(graph):
	"""
	Implements the Girvan-Newman algorithm to detect communities in a graph by progressively removing edges.
	Parameters:
		graph (networkx.Graph): The input graph on which to perform community detection.
	Returns:
		list: A list of sets, where each set contains the nodes of a connected component in the graph.
	Notes:
	- This function uses the edge betweenness centrality to identify and remove edges.
	- The process continues until the graph is split into multiple connected components.
	"""
	sg = connected_components(graph)
	sg_count = len(sg) # number_connected_components(graph)

	while sg_count == 1:
		edge = edge_to_remove(graph)
		graph.remove_edge(edge[0], edge[1])
		sg = connected_components(graph)
		sg_count = len(sg) # number_connected_components(graph)
	return sg