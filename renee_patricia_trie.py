class PatriciaTrieNode():
    def __init__(self, key=""):
        self.key = key
        self.children = {}
        self.is_end_of_word = False

class PatriciaTrie():
    def __init__(self):
        self.root = PatriciaTrieNode()

    def insert(self, word):
        current = self.root
        while word:
            found = False
            for key in list(current.children.keys()):
                common_prefix_length = self._common_prefix_length(word, key)
                
                if common_prefix_length > 0:
                    # Case 1: If the common prefix is shorter than the existing key, split the node
                    if common_prefix_length < len(key):
                        existing_node = current.children.pop(key)
                        new_node = PatriciaTrieNode(key[:common_prefix_length])
                        current.children[new_node.key] = new_node
                        new_node.children[key[common_prefix_length:]] = existing_node
                        existing_node.key = key[common_prefix_length:]

                    # Case 2: Update current node to handle the new word
                    current = current.children[key[:common_prefix_length]]
                    word = word[common_prefix_length:]

                    # Case 3: If the word length matches, mark it as an end of word
                    if not word:
                        current.is_end_of_word = True
                    else:
                        # Create a new node for the remaining part of the word
                        if word not in current.children:
                            current.children[word] = PatriciaTrieNode(word)
                            current.children[word].is_end_of_word = True
                    return
                
            # Case 4: If no common prefix, add the word as a new child
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
    
    def print_trie(self, node=None, indent=""):
        if node is None:
            node = self.root

        # Indicate if this is the end of a word
        end_marker = "(End of Word)" if node.is_end_of_word else ""
        print(f"{indent}{node.key} {end_marker}")

        # Recurse for each child with increased indentation
        for child_key, child_node in node.children.items():
            print("error")
            self.print_trie(child_node, indent + "    ")


    def print_trie_to_list(self, node=None, key_list=None, indent = ""):
        if node is None:
            node = self.root
        if key_list is None:
            key_list = []

        end_marker = "(End of Word)" if node.is_end_of_word else ""
        key_list.append(f"{indent}{node.key} {end_marker}")
        #if node.is_end_of_word:
        #    key_list.append(node.key)  # Append the key if it's an end-of-word node

        for child_key, child_node in node.children.items():
            self.print_trie_to_list(child_node, key_list, indent + "    ")