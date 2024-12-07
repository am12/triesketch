import numpy as np
from triesketch.utils import *
from triesketch import distance_calc
from triesketch import create_phylo_tree

def parse_mash_distance(file_path, genome_order):
    # Initialize the distance matrix
    n = len(genome_order)
    distance_matrix = np.zeros((n, n))
    
    # Create a mapping from genome names to indices
    genome_indices = {f"./correct_data_sets/{name}.fasta": i for i, name in enumerate(genome_order)}
    
    # Read the mash distance matrix file
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            genome1, genome2, distance = parts[0], parts[1], float(parts[2])
            
            if genome1 in genome_indices and genome2 in genome_indices:
                i, j = genome_indices[genome1], genome_indices[genome2]
                distance_matrix[i, j] = distance
                distance_matrix[j, i] = distance  # Symmetric matrix
    
    return distance_matrix

def parse_dashing_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract names and distances
    names = []
    distances = []
    reading_distances = False
    for line in lines:
        if line.startswith("##Names"):
            names = line.strip().split("\t")[1:]  # Extract genome names
            reading_distances = True
        elif reading_distances:
            parts = line.strip().split("\t")
            distances.append(parts[1:])

    # Convert distances to a symmetrical matrix
    n = len(names)
    matrix = np.zeros((n, n))
    for i, row in enumerate(distances):
        for j, value in enumerate(row):
            if value == '-':
                matrix[i, j] = 0.0
            else:
                matrix[i, j] = float(value)

    # Symmetrize the matrix
    for i in range(n):
        for j in range(i+1, n):
            matrix[j, i] = matrix[i, j]

    return names, matrix

def main():
    # Define the order of genomes for the distance matrix
    # genome_order = ["LC623948", "MW789246", "MW913395", "MW981442", 
    #                 "MZ169912", "MZ202314", "MZ219592", "MZ277392"]
    
    # # Parse the mash distance matrix
    # file_path = 'mash_distance_matrix.txt'
    # distance_matrix = parse_mash_distance(file_path, genome_order)
    
    # # Print the resulting distance matrix
    # print("Mash Distance Matrix:")
    # print(distance_matrix)

    # phylo_tree_mash = create_phylo_tree.neighbor_joining(distance_matrix, genome_order)
    # create_phylo_tree.print_tree(phylo_tree_mash)

    # file_path = "dashing_distance_matrix.txt"
    # names, distance_matrix_dashing = parse_dashing_matrix(file_path)

    # print("Dashing Distance Matrix")
    # print(distance_matrix_dashing)

    # phylo_tree_dashing = create_phylo_tree.neighbor_joining(distance_matrix_dashing, genome_order)
    # create_phylo_tree.print_tree(phylo_tree_dashing)

    # Define the order of animal genomes for the distance matrix
    genome_order = ["chicken", "Drosophila", "frog-FOR2", "human", "mouse", "rat"]

    # Parse the animal mash distance matrix
    file_path = 'mash_animal_distance_matrix.txt'
    distance_matrix = parse_mash_distance(file_path, genome_order)
    
    # Print the resulting distance matrix
    print("Mash Distance Matrix:")
    print(distance_matrix)

    phylo_tree_mash = create_phylo_tree.neighbor_joining(distance_matrix, genome_order)
    create_phylo_tree.print_tree(phylo_tree_mash)

    file_path = "dashing_animal_distance_matrix.txt"
    names, distance_matrix_dashing = parse_dashing_matrix(file_path)

    print("Dashing Distance Matrix")
    print(distance_matrix_dashing)

    phylo_tree_dashing = create_phylo_tree.neighbor_joining(distance_matrix_dashing, genome_order)
    create_phylo_tree.print_tree(phylo_tree_dashing)


if __name__ == "__main__":
    main()
