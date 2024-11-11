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