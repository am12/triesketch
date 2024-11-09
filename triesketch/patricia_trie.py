class PatriciaTrieNode():
    def __init__(self, key=""):
        self.key = key
        self.children = {}
        self.is_end_of_word = False

class PatriciaTrie():
  def  __init__(self):
    self.root = PatriciaTrieNode()
  def insert(self, word):
    current = self.root
    while word:
      for key in list(current.children.keys()):
        common_prefix_length = self._common_prefix_length(word, key)
        if common_prefix_length > 0:
          if common_prefix_length < len(key):
            existing_node = current.children.pop(key)
            new_node = PatriciaTrieNode(key[:common_prefix_length])
            current.children[new_node.key] = new_node
            new_node.children[key[common_prefix_length:]] = existing_node
            existing_node.key = key[common_prefix_length:]

            if common_prefix_length == len(word):
              new_node.is_end_of_word = True
            else:
              new_node.children[word[common_prefix_length:]] = PatriciaTrieNode(word[common_prefix_length:])
              new_node.children[word[common_prefix_length:]].is_end_of_word = True
            return
            word = word[common_prefix_length:]
            current = current.children[key]
            break
        else:
          current.children[word] = PatriciaTrieNode(word)
          current.children[word].is_end_of_word = True
          return

  def search(self, word):
    current = self.root
    while word:
      found = False
      for key, node in current.children.items():
        if word.startswith(key):
          if len(key) == len(word):
            return node.is_end_of_word
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
          return False
        node.is_end_of_word = False
        return len(node.children) == 0

      for key, child in list(node.children.items()):
        if word.startswith(key):
          if _delete(child, word[len(key):]):
            del node.children[key]
            return not node.is_end_of_word and len(node.children) == 0
          return False
      return False

    _delete(self.root, word)

  def _common_prefix_length(self, str1, str2):
    i = 0
    while i < len(str1) and i < len(str2) and str1[i] == str2[i]:
      i += 1
    return i