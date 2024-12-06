from triesketch.utils import *
import numpy as np
import sys
import hashlib

def minhash(kmers, size):
    hashed_kmers = [(int(hashlib.md5(kmer.encode()).hexdigest(), 16), kmer) for kmer in kmers]
    hashed_kmers.sort()
    return [kmer for _, kmer in hashed_kmers[:size]]

def main(genome_file_path, output_base, kmer_length=21, k_values=[21], sketch_size=1024):
    with open(genome_file_path, 'r') as f:
        genome_files = [line.strip() for line in f.readlines()]
    
    names = [file.split('/')[-1].split('.')[0] for file in genome_files]
    final_dict = []
    
    # this adds the tries to the final_dict
    for index, genome_file in enumerate(genome_files):
        sequences = read_genome_file(genome_file)
        if not sequences:
            print(f"Error: No sequences found in '{genome_file}'.")
            continue
        kmers = generate_kmers(sequences, kmer_length)
        sketch_kmers = minhash(kmers, sketch_size)
        trie = PatriciaTrie(keys=sketch_kmers)
        final_dict.append(trie)
    
    distance_matrix_1 = np.zeros((len(names), len(names)))
    distance_matrix_2 = np.zeros((len(names), len(names)))

    for k in k_values:
        for i in range(len(final_dict)):
            for j in range(i + 1, len(final_dict)):
                distance_matrix_1[i][j] = distance_matrix_1[j][i] = find_distance_by_trie(final_dict[i], final_dict[j], k)
                distance_matrix_2[i][j] = distance_matrix_2[j][i] = find_distance_by_trie_improved(final_dict[i], final_dict[j], k)
        
        np.savetxt(f'{output_base}_distance_matrix_1_k{k}.txt', distance_matrix_1, fmt='%.6f')
        np.savetxt(f'{output_base}_distance_matrix_2_k{k}.txt', distance_matrix_2, fmt='%.6f')
        
        tree_using_approach1 = neighbor_joining(distance_matrix_1, names)
        tree_using_approach2 = neighbor_joining(distance_matrix_2, names)
        
        print_tree(tree_using_approach1)
        print_tree(tree_using_approach2)

if __name__ == "__main__":
    for group in ['covid', 'bacteria', 'eukarya']: 
        genome_file_path = f'./data/{group}/genomes.txt'
        output_base = f'./tests/3_phylogenetic_distance/{group}'
        kmer_length = 31
        k_values = [21]
        sketch_size = 1024
        main(genome_file_path, output_base, kmer_length, k_values, sketch_size)