from triesketch.utils import *
import numpy as np

def main():
    names = ["chicken", "Drosophila", "frog-FOR2", "human", "mouse", "rat"]
    #read in files
    genome_files = [f'./data/animal_data_set/{names[i]}.fasta' for i in range(0,len(names))] 
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
        final_dict.append(trie)
    
    k_values = [15] #can change to the values we want to test or just change for loop to test range of k values
    
    distance_matrix_1 = np.zeros((len(names), len(names)))
    distance_matrix_2 = np.zeros((len(names), len(names)))

    for k in k_values:
        for i in range(len(final_dict)):
            for j in range(i + 1, len(final_dict)):
                distance_matrix_1[i][j] = distance_matrix_1[j][i] = find_distance_by_trie(final_dict[i], final_dict[j], k)
                distance_matrix_2[i][j] = distance_matrix_2[j][i] = find_distance_by_trie(final_dict[i], final_dict[j], k)
        tree_using_approach1 = neighbor_joining(distance_matrix_1, names)
        tree_using_approach2 = neighbor_joining(distance_matrix_2, names)
        
        print_tree(tree_using_approach1)
        print_tree(tree_using_approach2)

if __name__ == "__main__":
    main()