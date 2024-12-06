import numpy as np
from triesketch.patricia_trie import PatriciaTrie

def find_depth_of_patricia_trie_simple(trie):
    """
    Finds the depth of a Patricia Trie by following a single path.

    Parameters:
    - trie (PatriciaTrie): The Patricia Trie.

    Returns:
    - int: The depth of the trie.
    """
    current = trie.root
    depth = 0

    # Traverse down a single path
    while current.children:
        # Select one child arbitrarily and add its key length to depth
        key, next_node = next(iter(current.children.items()))
        depth += len(key)
        current = next_node

    return depth

# MASH distance calculation: takes in length of k-mer (k) and Jaccard similarity coefficient (j)
def mash_dist(kmer_a, kmer_b, k, jaccard_sim_a = True):
    if jaccard_sim_a:
        j = find_distance_by_trie(kmer_a, kmer_b, k)
        return (-1/k) * np.log(2 * j / (1 + j))
    else:
        j = calculate_jaccard_similarity_by_prefix_length(kmer_a, kmer_b, k)
        trie_k = find_depth_of_patricia_trie_simple(kmer_a)
        return (-1/trie_k) * np.log(2 * j / (1 + j))

def find_prefixes_of_length(trie, k):
    """Finds all unique prefixes of length k in the trie."""
    results = []

    def traverse(node, prefix):
        # If the accumulated prefix length is k, add it to results
        if len(prefix) == k:
            results.append(prefix)
            return

        # Traverse children if the current prefix length is less than k
        for key, child in node.children.items():
            remaining_length = k - len(prefix)
            if len(key) <= remaining_length:
                # Add the whole key if it fits within the remaining length
                traverse(child, prefix + key)
            else:
                # Add only the first part of the key to make the prefix length k
                results.append(prefix + key[:remaining_length])

    # Start traversal from the root with an empty prefix
    traverse(trie.root, "")
    return results

# kmer_a and kmer_b are two tries
def find_distance_by_trie(kmer_a: PatriciaTrie, kmer_b: PatriciaTrie, k):
     # Use helper function to find all prefixes of length k
    prefixes_a = set(find_prefixes_of_length(kmer_a, k))
    prefixes_b = set(find_prefixes_of_length(kmer_b, k))
    
    # Compute the intersection (shared prefixes) and union (unique prefixes)
    jacard_num = len(prefixes_a & prefixes_b)
    jacard_denom = len(prefixes_a | prefixes_b)
    
    return jacard_num / jacard_denom


def find_distance_by_trie_improved(trie_a, trie_b, k):
    """Calculates Jaccard similarity based on prefixes of length k."""
    
    # Step 1: Extract all prefixes of length k
    prefixes_a = set(find_prefixes_of_length(trie_a, k))
    prefixes_b = set(find_prefixes_of_length(trie_b, k))
    
    # Step 2: Compute shared prefixes
    shared_prefixes = prefixes_a & prefixes_b
    
    # Step 3: Compute the numerator (shared prefix count)
    shared_count = 0
    for prefix in shared_prefixes:
        count_a = trie_a.count_prefix_matches(prefix)
        count_b = trie_b.count_prefix_matches(prefix)
        shared_count += min(count_a, count_b)
    
    # Step 4: Compute the total prefix count (denominator)
    total_count_a = sum(trie_a.count_prefix_matches(prefix) for prefix in prefixes_a)
    total_count_b = sum(trie_b.count_prefix_matches(prefix) for prefix in prefixes_b)
    total_count = total_count_a + total_count_b - shared_count  # Avoid double-counting shared prefixes

    # Step 5: Calculate and return Jaccard similarity
    if total_count == 0:
        return 0  # Avoid division by zero
    return shared_count / total_count


if __name__ == '__main__': 
    trie_a = PatriciaTrie(['ATCG', 'TCGA', 'GCTA'])
    trie_b = PatriciaTrie(['TCGA', 'GCTA', 'ATCGT'])
    print(trie_a)
    k = 4 
    distance = mash_dist(trie_a, trie_b, k)
    print(f"MASH Distance: {distance}")
