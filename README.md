# Trie-Based Phylogenetic Distance Calculation
Group 4a: Renee Cai, Emma Dionne, Alan Mao, Amy Xing
## Project Overview
Our goal is to develop an efficient trie-based method to calculate the degree of relatedness (phylogenetic distance) between different genomes, leveraging their unique prefix-matching property, predictable search complexity, and efficient compression of smaller genetic alphabets. 

We first conduct an exploration of six trie-based data structures for storing k-mers, benchmarking their time and memory usages, and other special considerations. Then, we explore two novel, trie-baesd algorithms that enable comparison of genomes to reveal phylogenetic distance. 

## How to Run
### Installation
We used a Miniconda3 environment, containing the packages listed in the `trie.yaml` file. It may be useful to run `conda env create -f trie.yaml` to install all the packages. Ensure you run `pip install .` to install the `triesketch` package, which includes all of the custom-built and wrapped data structures we benchmarked.

### Trie Construction Benchmark (`tests/1_build_index/`)
Our first results are from the benchmark experiments in the above folder. Run `initialize.py  ` to run the benchmark, then `initialize_viz.py` to create the graphs.

### Trie Query Benchmark (`tests/2_query_kmers/`)
Run `query.py` and then `query_viz.py` to visualize the results. We run `query_scalene.py` using the `scalene` command-line tool to perform line-by-line profiling, which you may find helpful. 

### Distance Calculation (`tests/3_phylogenetic_distance/`)
#### Our Patricia Trie Algorithm
Run `run_covid_example.py` to calculate distance matrices and generate phylogenetic trees for the SARS-CoV-2 genomes. The SARS-CoV-2 genomes files can be found under `./data/covid`.

Run `run_animals_example.py` to calculate distance matrices and generate phylogenetic trees for the various animal genomes. The animal genomes files can be found under `./data/animal_data_set`.
#### Mash
Ensure you have installed [`mash`](https://mash.readthedocs.io/en/latest/) on your system using the proper pathways. 

Run `mash_script.sh` to generate the distance matrices for the SARS-CoV-2 Genomes and animals datasets. Store the files into `./distance_matrices` and run `mash_and_dashing_tree_construction.py` to create the phylogenetic trees.

#### Dashing2
Ensure you have installed [`dashing2`](https://github.com/dnbaker/dashing2?tab=readme-ov-file#installation) on your system using the proper pathways. 

Run the `dashing_all.sh` script to generate all the results for Dashing2.