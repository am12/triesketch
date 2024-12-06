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
