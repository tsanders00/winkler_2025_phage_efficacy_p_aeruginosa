#!/bin/bash
#SBATCH -J hhblits_parallel
#SBATCH -o hhblits_out
#SBATCH -e hhblits_error
#SBATCH -t 08:00:00 # Set at 8 hours
#SBATCH --ntasks=1
#SBATCH -p cpu_p
#SBATCH --qos cpu_normal

#SBATCH --cpus-per-task=2 # How many CPUs to use
#SBATCH --mem-per-cpu=2500 # Memory in Mb per CPU
#SBATCH --array=0-15 # Number of batches (0 to 15 for 16 batches)
#SBATCH --nice=10000

### load the modules
source $HOME/.bashrc

### activate conda env
conda activate speed_ppi_dev


### set the total number of proteins and the number of proteins per batch
TOTAL_PROTEINS=740
PROTEINS_PER_BATCH=46

### calculate the starting and ending index for the current batch
START_INDEX=$((SLURM_ARRAY_TASK_ID * PROTEINS_PER_BATCH))
END_INDEX=$((START_INDEX + PROTEINS_PER_BATCH - 1))

### Adjust the end index if it exceeds the total number of proteins
if [ $END_INDEX -ge $TOTAL_PROTEINS ]; then 
    END_INDEX=$((TOTAL_PROTEINS - 1))
fi


### Fasta with sequences to use for the PPI network
OUTDIR="$HOME/tiamani/phages_vs_bacterias"
MSADIR="$OUTDIR/msas"
FASTADIR="$HOME/tiamani/phages_vs_bacterias/fasta2"
HHBLITS="$HOME/test_speedppi/SpeedPPI/hh-suite/bin/hhblits"
UNICLUST="$HOME/test_speedppi/SpeedPPI/data/uniclust30_2018_08/uniclust30_2018_08"
IDS="$HOME/tiamani/phages_vs_bacterias/fasta2/id_seqs.csv"

### Loop through the protein IDs for the current batch
for ((i=START_INDEX; i<=END_INDEX; i++))
do
    ### Calculate the line number in the protein ID file
    LINE_NUMBER=$((i + 1))

    ### Get the protein ID from the id_seqs.csv file
    ID=$(sed -n "${LINE_NUMBER}p" "$IDS" | cut -d ',' -f1)
    FASTA="$FASTADIR/$ID.fasta"

    ### Run HHblits to create MSA
    if [ -f "$MSADIR/$ID.a3m" ]; then
        echo "$MSADIR/$ID.a3m exists"
    else
        echo "Creating MSA for $ID"
        $HHBLITS -i "$FASTA" -d "$UNICLUST" -E 0.001 -all -oa3m "$MSADIR/$ID.a3m"
    fi
done