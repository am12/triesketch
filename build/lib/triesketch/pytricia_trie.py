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
        return "PatriciaTrie"

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