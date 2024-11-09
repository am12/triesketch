import pytrie

class Trie:
    def __init__(self):
        # Using pytrie.StringTrie to store words
        self.trie = pytrie.StringTrie()

    def __name__(self):
        return "Trie"

    def insert(self, word, value=True):
        """
        Inserts a word into the trie with a default value.
        
        Parameters:
        - word (str): The word to insert.
        - value (any): The value associated with the word. Defaults to True.
        """
        self.trie[word] = value

    def search(self, word):
        """
        Searches for a word in the trie.
        
        Parameters:
        - word (str): The word to search for.

        Returns:
        - any: The value associated with the word if it exists, raises KeyError if not found.
        """
        return self.trie[word]  # Will raise KeyError if the word does not exist

    def delete(self, word):
        """
        Deletes a word from the trie if it exists.
        
        Parameters:
        - word (str): The word to delete.

        Returns:
        - bool: True if the word was deleted, False if the word was not found.
        """
        if word in self.trie:
            del self.trie[word]
            return True
        return False

# # Example usage
# trie = Trie()

# # Insert words
# trie.insert("apple")
# trie.insert("app")

# # Search for words
# print(trie.search("apple"))  # Output: True
# print(trie.search("app"))    # Output: True

# # Delete a word
# print(trie.delete("app"))    # Output: True
# print(trie.delete("app"))    # Output: False (already deleted)