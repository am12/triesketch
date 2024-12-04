from distance_calc import mash_dist
from triesketch.patricia_trie import PatriciaTrie

#test algorithm a
seq = 'AGCT'
kmer_1 = ['AGC', 'GCC']
kmer_2 = ['GCC', 'CTC']
pytrie_1 = PatriciaTrie(kmer_1)
pytrie_2 = PatriciaTrie(kmer_2)
dist_a = mash_dist(pytrie_1, pytrie_2, 2, jaccard_sim_a = True)
print(dist_a)

#test algorithm b
kmer_1 = ['ATCC', 'ATAC', 'ATGC', 'ATTC', 'ATAG'] 
kmer_2 = ['ATCC', 'ATAC', 'ATTG', 'ATGG', 'CTTT', 'CTTA', 'CTTC']
pytrie_1 = PatriciaTrie(kmer_1)
pytrie_2 = PatriciaTrie(kmer_2)
dist_b = mash_dist(pytrie_1, pytrie_2, 2, jaccard_sim_a = False)
print(dist_b)
