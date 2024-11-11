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