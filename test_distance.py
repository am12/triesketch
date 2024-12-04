from distance_calc import mash_dist
from triesketch.patricia_trie import PatriciaTrie
seq = 'AGCT'
kmer_1 = ['AG', 'GC']
kmer_2 = ['GC', 'CT']
pytrie_1 = PatriciaTrie(kmer_1)
pytrie_2 = PatriciaTrie(kmer_2)
dist_a = mash_dist(pytrie_1, pytrie_2, 2, jaccard_sim_a = True)
print(dist_a)