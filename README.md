# Trie-Based Phylogenetic Distance Calculation
Group 4a Final Project
Explore two trie-baesd algorithms that enable comparison of genomes to reveal how closely related they are (phylogenetic distance). We benchmarked 6 trie data structures, ultimately settling on PatriciaTries for the algorithms.

## How to Run
### Our Trie-Based Algorithm Examples
#### Generate SARS-CoV-2 Genomes Dataset Phylogenetic Tree
Run run_covid_example.py to calculate distance matrices and generate phylogenetic trees for the SARS-CoV-2 genomes. The SARS-CoV-2 genomes files can be found under ./data/covid .
#### Generate Animals Genomes Phylogenetic Tree
Run run_animals_example.py to calculate distance matrices and generate phylogenetic trees for the various animal genomes. The animal genomes files can be found under ./data/animal_data_set .
### Compare Against Mash and Dashing
#### Mash
Run mash_script.sh to generate the distance matrices for the SARS-CoV-2 Genomes and animals datasets. Store the files into ./distance_matrices and run mash_and_dashing_tree_construction.py to create the phylogenetic trees.