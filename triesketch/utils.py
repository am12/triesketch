from triesketch.dictionary import Dictionary
from triesketch.naive_trie import NaiveTrie
from pytrie import Trie
from triesketch.patricia_trie import PatriciaTrie
from marisa_trie import Trie as MarisaTrie
# from datrie import Trie as DATrie


def get_tries():
    """
    Returns a list of Trie objects for testing.
    """
    return [Dictionary(), NaiveTrie(), Trie(), PatriciaTrie(), MarisaTrie()], ["Dictionary", "NaiveTrie", "Trie", "PatriciaTrie", "MarisaTrie"]