import numpy as np

def neighbor_joining(distance_matrix):
    final_matrix = np.copy(distance_matrix)
    n = len(final_matrix)
    labels = [chr(65 + i) for i in range(n)]  # A, B, C, D for n=4
    nodes = labels.copy()
    tree = {}
    next_node = n  # Start new node labels from n
    
    while len(nodes) > 1:
        # Calculate net divergence (r)
        r = np.sum(final_matrix, axis=1)
        
        # Calculate adjusted distance (D)
        D = np.zeros((len(nodes), len(nodes)))
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                D[i][j] = D[j][i] = (len(nodes) - 2) * final_matrix[i][j] - r[i] - r[j]
        
        # Find neighbors (minimum D)
        min_value = float('inf')
        min_i, min_j = -1, -1
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if D[i][j] < min_value:
                    min_value = D[i][j]
                    min_i, min_j = i, j
        
        # Create new node
        new_node = str(next_node)
        next_node += 1
        if len(nodes) > 2:
            d_iu = 0.5 * (final_matrix[min_i][min_j] + (r[min_i] - r[min_j]) / (len(nodes) - 2))
        else:
            d_iu = 0.5 * final_matrix[min_i][min_j]
        d_ju = final_matrix[min_i][min_j] - d_iu
        
        # Update tree
        tree[new_node] = {nodes[min_i]: d_iu, nodes[min_j]: d_ju}
        
        # Update distance matrix
        new_distances = 0.5 * (final_matrix[min_i] + final_matrix[min_j] - final_matrix[min_i][min_j])
        final_matrix = np.delete(final_matrix, [min_i, min_j], axis=0)
        final_matrix = np.delete(final_matrix, [min_i, min_j], axis=1)
        final_matrix = np.vstack([final_matrix, new_distances[:-2]])
        final_matrix = np.hstack([final_matrix, np.append(new_distances[:-2], [0]).reshape(-1,1)])
        print(final_matrix)
        
        # Update nodes list
        nodes = [n for i, n in enumerate(nodes) if i not in [min_i, min_j]] + [new_node]
    
    return tree

def print_tree(tree, node=None, indent="", last=True):
    if node is None:
        node = max(tree.keys(), key=lambda x: int(x) if x.isdigit() else 0)
    
    prefix = indent + ("└── " if last else "├── ")
    print(f"{prefix}{node}")
    
    children = tree.get(node, {})
    child_count = len(children)
    for i, (child, distance) in enumerate(children.items()):
        print(distance)
        new_indent = indent + ("    " if last else "│   ")
        print_tree(tree, child, new_indent, i == child_count - 1)
        if i < child_count - 1:
            print(f"{new_indent}│")

# Ex
distance_matrix = np.array([
    [0, 2, 2, 2],
    [2, 0, 3, 2],
    [2, 3, 0, 2],
    [2, 2, 2, 0]
])

distance_matrix2 = np.array([
    [0, 4, 5, 10],
    [4, 0, 7, 12],
    [5, 7, 0, 9],
    [10, 12, 9, 0]
])

tree= neighbor_joining(distance_matrix2)
print_tree(tree)