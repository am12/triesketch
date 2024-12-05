from triesketch.utils import *



def main():
    names = ["MZ169912", "MZ219592", "MW913395", "LC623948", "MW981442", "MZ202314", "MW789246", "MZ277392"]
    #read in files
    genome_files = [f'./data/chr22_parts/{i}.fa' for i in range(1,11)] #change this for actual data
    final_dict = {}
    
    kmer_length = 21
    
    for genome_file in genome_files:
        sequences = read_genome_file(genome_file)
        if not sequences:
            print(f"Error: No sequences found in '{genome_file}'.")
            continue
        kmers = generate_kmers(sequences, kmer_length)
        trie = PatriciaTrie(keys=kmers)
        final_dict[]
    k_values = [3, 5] #can change to the values we want to test

    for k in k_values:
        