from pyfaidx import Fasta
from tqdm import tqdm
from triesketch.utils import *

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
            obj.insert(kmer)

    print(f"All {k}-mers have been added to the object.")

# runner
def main():
        
    genome_file = "./data/phiX174_phage.fasta" 
    tries, names = get_tries()
    k = 21  # Set your desired k-mer length
    
    for trie, name in zip(tries, names):
        print(f"Building index for {name}...")
        build_kmer_index(genome_file, trie, k)
        print(f"Index built for {name}.\n")
    
if __name__ == "__main__":
    main()
