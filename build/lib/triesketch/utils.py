from triesketch.dictionary import Dictionary
from triesketch.naive_trie import NaiveTrie
from triesketch.trie import Trie
from triesketch.patricia_trie import PatriciaTrie
from triesketch.pytricia_trie import PytriciaTrie
from triesketch.marisa_trie import MarisaTrie
# from datrie import Trie as DATrie

# NOTE: Marisa trie is static, so cannot add or remove from it without creating a new trie
def get_tries():
    """
    Returns a list of Trie objects for testing.
    """
    return [Dictionary(), NaiveTrie(), Trie(), PatriciaTrie(), PytriciaTrie(), MarisaTrie()], ["Dictionary", "NaiveTrie", "Trie", "PatriciaTrie", "PytriciaTrie", "MarisaTrie"]

