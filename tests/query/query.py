from pympler import asizeof
import os
import time
import itertools
import pandas as pd
import seaborn as sns
import random
from triesketch.utils import *

######################### RUNNER #########################

def main():

    ### VARIABLES ############
    k = 21  # K-mer length
    genome_file = './data/chm13_chr22.fa'  # Using only the 1% genome sample
    trie_types = ['NaiveTrie', 'PatriciaTrie', 'PytriciaTrie', 'MarisaTrie'] # Using only the NaiveTrie, PatriciaTrie, PytriciaTrie, and MarisaTrie
    num_test_prefixes = 30  # Number of random prefixes to test per prefix length
    max_prefix_length = 21  # Maximum length of prefixes to test
    
    results = [] 
    ###########################

    # Step 1: Read genome sequences from the file
    sequences = read_genome_file(genome_file)
    if not sequences:
        print(f"Error: No sequences found in '{genome_file}'.")
        return
    
    print(f"Loaded {len(sequences)} sequences from '{genome_file}'.")
    
    # Step 2: Generate all k-mers of length k
    kmers = list(generate_kmers(sequences, k))
    print(f"Generated {len(kmers)} unique {k}-mers from the genome sequences.")
    
    # Loop over each trie type
    for trie_type in trie_types:
        
        # Step 3: Initialize the trie with all k-mers and time the construction
        start_time = time.perf_counter()
        
        # Initialize the specified trie type
        if trie_type == "NaiveTrie":
            trie = NaiveTrie(keys=kmers)
        elif trie_type == "PytriciaTrie":
            trie = PytriciaTrie(keys=kmers)
        elif trie_type == "PatriciaTrie":
            trie = PatriciaTrie(keys=kmers)
        elif trie_type == "MarisaTrie":
            trie = MarisaTrie(keys=kmers)
        else:
            print(f"Error: Invalid trie type '{trie_type}' specified.")
            continue
        
        end_time = time.perf_counter()
        construction_time = end_time - start_time
        
        # Measure the size of the trie
        trie_size = asizeof.asizeof(trie)
        
        # Step 4: Test different prefix lengths
        for prefix_length in range(1, max_prefix_length + 1):
            # Generate random prefixes of the specified length from the k-mers
            test_prefixes = []
            for _ in range(num_test_prefixes):
                # Choose a k-mer long enough to provide a prefix of the desired length
                kmer = random.choice([k for k in kmers if len(k) >= prefix_length])
                test_prefixes.append(kmer[:prefix_length])
            
            # Time prefix search and count for each prefix
            prefix_search_times = []
            prefix_count_times = []
            
            for prefix in test_prefixes:
                # Prefix search timing
                start_time = time.perf_counter()
                prefix_exists = trie.prefix_search(prefix)  # Now returns True/False
                end_time = time.perf_counter()
                prefix_search_times.append(end_time - start_time)
                
                # Prefix count timing
                start_time = time.perf_counter()
                count_result = trie.count_prefix_matches(prefix)
                end_time = time.perf_counter()
                prefix_count_times.append(end_time - start_time)
            
            # Calculate average times for the current prefix length
            avg_prefix_search_time = sum(prefix_search_times) / num_test_prefixes
            avg_prefix_count_time = sum(prefix_count_times) / num_test_prefixes
            
            # Record results for each prefix length
            results.append({
                "Genome File": genome_file,
                "Trie Type": trie_type,
                "Prefix Length": prefix_length,
                "Construction Time (s)": construction_time,
                "Trie Size (bytes)": trie_size,
                "Average Prefix Search Time (s)": avg_prefix_search_time,
                "Average Prefix Count Time (s)": avg_prefix_count_time,
                "Prefixes Tested": num_test_prefixes,
                "Prefixes": test_prefixes,
                "Prefix Exists": prefix_exists,
                "Prefix Count": count_result,
                "Number of k-mers": len(kmers)
            })
            
            print(f"{trie_type} with prefix length '{prefix_length}'")
            print(f"  Average prefix search time: {avg_prefix_search_time:.6f} seconds")
            print(f"  Average prefix count time: {avg_prefix_count_time:.6f} seconds")
    
    # Save results to a DataFrame and export to CSV
    results_path = './tests/query/query_results_avg.csv'
    df_results = pd.DataFrame(results)
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    df_results.to_csv(results_path, index=False)

    print(f"\nResults saved to {results_path}.")

if __name__ == "__main__":
    main()