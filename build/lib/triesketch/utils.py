from triesketch.dictionary import Dictionary
from triesketch.naive_trie import NaiveTrie
from triesketch.trie import Trie
from triesketch.patricia_trie import PatriciaTrie
from triesketch.pytricia_trie import PytriciaTrie
from triesketch.marisa_trie import MarisaTrie

# NOTE: Marisa trie is static, so cannot add or remove from it without creating a new trie
def get_tries():
    """
    Returns a list of Trie objects for testing.
    """
    return [Dictionary(), NaiveTrie(), Trie(), PatriciaTrie(), PytriciaTrie(), MarisaTrie()], ["Dictionary", "NaiveTrie", "Trie", "PatriciaTrie", "PytriciaTrie", "MarisaTrie"]

def read_genome_file(filename):
    """
    Reads a genome file in FASTA format and returns a list of sequences.
    
    Parameters:
    - filename (str): The path to the genome file.
    
    Returns:
    - sequences (list of str): A list of genome sequences.
    """
    sequences = []
    with open(filename, 'r') as file:
        seq = ''
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if line.startswith('>'):
                if seq:
                    sequences.append(seq)
                    seq = ''
            else:
                seq += line.upper()  # Convert to uppercase for consistency
        if seq:
            sequences.append(seq)
    return sequences

def generate_kmers(sequences, k):
    """
    Generates all k-mers of length k from the given sequences.
    
    Parameters:
    - sequences (list of str): The list of sequences to generate k-mers from.
    - k (int): The length of each k-mer.
    
    Returns:
    - kmers (set of str): A set containing all unique k-mers.
    """
    kmers = set()
    for seq in sequences:
        seq_length = len(seq)
        if seq_length < k:
            continue  # Skip sequences shorter than k
        for i in range(seq_length - k + 1):
            kmer = seq[i:i+k]
            kmers.add(kmer)
    return kmers
