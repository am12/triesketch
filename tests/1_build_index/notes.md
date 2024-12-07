# aim
test various trie-like data structures in their ability to build an index from k-mers of a genome:
- python dictionary (Dictionary)
- marisa-trie package (MarisaTrie)
- naive trie, from class with slight optimizations (NaiveTrie)
- patricia-trie package (PytriciaTrie)
- trie package, a basic rl-compressed string trie (Trie)
- our implementation of patricia trie (PatriciaTrie)
measured time and memory usage
used increasing partitions of CHM13 chr22 (1-10%) to see growth over input size

