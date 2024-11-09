class TrieNode():
    def __init__(self, key="", is_end_of_word=False):
        self.key = key
        self.children = []
        self.is_end_of_word = is_end_of_word
    def find_child(self, char):
        for child in self.children:
            if child.key == char:
                return child
        return None

class Trie():
    def __init__(self):
        self.root = TrieNode()
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
        ...