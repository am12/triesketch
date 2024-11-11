from triesketch.dictionary import Dictionary
from triesketch.naive_trie import NaiveTrie
from pytrie import Trie
from triesketch.patricia_trie import PatriciaTrie
from marisa_trie import Trie as MarisaTrie
# from datrie import Trie as DATrie

# NOTE: Marisa trie is static, so cannot add or remove from it without creating a new trie
def get_tries():
    """
    Returns a list of Trie objects for testing.
    """
    return [Dictionary(), NaiveTrie(), Trie(), PatriciaTrie(), MarisaTrie()], ["Dictionary", "NaiveTrie", "Trie", "PatriciaTrie", "MarisaTrie"]

