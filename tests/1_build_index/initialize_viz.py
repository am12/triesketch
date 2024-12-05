import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(csv_file):
    """
    Load the benchmark data from a CSV file, converting Genome File to percentage size and 
    converting Trie Size from bytes to megabytes (MB).
    
    Parameters:
    - csv_file (str): Path to the CSV file containing benchmark results.
    
    Returns:
    - pd.DataFrame: DataFrame containing the benchmark results with input size as percentage.
    """
    df = pd.read_csv(csv_file)

    # Convert Trie Size from bytes to MB
    df["Trie Size (MB)"] = df["Trie Size (bytes)"] / (1024 ** 2)

    # Optionally: extract percentage size from the Genome File name
    df['Input Size (%)'] = df['Genome File'].str.extract(r'(\d+)\.fa').astype(float)
    
    return df

def plot_construction_time(df):
    """
    Plot the construction time for each trie type across different input sizes.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing benchmark results.
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="Input Size (%)", y="Construction Time (s)", hue="Trie Type", marker="o")
    plt.title("Trie Construction Time")
    plt.ylabel("CPU Time (s)")
    plt.xlabel("Input Size (% of CHM13-Chr22)")
    plt.legend(title="Trie Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("trie_construction_time_line.png")
    plt.show()

def plot_memory_usage(df):
    """
    Plot the memory usage for each trie type across different input sizes, in MB.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing benchmark results.
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="Input Size (%)", y="Trie Size (MB)", hue="Trie Type", marker="o")
    plt.title("Trie Memory Usage")
    plt.ylabel("Memory Usage (MB)")
    plt.xlabel("Input Size (% of CHM13-Chr22)")
    plt.legend(title="Trie Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("trie_memory_usage_line.png")
    plt.show()

def main():
    # Load the data
    csv_file = 'initialize_results.csv'
    df = load_data(csv_file)

    # Plot construction time
    plot_construction_time(df)

    # Plot memory usage
    plot_memory_usage(df)

if __name__ == "__main__":
    main()