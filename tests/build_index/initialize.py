from pympler import asizeof
import time
import itertools
import pandas as pd
import seaborn as sns
from triesketch.utils import *

######################### RUNNER #########################

def main():

    ### VARIABLES ############
    k = 21  # K-mer length
    genome_files = [f'./data/chr22_parts/{i}.fna' for i in range(1,11)]
    _, trie_types = get_tries()
    
    results = [] 
    ###########################

    # Loop over each genome file and each trie type
    for genome_file, trie_type in itertools.product(genome_files, trie_types):
        
        # Step 1: Read genome sequences from the file
        sequences = read_genome_file(genome_file)
        if not sequences:
            print(f"Error: No sequences found in '{genome_file}'.")
            continue
        
        print(f"Loaded {len(sequences)} sequences from '{genome_file}'.")
        
        # Step 2: Generate all k-mers of length k
        kmers = generate_kmers(sequences, k)
        print(f"Generated {len(kmers)} unique {k}-mers from the genome sequences.")
        
        # Step 3: Initialize the trie with all k-mers and time the construction
        start_time = time.perf_counter()
        
        # Initialize the specified trie type
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
            print(f"Error: Invalid trie type '{trie_type}' specified.")
            continue
        
        end_time = time.perf_counter()
        construction_time = end_time - start_time
        
        # Measure the size of the trie
        trie_size = asizeof.asizeof(trie)
        
        # Record the results for this trie type and genome file
        results.append({
            "Genome File": genome_file,
            "Trie Type": trie_type,
            "Construction Time (s)": construction_time,
            "Trie Size (bytes)": trie_size,
            "Number of k-mers": len(kmers)
        })
        
        print(f"{trie_type} initialized with {len(kmers)} k-mers.")
        print(f"Trie construction time: {construction_time:.4f} seconds")
        print(f"Total size of trie: {trie_size} bytes")
    
    # Save results to a DataFrame and export to CSV
    df_results = pd.DataFrame(results)
    df_results.to_csv('./build_index/initialize_results.csv', index=False)
    print("\nResults saved to 'initialize_results.csv'.")

if __name__ == "__main__":
    main()