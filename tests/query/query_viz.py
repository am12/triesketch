import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_process_data(csv_file):
    """
    Load the CSV file, compute average prefix search and prefix count times across all prefixes.
    
    Parameters:
    - csv_file (str): Path to the CSV file containing benchmark results.
    
    Returns:
    - pd.DataFrame: DataFrame with average times for prefix search and count per Trie Type.
    """
    # Load data
    df = pd.read_csv(csv_file)

    # Group by Trie Type and compute the mean search and count times across all prefixes
    df_avg = df.groupby("Trie Type").agg({
        "Prefix Search Time (s)": "mean",
        "Prefix Count Time (s)": "mean"
    }).reset_index()

    return df_avg

def plot_prefix_search_time(df):
    """
    Plot the average prefix search time for each trie type.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing average query times.
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Trie Type", y="Prefix Search Time (s)", palette="viridis")
    plt.title("Average Prefix Search Time by Trie Type")
    plt.ylabel("Average Search Time (s)")
    plt.xlabel("Trie Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("average_prefix_search_time.png")
    plt.show()

def plot_prefix_count_time(df):
    """
    Plot the average prefix count time for each trie type.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing average query times.
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Trie Type", y="Prefix Count Time (s)", palette="viridis")
    plt.title("Average Prefix Count Time by Trie Type")
    plt.ylabel("Average Count Time (s)")
    plt.xlabel("Trie Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("average_prefix_count_time.png")
    plt.show()

def main():
    # Load and process the data
    csv_file = './tests/query_benchmark/query_results.csv'
    df_avg = load_and_process_data(csv_file)

    # Plot average prefix search time
    plot_prefix_search_time(df_avg)

    # Plot average prefix count time
    plot_prefix_count_time(df_avg)

if __name__ == "__main__":
    main()