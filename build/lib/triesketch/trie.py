import pytrie

# draws from idea of radix tries
class Trie:
    def __init__(self, keys=None):
        """
        Initializes the trie. If a list of keys is provided, inserts them into the trie.
        
        Parameters:
        - keys (list of str, optional): The list of words to initialize the trie with.
        """
        # Using pytrie.StringTrie to store words
        if keys:
            # Initialize the trie with the given keys and default value True
            key_values = {key: True for key in keys}
            self.trie = pytrie.StringTrie(key_values)
        else:
            self.trie = pytrie.StringTrie()

    def __name__(self):
        return "Trie"

    def insert(self, word, value=True):
        """
        Inserts a word into the trie with a default value.
        
        Parameters:
        - word (str): The word to insert.
        - value (any, optional): The value associated with the word. Defaults to True.
        """
        self.trie[word] = value

    def search(self, word):
        """
        Searches for a word in the trie.
        
        Parameters:
        - word (str): The word to search for.

        Returns:
        - any: The value associated with the word if it exists.
        - None: If the word does not exist in the trie.
        """
        return self.trie.get(word, None)

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