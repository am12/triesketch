import numpy as np

def neighbor_joining(distance_matrix):
    n = len(distance_matrix)
    nodes = list(range(n))
    tree = {}
    
    while len(nodes) > 2:
        # Calculate Q matrix 
        Q = np.zeros((n, n))
        r = len(nodes)
        for i in range(r):
            for j in range(i+1, r):
                Q[i][j] = Q[j][i] = (r-2) * distance_matrix[i][j] - sum(distance_matrix[i]) - sum(distance_matrix[j])
        
        # Find minimum Q
        min_q = np.inf
        min_i, min_j = -1, -1
        for i in range(r):
            for j in range(i+1, r):
                if Q[i][j] < min_q:
                    min_q = Q[i][j]
                    min_i, min_j = i, j
        
        # Create new node
        new_node = max(nodes) + 1
        d_iu = 0.5 * distance_matrix[min_i][min_j] + (sum(distance_matrix[min_i]) - sum(distance_matrix[min_j])) / (2 * (r-2))
        d_ju = distance_matrix[min_i][min_j] - d_iu
        
        # Update tree
        tree[new_node] = {nodes[min_i]: d_iu, nodes[min_j]: d_ju}
        
        # Update distance matrix
        new_distances = np.zeros(r-1)
        for k in range(r):
            if k != min_i and k != min_j:
                new_distances[k if k < min_j else k-1] = 0.5 * (distance_matrix[min_i][k] + distance_matrix[min_j][k] - distance_matrix[min_i][min_j])
        
        distance_matrix = np.delete(distance_matrix, [min_i, min_j], axis=0)
        distance_matrix = np.delete(distance_matrix, [min_i, min_j], axis=1)
        distance_matrix = np.vstack([distance_matrix, new_distances[:-1]])
        distance_matrix = np.hstack([distance_matrix, np.append(new_distances, [0]).reshape(-1,1)])
        
        # Update nodes list
        nodes = [n for n in nodes if n != nodes[min_i] and n != nodes[min_j]] + [new_node]
        n = len(nodes)
    
    # Connect last two nodes
    tree[nodes[0]] = {nodes[1]: distance_matrix[0][1]}
    
    return tree

# Example usage
distance_matrix = np.array([
    [0, 5, 9, 9, 8],
    [5, 0, 10, 10, 9],
    [9, 10, 0, 8, 7],
    [9, 10, 8, 0, 3],
    [8, 9, 7, 3, 0]
])

tree = neighbor_joining(distance_matrix)
print(tree)