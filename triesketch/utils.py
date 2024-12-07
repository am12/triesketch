####### BUILD INDICES #######
from triesketch.dictionary import Dictionary
from triesketch.naive_trie import NaiveTrie
from triesketch.trie import Trie
from triesketch.patricia_trie import PatriciaTrie
from triesketch.pytricia_trie import PytriciaTrie
from triesketch.marisa_trie import MarisaTrie

# NOTE: Marisa trie is static, so cannot add or remove from it without creating a new trie
def get_tries():
    """
    Returns a list of Trie objects for testing.
    """
    return [Dictionary(), NaiveTrie(), Trie(), PatriciaTrie(), PytriciaTrie(), MarisaTrie()], ["Dictionary", "NaiveTrie", "Trie", "PatriciaTrie", "PytriciaTrie", "MarisaTrie"]

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


####### CREATE PHYLOGENETIC TREE #######
import numpy as np

def neighbor_joining(distance_matrix, name_list):
    final_matrix = np.copy(distance_matrix)
    n = len(final_matrix)
    labels = name_list
    nodes = labels.copy()
    tree = {}
    next_node = n  #when there is a new node that is created to connect the original nodes use next number
    
    while len(nodes) > 1:
        # Calculate net divergence (r)
        if len(nodes) > 2:
            r = np.sum(final_matrix, axis=1) * 1 / (len(nodes) - 2)
        else:
            node1, node2 = nodes
            distance = final_matrix[0, 1]  #Distance between the last two nodes
            if node1 in tree:
                tree[node1][node2] = distance
            else:
                tree[node2][node1] = distance
            break
        
        # Calculate adjusted distance (D)
        D = np.zeros((len(nodes), len(nodes)))
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                D[i][j] = D[j][i] = final_matrix[i][j] - r[i] - r[j]
        
        # Find neighbors (minimum D)
        min_value = float('inf')
        min_i, min_j = -1, -1
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if D[i][j] < min_value:
                    min_value = D[i][j]
                    min_i, min_j = i, j
        #print(min_i, min_j)
        
        #Create new node
        new_node = str(next_node)
        next_node += 1
        d_iu = 0.5 * (final_matrix[min_i][min_j] + r[min_i] - r[min_j])
        d_ju = 0.5 * (final_matrix[min_i][min_j] - r[min_i] + r[min_j])
        
        #Update tree
        tree[new_node] = {nodes[min_i]: d_iu, nodes[min_j]: d_ju}
        
        #Update distance matrix
        new_distances = 0.5 * (final_matrix[min_i] + final_matrix[min_j] - final_matrix[min_i][min_j])
        new_distances = np.delete(new_distances, [min_i, min_j])
        
        final_matrix = np.delete(final_matrix, [min_i, min_j], axis=0)
        final_matrix = np.delete(final_matrix, [min_i, min_j], axis=1)
        
        if final_matrix.size == 0:
            final_matrix = new_distances.reshape(1, -1)
        else:
            new_distances_row = new_distances.reshape(1, -1)
            final_matrix = np.vstack([new_distances_row, final_matrix])

            new_distances = np.insert(new_distances, 0, 0)
            new_column = new_distances.reshape(-1, 1)
            final_matrix = np.hstack([new_column, final_matrix])
        #print(final_matrix)
        
        #Update nodes list
        nodes = [new_node] + [n for i, n in enumerate(nodes) if i not in [min_i, min_j]]
    
    return tree

def print_tree(tree, node=None, indent="", last=True):
    if node is None:
        node = max(tree.keys(), key=lambda x: int(x) if x.isdigit() else 0)
    
    prefix = indent + ("└── " if last else "├── ")
    print(f"{prefix}{node}")
    
    children = tree.get(node, {})
    child_count = len(children)
    for i, (child, distance) in enumerate(children.items()):
        #print(distance)
        new_indent = indent + ("    " if last else "│   ")
        print_tree(tree, child, new_indent, i == child_count - 1)
        if i < child_count - 1:
            print(f"{new_indent}│")


####### DISTANCE CALCULATION #######
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
        j = find_distance_by_trie_improved(kmer_a, kmer_b, k)
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