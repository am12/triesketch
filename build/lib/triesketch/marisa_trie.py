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
        

# # Initialize the trie
# trie = MarisaTrie(keys=["apple", "banana", "cherry"])

# # Insert multiple words
# trie.insert_many(["date", "elderberry", "fig"])

# # Search for words
# print(trie.search("date"))       # Output: True
# print(trie.search("elderberry")) # Output: True
# print(trie.search("fig"))        # Output: True

# # Delete multiple words
# trie.delete_many(["banana", "cherry"])

# # Search for deleted words
# print(trie.search("banana"))     # Output: False
# print(trie.search("cherry"))     # Output: False