import numpy as np

def neighbor_joining(distance_matrix):
    final_matrix = np.copy(distance_matrix)
    n = len(final_matrix)
    labels = [chr(65 + i) for i in range(n)]
    nodes = labels.copy()
    tree = {}
    next_node = n  #when there is a new node that is created to connect the original nodes use next number
    
    while len(nodes) > 1:
        # Calculate net divergence (r)
        if len(nodes) > 2:
            r = np.sum(final_matrix, axis=1) * 1 / (len(nodes) - 2)
        else:
            node1, node2 = nodes
            distance = final_matrix[0, 1]  #Distance between the last two nodes
            if node1 in tree:
                tree[node1][node2] = distance
            else:
                tree[node2][node1] = distance
            break
        
        # Calculate adjusted distance (D)
        D = np.zeros((len(nodes), len(nodes)))
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                D[i][j] = D[j][i] = final_matrix[i][j] - r[i] - r[j]
        
        # Find neighbors (minimum D)
        min_value = float('inf')
        min_i, min_j = -1, -1
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if D[i][j] < min_value:
                    min_value = D[i][j]
                    min_i, min_j = i, j
        #print(min_i, min_j)
        
        #Create new node
        new_node = str(next_node)
        next_node += 1
        d_iu = 0.5 * (final_matrix[min_i][min_j] + r[min_i] - r[min_j])
        d_ju = 0.5 * (final_matrix[min_i][min_j] - r[min_i] + r[min_j])
        
        #Update tree
        tree[new_node] = {nodes[min_i]: d_iu, nodes[min_j]: d_ju}
        
        #Update distance matrix
        new_distances = 0.5 * (final_matrix[min_i] + final_matrix[min_j] - final_matrix[min_i][min_j])
        new_distances = np.delete(new_distances, [min_i, min_j])
        
        final_matrix = np.delete(final_matrix, [min_i, min_j], axis=0)
        final_matrix = np.delete(final_matrix, [min_i, min_j], axis=1)
        
        if final_matrix.size == 0:
            final_matrix = new_distances.reshape(1, -1)
        else:
            new_distances_row = new_distances.reshape(1, -1)
            final_matrix = np.vstack([new_distances_row, final_matrix])

            new_distances = np.insert(new_distances, 0, 0)
            new_column = new_distances.reshape(-1, 1)
            final_matrix = np.hstack([new_column, final_matrix])
        #print(final_matrix)
        
        #Update nodes list
        nodes = [new_node] + [n for i, n in enumerate(nodes) if i not in [min_i, min_j]]
    
    return tree

def print_tree(tree, node=None, indent="", last=True):
    if node is None:
        node = max(tree.keys(), key=lambda x: int(x) if x.isdigit() else 0)
    
    prefix = indent + ("└── " if last else "├── ")
    print(f"{prefix}{node}")
    
    children = tree.get(node, {})
    child_count = len(children)
    for i, (child, distance) in enumerate(children.items()):
        #print(distance)
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

tree = neighbor_joining(distance_matrix)
print_tree(tree)