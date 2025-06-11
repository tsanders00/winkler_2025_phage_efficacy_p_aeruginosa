#!/bin/bash
#SBATCH -J 15
#SBATCH -o alphafold_out_15
#SBATCH -e alphafold_error_15
#SBATCH -t 1-23:00:00 # Set to 2 days
#SBATCH --nodelist=supergpu08

#SBATCH -p gpu_p
#SBATCH --qos gpu_normal
#SBATCH --gres=gpu:1

#SBATCH --ntasks=1
#SBATCH -c 19
#SBATCH --mem=100G
#SBATCH --nice=10000

### set source 
source $HOME/.bashrc

### activate conda env
conda activate speed_ppi_dev

# Fasta with sequences to use for alphafold2
OUTDIR="$HOME/tiamani/phages_vs_bacterias"

# Path to individual fasta seqs created in step 1 for the protein lists
FASTADIR1="$HOME/tiamani/phages_vs_bacterias/fasta1"
FASTADIR2="$HOME/tiamani/phages_vs_bacterias/fasta2"

# DEFAULT
UNICLUST=./data/uniclust30_2018_08/uniclust30_2018_08 #Assume path according to setup

#The pipeline starts here
#3. Predict the structure using a modified version of AlphaFold2 (FoldDock)
PR_CSV1=$FASTADIR1/id_seqs.csv
PR_CSV2=$FASTADIR2/id_seqs.csv
NUM_PREDS=$(wc -l "$HOME/tiamani/phages_vs_bacterias/fasta1/id_seqs.csv"|cut -d ' ' -f 1)
DATADIR="$HOME/test_speedppi/SpeedPPI/data/"
RECYCLES=10
NUM_CPUS=17
PDOCKQ_T=0.5
MSADIR="$OUTDIR/msas/"

for (( c=1; c<=$NUM_PREDS; c++ ))
do
  echo Running pred $c out of $NUM_PREDS
  python3 "$HOME/test_speedppi/SpeedPPI/src/run_alphafold_some_vs_some.py" --protein_csv1 $PR_CSV1 \
  --protein_csv2 $PR_CSV2 \
    --target_row $c \
    --msa_dir $MSADIR \
    --data_dir $DATADIR \
    --max_recycles $RECYCLES \
    --pdockq_t $PDOCKQ_T \
    --num_cpus $NUM_CPUS \
    --output_dir "$OUTDIR/pred/"
done

