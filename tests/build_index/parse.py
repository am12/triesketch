import re
import pandas as pd

# Sample multiline string (log output) for demonstration purposes
log_data = open('results.txt', 'r').read()

def parse_log_data(log_data):
    # Regular expressions to capture fields
    file_pattern = re.compile(r"Loaded 1 sequences from '(.*?)'")
    kmer_pattern = re.compile(r"Generated (\d+) unique 21-mers from the genome sequences.")
    trie_pattern = re.compile(r"(Dictionary|\w+Trie|Trie) initialized with \d+ k-mers.")
    time_pattern = re.compile(r"Trie construction time: ([\d.]+) seconds")
    size_pattern = re.compile(r"Total size of trie: (\d+) bytes")

    # List to store parsed data as dictionaries
    data = []

    # Split the log data by lines and iterate over each line
    lines = log_data.strip().split("\n")
    for i in range(0, len(lines), 5):  # Process in chunks of 5 lines per entry
        try:
            # Match each pattern to the appropriate line
            genome_file = file_pattern.search(lines[i]).group(1)
            kmer_count = int(kmer_pattern.search(lines[i + 1]).group(1))
            trie_type = trie_pattern.search(lines[i + 2]).group(1)
            construction_time = float(time_pattern.search(lines[i + 3]).group(1))
            trie_size = int(size_pattern.search(lines[i + 4]).group(1))

            # Extract percentage from genome file path (e.g., '1' from './data/chr22_parts/1.fa')
            input_size_percentage = int(re.search(r'(\d+)\.fa', genome_file).group(1))

            # Append parsed values to the data list as a dictionary
            data.append({
                "Genome File": genome_file,
                "Input Size (%)": input_size_percentage,
                "Trie Type": trie_type,
                "Construction Time (s)": construction_time,
                "Trie Size (bytes)": trie_size,
                "Number of k-mers": kmer_count
            })

        except AttributeError:
            # If there's a missing field or an unmatched pattern, skip this entry
            print(f"Warning: Could not parse entry starting at line {i}")

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)
    return df

# Parse the log data and print the resulting DataFrame
df = parse_log_data(log_data)
df.to_csv('initialize_results.csv', index=False)