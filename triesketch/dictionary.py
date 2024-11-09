class Dictionary():
    def __init__(self):
        self.dict = {}
        
    def __name__(self):
        return "Dictionary"

    def insert(self, word):
        self.dict[word] = self.dict.get(word, 0) + 1

    def search(self, word):
        return self.dict[word]
        
    def delete(self, word):
        self.dict[word] = self.dict.get(word, 1) - 1