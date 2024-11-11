class Dictionary:
    def __init__(self, keys=None):
        """
        Initializes the dictionary. If a list of keys is provided, inserts them into the dictionary.

        Parameters:
        - keys (list of str, optional): The list of keys to initialize the dictionary with.
        """
        self._data = {}
        if keys:
            for key in keys:
                self._data[key] = True  # Value is arbitrary; we're only tracking existence

    def __name__(self):
        """Return the name of the class."""
        return self.__class__.__name__

    def insert(self, key):
        """Insert a key into the dictionary."""
        self._data[key] = True  # Value is arbitrary; we're only tracking existence

    def delete(self, key):
        """Delete a key from the dictionary."""
        self._data.pop(key, None)

    def search(self, key):
        """Search for a key in the dictionary. Returns True if found, False otherwise."""
        return key in self._data

# # List of keys to initialize the dictionary with
# keys = ["apple", "banana", "cherry", "date", "elderberry"]

# # Initialize the dictionary with the list of keys
# my_dict = Dictionary(keys=keys)

# # Search for keys
# print(my_dict.search("apple"))       # Output: True
# print(my_dict.search("banana"))      # Output: True
# print(my_dict.search("fig"))         # Output: False (not found)

# # Insert a new key
# my_dict.insert("fig")
# print(my_dict.search("fig"))         # Output: True

# # Delete a key
# my_dict.delete("banana")
# print(my_dict.search("banana"))      # Output: False (since it's deleted)