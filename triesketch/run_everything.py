from triesketch.utils import *
import numpy as np
from triesketch import distance_calc
from triesketch import create_phylo_tree

def main():
    names = ["MZ169912", "MZ219592", "MW913395", "LC623948", "MW981442", "MZ202314", "MW789246", "MZ277392"]
    #read in files
    genome_files = [f'./data/chr22_parts/{i}.fa' for i in range(1,11)] #change this for actual data
    final_dict = []
    
    kmer_length = 21
    
    #this adds the tries to the final_dict
    for index, genome_file in enumerate(genome_files):
        sequences = read_genome_file(genome_file)
        if not sequences:
            print(f"Error: No sequences found in '{genome_file}'.")
            continue
        kmers = generate_kmers(sequences, kmer_length)
        trie = PatriciaTrie(keys=kmers)
        final_dict[index] = trie
    
    k_values = [3, 5] #can change to the values we want to test or just change for loop to test range of k values
    
    distance_matrix_1 = np.zeros((len(names), len(names)))
    distance_matrix_2 = np.zeros((len(names), len(names)))

    for k in k_values:
        for i in range(len(final_dict)):
            for j in range(i + 1, len(final_dict)):
                distance_matrix_1[i][j] = distance_matrix_1[j][i] = distance_calc.find_distance_by_trie(final_dict[i], final_dict[j], k)
                distance_matrix_2[i][j] = distance_matrix_2[j][i] = distance_calc.find_distance_by_trie(final_dict[i], final_dict[j], k)
        tree_using_approach1 = create_phylo_tree.neighbor_joining(distance_matrix_1)
        tree_using_approach2 = create_phylo_tree.neighbor_joining(distance_matrix_2)
        
        create_phylo_tree.print_tree(tree_using_approach1)
        create_phylo_tree.print_tree(tree_using_approach2)