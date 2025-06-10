#!/bin/bash
#SBATCH --mail-user=torben.sanders@helmholtz-munich.de
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --job-name=run_phylo
#SBATCH --output=tree.out
#SBATCH --error=tree.err
#SBATCH -p cpu_p
#SBATCH --qos cpu_long
#SBATCH --ntasks=1
#SBATCH -c 20
#SBATCH --mem=125G  # Adjust memory as needed
#SBATCH --time=6-23:59:59  # Adjust time limit as needed
#SBATCH --nice=10000

source $HOME/.bashrc

# data
data_path=$HOME/corinna/all_bacteria.fasta
output_path=$HOME/corinna/all_bacteria_aligned.fasta
output_tree=$HOME/corinna/all_bacteria.nw
# Load necessary modules
conda activate phylo_tree
echo Successfully loaded conda environment and starting pipeline
mugsy --directory $HOME/corinna --prefix all_bacterial_genomes_aligned 50071.fasta pa3.fasta pa4.fasta pa8.fasta pa13.fasta
echo Alignment finished
fasttree -nt $output_path > $output_tree
echo Finished
