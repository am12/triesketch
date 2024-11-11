from pympler import asizeof
import os
import time
import itertools
import pandas as pd
import seaborn as sns
from triesketch.utils import *

######################### RUNNER #########################

def main():

    ### VARIABLES ############
    k = 21  # K-mer length
    genome_file = './data/chr22_parts/1.fa'  # Using only the 1% genome sample
    trie_types = ['NaiveTrie', 'PatriciaTrie', 'PytriciaTrie', 'MarisaTrie'] # Using only the NaiveTrie, PatriciaTrie, PytriciaTrie, and MarisaTrie
    
    results = [] 
    ###########################

    # Step 1: Read genome sequences from the file
    sequences = read_genome_file(genome_file)
    if not sequences:
        print(f"Error: No sequences found in '{genome_file}'.")
        return
    
    print(f"Loaded {len(sequences)} sequences from '{genome_file}'.")
    
    # Step 2: Generate all k-mers of length k
    kmers = generate_kmers(sequences, k)
    print(f"Generated {len(kmers)} unique {k}-mers from the genome sequences.")
    
    # Define prefixes for query testing
    test_prefixes = ["ACTG", "GCTA", "TTAA", "AGCT", "CGTA"]
    
    # Loop over each trie type
    for trie_type in trie_types:
        
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
        
        # Step 4: Time prefix search and prefix count for each prefix
        for prefix in test_prefixes:
            # Prefix search timing
            start_time = time.perf_counter()
            search_results = trie.prefix_search(prefix)
            end_time = time.perf_counter()
            prefix_search_time = end_time - start_time
            
            # Prefix count timing
            start_time = time.perf_counter()
            count_result = trie.count_prefix_matches(prefix)
            end_time = time.perf_counter()
            prefix_count_time = end_time - start_time
            
            # Record results
            results.append({
                "Genome File": genome_file,
                "Trie Type": trie_type,
                "Prefix": prefix,
                "Construction Time (s)": construction_time,
                "Trie Size (bytes)": trie_size,
                "Prefix Search Time (s)": prefix_search_time,
                "Prefix Count Time (s)": prefix_count_time,
                "Number of k-mers": len(kmers),
                "Search Result Count": len(search_results),
                "Count Result": count_result
            })
            
            print(f"{trie_type} with prefix '{prefix}'")
            print(f"  Prefix search time: {prefix_search_time:.6f} seconds")
            print(f"  Prefix count time: {prefix_count_time:.6f} seconds")
            print(f"  Search results found: {len(search_results)}")
            print(f"  Count result: {count_result}")
    
    # Save results to a DataFrame and export to CSV
    results_path = './tests/query_benchmark/query_results.csv'
    df_results = pd.DataFrame(results)
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    df_results.to_csv(results_path, index=False)

    print(f"\nResults saved to {results_path}.")

if __name__ == "__main__":
    main()