import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_process_data(csv_file):
    """
    Load the CSV file containing benchmark results.
    
    Parameters:
    - csv_file (str): Path to the CSV file containing benchmark results.
    
    Returns:
    - pd.DataFrame: DataFrame with benchmark results ready for plotting.
    """
    # Load data
    df = pd.read_csv(csv_file)

    # Group by Trie Type and Prefix Length to calculate average search and count times
    df_avg = df.groupby(["Trie Type", "Prefix Length"]).agg({
        "Average Prefix Search Time (s)": "mean",
        "Average Prefix Count Time (s)": "mean"
    }).reset_index()

    return df_avg

def plot_prefix_search_time(df):
    """
    Plot the average prefix search time against prefix length for each trie type.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing benchmark results.
    """
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="Prefix Length", y="Average Prefix Search Time (s)", hue="Trie Type", marker="o")
    plt.title("Average Prefix Search Time")
    plt.ylabel("Average Search Time (s)")
    plt.xlabel("Prefix Length")
    plt.legend(title="Trie Type")
    plt.xticks(range(1, 22))  # Set x-ticks from 1 to 21
    plt.tight_layout()
    plt.savefig("average_prefix_search_time_line.png")
    plt.show()

def plot_prefix_count_time(df):
    """
    Plot the average prefix count time against prefix length for each trie type.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing benchmark results.
    """
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="Prefix Length", y="Average Prefix Count Time (s)", hue="Trie Type", marker="o")
    plt.title("Average Prefix Count Time")
    plt.ylabel("Average Count Time (s)")
    plt.xlabel("Prefix Length")
    plt.legend(title="Trie Type")
    plt.xticks(range(1, 22))  # Set x-ticks from 1 to 21
    plt.tight_layout()
    plt.savefig("average_prefix_count_time_line.png")
    plt.show()

def main():
    # Load and process the data
    csv_file = './tests/query/partition_10/query_results_avg.csv'
    df_avg = load_and_process_data(csv_file)

    # Plot average prefix search time against prefix length
    plot_prefix_search_time(df_avg)

    # Plot average prefix count time against prefix length
    plot_prefix_count_time(df_avg)

if __name__ == "__main__":
    main()