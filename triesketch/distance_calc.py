import numpy as np
from triesketch.patricia_trie import PatriciaTrie

# MASH distance calculation: takes in length of k-mer (k) and Jaccard similarity coefficient (j)
def mash_dist(kmer_a, kmer_b, k, jaccard_sim_a = True):
    if jaccard_sim_a:
        j = find_distance_by_trie(kmer_a, kmer_b, k)
        return (-1/k) * np.log(2 * j / (1 + j)) if j != 0 else (-1/k) * np.log(2 * 1e-6 / (1 + 1e-6))
    else:
        j = find_distance_by_trie_improved(kmer_a, kmer_b, k)
        trie_k = find_depth_of_patricia_trie_simple(kmer_a)
        return (-1/trie_k) * np.log(2 * j / (1 + j)) if j != 0 else (-1/trie_k) * np.log(2 * 1e-6 / (1 + 1e-6))

def find_depth_of_patricia_trie_simple(trie):
    current = trie.root
    depth = 0

    while current.children:
        key, next_node = next(iter(current.children.items()))
        depth += len(key)
        current = next_node

    return depth

def find_prefixes_of_length(trie, k):
    results = []

    def traverse(node, prefix):
        if len(prefix) == k:
            results.append(prefix)
            return

        for key, child in node.children.items():
            remaining_length = k - len(prefix)
            if len(key) <= remaining_length:
                traverse(child, prefix + key)
            else:
                results.append(prefix + key[:remaining_length])

    traverse(trie.root, "")
    return results

# Approach 1
def find_distance_by_trie(trie_a: PatriciaTrie, trie_b: PatriciaTrie, k):
    prefixes_a = set(find_prefixes_of_length(trie_a, k))
    prefixes_b = set(find_prefixes_of_length(trie_b, k))
    
    jacard_num = len(prefixes_a & prefixes_b)
    jacard_denom = len(prefixes_a | prefixes_b)
    
    return jacard_num / jacard_denom

# Approach 2
def find_distance_by_trie_improved(trie_a, trie_b, k):
    prefixes_a = set(find_prefixes_of_length(trie_a, k))
    prefixes_b = set(find_prefixes_of_length(trie_b, k))
    
    shared_prefixes = prefixes_a & prefixes_b

    shared_count = 0
    for prefix in shared_prefixes:
        count_a = trie_a.count_prefix_matches(prefix)
        count_b = trie_b.count_prefix_matches(prefix)
        shared_count += min(count_a, count_b)
    
    total_count_a = sum(trie_a.count_prefix_matches(prefix) for prefix in prefixes_a)
    total_count_b = sum(trie_b.count_prefix_matches(prefix) for prefix in prefixes_b)
    total_count = total_count_a + total_count_b - shared_count  

    if total_count == 0:
        return 0  
    return shared_count / total_count
