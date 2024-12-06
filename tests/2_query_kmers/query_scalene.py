from pympler import asizeof
import os
import time
import itertools
import pandas as pd
import seaborn as sns
import random

######################### TRIES #########################

class TrieNode:
    def __init__(self, key="", is_end_of_word=False):
        self.key = key  # The substring stored at this node
        self.children = []  # List of child TrieNode objects
        self.is_end_of_word = is_end_of_word  # True if the node represents the end of a word

class NaiveTrie:
    def __init__(self, keys=None):
        """
        Initializes the trie. If a list of keys is provided, inserts them into the trie.
        
        Parameters:
        - keys (list of str, optional): The list of words to initialize the trie with.
        """
        self.root = TrieNode()
        if keys:
            for key in keys:
                self.insert(key)
    
    def __name__(self):
        return "NaiveTrie"
    
    def __repr__(self):
        return f"NaiveTrie()"

    def insert(self, word):
        current = self.root
        while word:
            for child in current.children:
                if word.startswith(child.key):
                    # Move down the trie
                    prefix_length = len(child.key)
                    word = word[prefix_length:]
                    current = child
                    break
                else:
                    # Find common prefix between word and child.key
                    common_prefix_length = self._common_prefix_length(word, child.key)
                    if common_prefix_length > 0:
                        # Split the child node
                        common_prefix = word[:common_prefix_length]
                        remaining_word = word[common_prefix_length:]
                        remaining_child_key = child.key[common_prefix_length:]
                        
                        # Create new nodes
                        common_node = TrieNode(common_prefix)
                        child.key = remaining_child_key
                        
                        # Reassign children
                        common_node.children.append(child)
                        current.children.remove(child)
                        current.children.append(common_node)
                        
                        if remaining_word:
                            new_node = TrieNode(remaining_word, True)
                            common_node.children.append(new_node)
                        else:
                            common_node.is_end_of_word = True
                        return
            else:
                # No matching child, add new node
                new_node = TrieNode(word, True)
                current.children.append(new_node)
                return
        current.is_end_of_word = True

    def search(self, word):
        current = self.root
        while word:
            found = False
            for child in current.children:
                if word.startswith(child.key):
                    word = word[len(child.key):]
                    current = child
                    found = True
                    break
            if not found:
                return False
        return current.is_end_of_word

    def delete(self, word):
        """
        Deletes a word from the trie if it exists.
        Returns True if the word was deleted, False if the word was not found.
        """
        return self._delete_recursive(self.root, word)

    def _delete_recursive(self, current, word):
        if not word:
            if not current.is_end_of_word:
                return False  # Word not found
            current.is_end_of_word = False
            return len(current.children) == 0  # If no children, node can be deleted

        for child in current.children:
            if word.startswith(child.key):
                can_delete = self._delete_recursive(child, word[len(child.key):])
                if can_delete:
                    current.children.remove(child)
                    return not current.is_end_of_word and len(current.children) == 0
                return False
        return False  # Word not found

    def _common_prefix_length(self, str1, str2):
        """
        Returns the length of the common prefix between two strings.
        """
        min_length = min(len(str1), len(str2))
        for i in range(min_length):
            if str1[i] != str2[i]:
                return i
        return min_length

    def prefix_search(self, prefix):
        """
        Checks if any word in the trie starts with the given prefix.
        
        Parameters:
        - prefix (str): The prefix to search for.
        
        Returns:
        - bool: True if any word in the trie starts with the given prefix, False otherwise.
        """
        current = self.root
        
        # Traverse the trie to the end of the prefix
        while prefix:
            found = False
            for child in current.children:
                if prefix.startswith(child.key):
                    prefix = prefix[len(child.key):]
                    current = child
                    found = True
                    break
                elif child.key.startswith(prefix):
                    # The prefix matches part of the child's key
                    return True  # Prefix exists in the trie
            if not found:
                return False  # No words with the given prefix

        return True

    def count_prefix_matches(self, prefix):
        """
        Counts the number of words in the trie that match a given prefix.
        
        Parameters:
        - prefix (str): The prefix to count matches for.
        
        Returns:
        - int: The count of words in the trie that start with the given prefix.
        """
        current = self.root
        
        # Traverse the trie to the end of the prefix
        while prefix:
            found = False
            for child in current.children:
                if prefix.startswith(child.key):
                    prefix = prefix[len(child.key):]
                    current = child
                    found = True
                    break
                elif child.key.startswith(prefix):
                    prefix = ""
                    current = child
                    found = True
                    break
            if not found:
                return 0  # No words with the given prefix

        # Count all words starting from the current node
        return self._count_words_from_node(current)

    def _count_words_from_node(self, node):
        """
        Helper method to count all words starting from a given node.
        
        Parameters:
        - node (TrieNode): The current TrieNode to count words from.
        
        Returns:
        - int: The count of words from this node down the tree.
        """
        count = 1 if node.is_end_of_word else 0
        for child in node.children:
            count += self._count_words_from_node(child)
        return count
    
class PatriciaTrieNode:
    def __init__(self, key=""):
        self.key = key  # The substring stored at this node
        self.children = {}  # Dictionary mapping substrings to child nodes
        self.is_end_of_word = False  # True if the node represents the end of a word

class PatriciaTrie:
    def __init__(self, keys=None):
        """
        Initializes the Patricia trie. If a list of keys is provided, inserts them into the trie.

        Parameters:
        - keys (list of str, optional): The list of words to initialize the trie with.
        """
        self.root = PatriciaTrieNode()
        if keys:
            for key in keys:
                self.insert(key)

    def __name__(self):
        return "PatriciaTrie"

    def insert(self, word):
        current = self.root
        while word:
            found = False
            for key in list(current.children.keys()):
                common_prefix_length = self._common_prefix_length(word, key)

                if common_prefix_length > 0:
                    # Case 1: If the common prefix is shorter than the existing key, split the node
                    if common_prefix_length < len(key):
                        existing_node = current.children.pop(key)
                        # Create a new node with the common prefix
                        new_node = PatriciaTrieNode(key=word[:common_prefix_length])
                        current.children[new_node.key] = new_node
                        # Adjust the existing node
                        existing_node.key = key[common_prefix_length:]
                        new_node.children[existing_node.key] = existing_node
                        # Update current node
                        current = new_node
                    else:
                        # Move to the child node
                        current = current.children[key]
                    word = word[common_prefix_length:]
                    if not word:
                        current.is_end_of_word = True
                    found = True
                    break
            if not found:
                # No common prefix; add the word as a new child
                new_node = PatriciaTrieNode(key=word)
                new_node.is_end_of_word = True
                current.children[word] = new_node
                return

    def search(self, word):
        current = self.root
        while word:
            found = False
            for key, node in current.children.items():
                if word.startswith(key):
                    word = word[len(key):]
                    current = node
                    found = True
                    break
            if not found:
                return False
        return current.is_end_of_word

    def delete(self, word):
        def _delete(node, word):
            if not word:
                if not node.is_end_of_word:
                    return False  # Word not found
                node.is_end_of_word = False
                return len(node.children) == 0  # If leaf node, indicate it can be removed

            for key, child in list(node.children.items()):
                if word.startswith(key):
                    can_delete_child = _delete(child, word[len(key):])
                    if can_delete_child:
                        del node.children[key]
                        # If the current node is not an end of a word and has no children, it can be deleted
                        return not node.is_end_of_word and len(node.children) == 0
                    return False
            return False  # Word not found

        _delete(self.root, word)

    def _common_prefix_length(self, str1, str2):
        i = 0
        while i < len(str1) and i < len(str2) and str1[i] == str2[i]:
            i += 1
        return i

    def prefix_search(self, prefix):
        """
        Checks if any word in the trie matches the given prefix.

        Parameters:
        - prefix (str): The prefix to search for.

        Returns:
        - bool: True if any word in the trie starts with the given prefix, False otherwise.
        """
        current = self.root

        # Traverse the trie to the end of the prefix
        while prefix:
            found = False
            for key, node in current.children.items():
                common_prefix_length = self._common_prefix_length(prefix, key)
                if common_prefix_length == len(key):
                    # The key fully matches a prefix of the remaining prefix
                    prefix = prefix[common_prefix_length:]
                    current = node
                    found = True
                    break
                elif common_prefix_length == len(prefix):
                    # The prefix fully matches a prefix of the key
                    return True  # Prefix exists in the trie
            if not found:
                return False  # No words found with the given prefix

        return True

    def count_prefix_matches(self, prefix):
        """
        Counts the number of words in the trie that match a given prefix.

        Parameters:
        - prefix (str): The prefix to count matches for.

        Returns:
        - int: The count of words in the trie that start with the given prefix.
        """
        current = self.root

        # Traverse the trie to the end of the prefix
        while prefix:
            found = False
            for key, node in current.children.items():
                common_prefix_length = self._common_prefix_length(prefix, key)
                if common_prefix_length == len(key):
                    # The key fully matches a prefix of the remaining prefix
                    prefix = prefix[common_prefix_length:]
                    current = node
                    found = True
                    break
                elif common_prefix_length == len(prefix):
                    # The prefix fully matches a prefix of the key
                    prefix = ""
                    current = node
                    found = True
                    break
            if not found:
                return 0  # No words found with the given prefix

        # Count all words starting from the current node
        return self._count_words_from_node(current)

    def _count_words_from_node(self, node):
        """
        Helper method to count all words starting from a given node.
        
        Returns:
        - int: The count of words from this node down the tree.
        """
        count = 1 if node.is_end_of_word else 0
        for child in node.children.values():
            count += self._count_words_from_node(child)
        return count

import patricia

class PytriciaTrie:
    def __init__(self, keys=None):
        """
        Initializes the Patricia trie. If a list of keys is provided, inserts them into the trie.
        
        Parameters:
        - keys (list of str, optional): The list of keys to initialize the trie with.
        """
        self.trie = patricia.trie()
        if keys:
            for key in keys:
                self.trie[key] = True  # Store True as the value since we're only tracking existence

    def __name__(self):
        return "PytriciaTrie"

    def insert(self, key):
        """
        Inserts a key into the trie.
        
        Parameters:
        - key (str): The key to insert.
        """
        self.trie[key] = True

    def delete(self, key):
        """
        Deletes a key from the trie.
        
        Parameters:
        - key (str): The key to delete.
        
        Returns:
        - bool: True if the key was deleted, False if the key was not found.
        """
        try:
            del self.trie[key]
            return True
        except KeyError:
            return False

    def search(self, key):
        """
        Searches for a key in the trie.
        
        Parameters:
        - key (str): The key to search for.
        
        Returns:
        - bool: True if the key exists in the trie, False otherwise.
        """
        return key in self.trie

    def prefix_search(self, prefix):
        """
        Checks if any key in the trie starts with the given prefix.
        
        Parameters:
        - prefix (str): The prefix to search for.
        
        Returns:
        - bool: True if any key in the trie starts with the given prefix, False otherwise.
        """
        return bool(self.trie.keys(prefix))

    def count_prefix_matches(self, prefix):
        """
        Counts the number of keys in the trie that match a given prefix.
        
        Parameters:
        - prefix (str): The prefix to count matches for.
        
        Returns:
        - int: The count of keys in the trie that start with the given prefix.
        """
        return len(list(self.trie.keys(prefix)))
    
import marisa_trie

class MarisaTrie:
    def __init__(self, keys=None):
        """
        Initializes the trie. If a list of keys is provided, inserts them into the trie.
        
        Parameters:
        - keys (list of str, optional): The list of words to initialize the trie with.
        """
        if keys:
            self._keys = set(keys)
        else:
            self._keys = set()
        self._build_trie()
    
    def __name__(self):
        return "MarisaTrie"
    
    def insert(self, word):
        """
        Inserts a word into the trie.
        
        Parameters:
        - word (str): The word to insert.
        """
        self._keys.add(word)
        self._build_trie()
    
    def insert_many(self, words):
        """
        Inserts multiple words into the trie.
        
        Parameters:
        - words (iterable of str): The words to insert.
        """
        self._keys.update(words)
        self._build_trie()
    
    def search(self, word):
        """
        Searches for a word in the trie.
        
        Parameters:
        - word (str): The word to search for.
        
        Returns:
        - bool: True if the word exists in the trie, False otherwise.
        """
        return word in self.trie
    
    def delete(self, word):
        """
        Deletes a word from the trie if it exists.
        
        Parameters:
        - word (str): The word to delete.
        
        Returns:
        - bool: True if the word was deleted, False if the word was not found.
        """
        if word in self._keys:
            self._keys.remove(word)
            self._build_trie()
            return True
        return False
    
    def delete_many(self, words):
        """
        Deletes multiple words from the trie.
        
        Parameters:
        - words (iterable of str): The words to delete.
        """
        self._keys.difference_update(words)
        self._build_trie()
    
    def _build_trie(self):
        """
        Builds the marisa_trie.Trie from the current set of keys.
        """
        self.trie = marisa_trie.Trie(self._keys)

    def prefix_search(self, prefix):
        """
        Checks if any word in the trie matches the given prefix.

        Parameters:
        - prefix (str): The prefix to search for.

        Returns:
        - bool: True if any word in the trie starts with the given prefix, False otherwise.
        """
        return any(self.trie.keys(prefix))

    def count_prefix_matches(self, prefix):
        """
        Counts the number of words in the trie that match a given prefix.

        Parameters:
        - prefix (str): The prefix to count matches for.

        Returns:
        - int: The count of words in the trie that start with the given prefix.
        """
        return len(self.trie.keys(prefix))








########################## UTILS ##########################

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


######################### RUNNER #########################

def main():

    ### VARIABLES ############
    k = 21  # K-mer length
    genome_file = './data/chm13_chr22.fa' 
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
        
        # # Step 3: Initialize the trie with all k-mers and time the construction
        # start_time = time.perf_counter()
        
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
        
        # end_time = time.perf_counter()
        # construction_time = end_time - start_time
        
        # # Measure the size of the trie
        # trie_size = asizeof.asizeof(trie)
        
        # Step 4: Test different prefix lengths
        for prefix_length in range(1, max_prefix_length + 1):
            # Generate random prefixes of the specified length by sampling from 'A', 'C', 'T', 'G'
            test_prefixes = [
                ''.join(random.choices(['A', 'C', 'T', 'G'], k=prefix_length))
                for _ in range(num_test_prefixes)
            ]
            
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
                # "Construction Time (s)": construction_time,
                # "Trie Size (bytes)": trie_size,
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