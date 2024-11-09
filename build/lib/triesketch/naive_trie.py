class TrieNode:
    def __init__(self, key="", is_end_of_word=False):
        self.key = key
        self.children = []
        self.is_end_of_word = is_end_of_word

    def find_child(self, char):
        for child in self.children:
            if child.key == char:
                return child
        return None

class NaiveTrie:
    def __init__(self):
        self.root = TrieNode()
    
    def __name__(self):
        return "NaiveTrie"

    def insert(self, word):
        current = self.root
        while word:
            for child in current.children:
                if word.startswith(child.key):
                    prefix_length = len(child.key)
                    word = word[prefix_length:]
                    current = child
                    break
            else:
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
                    prefix_length = len(child.key)
                    word = word[prefix_length:]
                    current = child
                    found = True
                    break
            if not found:
                return False
        return current.is_end_of_word

    def delete(self, word):
        """
        Deletes a word from the Trie if it exists.
        Returns True if the word was deleted, False if the word was not found.
        """
        return self._delete_recursive(self.root, word)

    def _delete_recursive(self, current, word):
        if not word:
            # Reached the end of the word
            if not current.is_end_of_word:
                return False  # Word not found
            current.is_end_of_word = False  # Unmark the end of the word
            # If current node has no children, indicate it can be removed
            return len(current.children) == 0

        # Recursive case: traverse down the Trie
        char = word[0]
        child = current.find_child(char)
        if not child:
            return False  # Word not found

        # Proceed to the next character
        can_delete_child = self._delete_recursive(child, word[len(child.key):])

        # If the child can be deleted, remove it from the children list
        if can_delete_child:
            current.children.remove(child)
            # Check if current node can now be deleted
            return not current.is_end_of_word and len(current.children) == 0

        return False