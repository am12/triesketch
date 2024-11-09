from pyfaidx import Fasta
from patricia import trie
from tqdm import tqdm
from triesketch import * 
from renee_patricia_trie import PatriciaTrie
import sys

# loading k-mers from index into the sketch
def build_kmer_index(genome_file, obj, k):
    """
    Reads a genome file, extracts all k-mers of length k, and adds them to the given object.
    
    Parameters:
    genome_file (str): Path to the genome file in FASTA format.
    obj (object): An object with `insert`, `search`, and `delete` methods.
    k (int): Length of k-mer to extract and add to the object.
    """
    # Open the genome file with pyfaidx
    genome = Fasta(genome_file)

    # Loop over each chromosome or sequence in the genome file
    for record in genome:
        sequence = str(record)  # Get the sequence as a string
        seq_len = len(sequence) - k + 1  # Number of k-mers in this sequence

        # Use tqdm to show progress for the k-mer extraction
        for i in tqdm(range(seq_len), desc=f"Processing {record.name}"):
            kmer = sequence[i:i + k]
            #print(kmer)
            obj.insert(kmer)
    print(f"All {k}-mers have been added to the object.")
    
    
patricia_trie = PatriciaTrie()

    
genome_file = "phiX174_phage.fasta"  # Path to your phage genome file
k = 21  # Set your desired k-mer length

build_kmer_index(genome_file, patricia_trie, k)

#patricia_trie.print_trie()

def build_kmer_index_python(genome_file, obj, k):
    """
    Reads a genome file, extracts all k-mers of length k, and adds them to the given object.
    
    Parameters:
    genome_file (str): Path to the genome file in FASTA format.
    obj (object): An object with `insert`, `search`, and `delete` methods.
    k (int): Length of k-mer to extract and add to the object.
    """
    # Open the genome file with pyfaidx
    genome = Fasta(genome_file)

    # Loop over each chromosome or sequence in the genome file
    for record in genome:
        sequence = str(record)  # Get the sequence as a string
        seq_len = len(sequence) - k + 1  # Number of k-mers in this sequence

        # Use tqdm to show progress for the k-mer extraction
        for i in tqdm(range(seq_len), desc=f"Processing {record.name}"):
            kmer = sequence[i:i + k]
            #print(kmer)
            obj[kmer] = True
    print(f"All {k}-mers have been added to the object.")

    genome_file = "phiX174_phage.fasta"  # Path to your phage genome file

python_patricia_trie = trie()

k = 21  # Set your desired k-mer length

build_kmer_index_python(genome_file, python_patricia_trie, k)

#patricia_trie.print_trie()

#for kmer, value in python_patricia_trie.items():
#    print(kmer)



custom_kmers = []
patricia_trie.print_trie_to_list()  # Modify your print_trie method to append keys

# Print patricia-trie keys as a flat list
patricia_kmers = list(python_patricia_trie.keys())

# Compare the two lists
print("Comparing custom Patricia Trie and patricia-trie:")
print("Custom Patricia Trie kmers:", custom_kmers)
print("Patricia Trie kmers from the package:", patricia_kmers)

# You can also compare the two directly using set operations
if set(custom_kmers) == set(patricia_kmers):
    print("Both tries contain the same k-mers.")
else:
    print("The k-mers differ between the custom Patricia Trie and the patricia-trie package.")