import sys
from pympler import asizeof
import time
import itertools
import pandas as pd

# from triesketch.dictionary import Dictionary
# from triesketch.naive_trie import NaiveTrie
# from triesketch.trie import Trie
# from triesketch.patricia_trie import PatriciaTrie
# from triesketch.pytricia_trie import PytriciaTrie
# from triesketch.marisa_trie import MarisaTrie
from triesketch.utils import *

def read_genome_file(filename):
    """
    Reads a genome file in FASTA format and returns a list of sequences.
    
    Parameters:
    - filename (str): The path to the genome file.
    
    Returns:
    - sequences (list of str): A list of genome sequences.
    """
    sequences = []
    with open(filename, 'r') as file:
        seq = ''
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if line.startswith('>'):
                if seq:
                    sequences.append(seq)
                    seq = ''
            else:
                seq += line.upper()  # Convert to uppercase for consistency
        if seq:
            sequences.append(seq)
    return sequences

def generate_kmers(sequences, k):
    """
    Generates all k-mers of length k from the given sequences.
    
    Parameters:
    - sequences (list of str): The list of sequences to generate k-mers from.
    - k (int): The length of each k-mer.
    
    Returns:
    - kmers (set of str): A set containing all unique k-mers.
    """
    kmers = set()
    for seq in sequences:
        seq_length = len(seq)
        if seq_length < k:
            continue  # Skip sequences shorter than k
        for i in range(seq_length - k + 1):
            kmer = seq[i:i+k]
            kmers.add(kmer)
    return kmers

def main():

    ### VARIABLES ############
    k=21
    
    genome_files = [f'./data/partition_{i}.fna' for i in range(20, 101, 20)]
    _, trie_types = get_tries()
    
    ###########################
    
    for 
        
    # Step 1: Read genome sequences from the file
    sequences = read_genome_file(genome_file)
    if not sequences:
        print("Error: No sequences found in the genome file.")
        sys.exit(1)
    
    print(f"Loaded {len(sequences)} sequences from '{genome_file}'.")
    
    # Step 2: Generate all k-mers of length k
    kmers = generate_kmers(sequences, k)
    print(f"Generated {len(kmers)} unique {k}-mers from the genome sequences.")

    # Step 3: Initialize the trie with all k-mers
    # time the construction of sketch
    start_time = time.time()
    if trie_type == "NaiveTrie":
        trie = NaiveTrie(keys=kmers)
    elif trie_type == "Trie":
        trie = Trie(keys=kmers)
    elif trie_type == "PytriciaTrie":
        trie = PytriciaTrie(keys=kmers)
    elif trie_type == "PatriciaTrie":
        trie = PatriciaTrie(keys=kmers)
    elif trie_type == "MarisaTrie":
        trie = MarisaTrie(keys=kmers)
    elif trie_type == "Dictionary":
        trie = Dictionary(keys=kmers)
    else:
        print("Error: Invalid trie type specified.")
        sys.exit(1)
    end_time = time.time()
    construction_time = end_time - start_time
    trie_size = asizeof.asizeof(trie)
    print(f"{trie_type} initialized with {len(kmers)} k-mers.")
    print(f"Trie construction time: {construction_time:.4f} seconds")
    print(f"Total size of trie: {trie_size} bytes")

    
    # Example usage: Search for a specific k-mer
    # Replace 'ACTGACTG' with the k-mer you want to search for
    kmer_to_search = 'ACTGACTGATATATGTGTCTA'
    if len(kmer_to_search) != k:
        print(f"Error: The k-mer to search must be of length {k}.")
    else:
        if trie.search(kmer_to_search):
            print(f"K-mer '{kmer_to_search}' is present in the genome.")
        else:
            print(f"K-mer '{kmer_to_search}' is not present in the genome.")

if __name__ == "__main__":
    main()