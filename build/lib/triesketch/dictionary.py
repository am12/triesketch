class Dictionary:
    def __init__(self):
        self._data = {}
    
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