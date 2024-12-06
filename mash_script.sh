#!/bin/bash

mash sketch -o all_sketch ./data/covid/*.fasta

mash dist all_sketch.msh all_sketch.msh > mash_distance_matrix.txt

mash sketch -o animal_sketch ./data/animal_data_set/*.fasta

mash dist animal_sketch.msh animal_sketch.msh > mash_animal_distance_matrix.txt

