import numpy as np

from triesketch.patricia_trie import PatriciaTrie

# MASH distance calculation: takes in length of k-mer (k) and Jaccard similarity coefficient (j)
def mash_dist(kmer_a, kmer_b, k, jaccard_sim_a = True):
    if jaccard_sim_a:
        j = find_distance_by_trie(kmer_a, kmer_b)
    else:
        j = find_distance_by_trie_improved(kmer_a, kmer_b)
    return j, (-1/k) * np.log(2 * j / (1 + j))

# kmer_a and kmer_b are two tries
def find_distance_by_trie(kmer_a: PatriciaTrie, kmer_b: PatriciaTrie):
    #two helper functions to find shared kmers and total unique kmers between the two genomes
    def traverse_and_count_shared(node, current_prefix):
        """Helper function to traverse trie1 and count shared k-mers."""
        count = 0
        
        if kmer_b.prefix_search(current_prefix):
            if node.is_end_of_word and kmer_b.search(current_prefix):
                count += 1
            
            # Recursively check all children
            for key, child in node.children.items():
                count += traverse_and_count_shared(child, current_prefix + key)
        
        return count

    # Store unique k-mers across both tries
    unique_kmers = set()

    def add_kmers_to_set(node, current_prefix, kmers_set):
        """Helper function to traverse a trie and add k-mers to a set."""
        if node.is_end_of_word:
            kmers_set.add(current_prefix)
        for key, child in node.children.items():
            add_kmers_to_set(child, current_prefix + key, kmers_set)

    jacard_num = traverse_and_count_shared(kmer_a.root, "")
    # Add k-mers from both tries to the set
    add_kmers_to_set(kmer_a.root, "", unique_kmers)
    add_kmers_to_set(kmer_b.root, "", unique_kmers)
    jacard_denom = len(unique_kmers)

    return jacard_num/jacard_denom

def find_distance_by_trie_improved(kmer_a, kmer_b):
    def count_shared_kmers_with_prefix(trie1, trie2):
        shared_kmer_count = 0

        def traverse_and_compare(node, prefix):
            nonlocal shared_kmer_count
            if node.is_end_of_word:
                # Count matches for this k-mer in the second trie
                shared_count = trie2.count_prefix_matches(prefix)
                shared_kmer_count += min(node.count, shared_count)

            # Traverse children and extend the prefix
            for key, child in node.children.items():
                traverse_and_compare(child, prefix + key)

        traverse_and_compare(trie1.root, "")
        return shared_kmer_count
    jacard_num = count_shared_kmers_with_prefix(kmer_a, kmer_b)

    total_kmers_a = kmer_a.count_prefix_matches("")
    total_kmers_b = kmer_b.count_prefix_matches("")
    jacard_denom = (total_kmers_a + total_kmers_b) - jacard_num

    return jacard_num/jacard_denom