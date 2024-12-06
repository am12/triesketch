from triesketch.utils import read_genome_file


genome_file = './data/covid/MZ169912.fasta'

sequences = read_genome_file(genome_file)
if not sequences:
    print(f"Error: No sequences found in '{genome_file}'.")
else:
    print(sequences)