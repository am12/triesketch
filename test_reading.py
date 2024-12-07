from triesketch.utils import read_genome_file


genome_file = './correct_data_sets/MZ169912.txt'

sequences = read_genome_file(genome_file)
if not sequences:
    print(f"Error: No sequences found in '{genome_file}'.")