def initialize_labels(graph):
    """
    This function assigns each node in the graph a unique label (which is the node itself).
    Parameters:
        graph (networkx.Graph): The input graph for which labels need to be initialized.
    Returns:
        dict: A dictionary where keys are nodes and values are the corresponding labels.
    """
    return {node: node for node in graph.nodes()}




def propagate_labels(graph, labels):
    """
    This function iteratively updates the label of each node to the most frequent label
    among its neighbors until no more changes occur (the propagation process).
    Parameters:
        graph (networkx.Graph): The input graph where nodes have labels.
        labels (dict): A dictionary where keys are node identifiers and values are the labels of the nodes.
    Returns:
        dict: The updated labels dictionary after propagation.
    """
    changed = True
    while changed:
        changed = False
        for node in graph.nodes():
            # collects labels from neighbors
            neighbor_labels = [labels[neighbor] for neighbor in graph.neighbors(node)]
            if not neighbor_labels:
                continue
            # determines the most frequent label among neighbors
            most_frequent_label = max(set(neighbor_labels), key=neighbor_labels.count)
            # updates the node's label if it changes
            if labels[node] != most_frequent_label:
                labels[node] = most_frequent_label
                changed = True
    return labels




def get_communities(labels):
    """
    Given a dictionary of node labels, group nodes into communities based on their labels.
    Args:
        labels (dict): A dictionary where keys are node identifiers and values are community labels.
    Returns:
        list: A list of lists, where each inner list contains nodes that belong to the same community.
    """
    communities = {}
    for node, label in labels.items():
        if label not in communities:
            communities[label] = []
        communities[label].append(node)
    return list(communities.values())




def label_propagation(graph):
    """
    Perform label propagation algorithm to detect communities in a graph.
    Parameters:
        graph (networkx.Graph): The input graph on which to perform label propagation.
    Returns:
        list: A list of lists, where each inner list contains nodes that belong to the same community.
    """
    labels = initialize_labels(graph)
    labels = propagate_labels(graph, labels)
    communities = get_communities(labels)
    return communities



