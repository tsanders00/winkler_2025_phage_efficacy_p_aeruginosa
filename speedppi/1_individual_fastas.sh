#!/bin/bash
#
#SBATCH -J make_idividual_fastas
#SBATCH -o make_idividual_fastas_out
#SBATCH -e make_idividual_fastas_error

#SBATCH -p cpu_p
#SBATCH --qos cpu_normal

#SBATCH -t 08:00:00
#SBATCH -c 6
#SBATCH --mem=20G
#SBATCH --nice=10000


source $HOME/.bashrc

### Activate working env
conda activate speed_ppi_dev

cd $HOME/test_speedppi/SpeedPPI

#INPUT
FASTA_SEQS1=/path_to_fasta1 #All fasta seqs from list 1
FASTA_SEQS2=/path_to_fasta2 #All fasta seqs from list 2
HHBLITS=/path_to_hblits #Path to HHblits
PDOCKQ_T=0.5 # (default=0.5)
OUTDIR=/path_to_outdir # Path to output directory where 2 directories called fasta1 and fasta2 will be created.

#DEFAULT
UNICLUST=./data/uniclust30_2018_08/uniclust30_2018_08 #Assume path according to setup


# The pipeline starts here
#1. Create individual fastas

#List 1
FASTADIR=$OUTDIR/fasta1/
if [ -f "$FASTADIR/id_seqs.csv" ]; then
  echo Fastas exist...
  echo "Remove the directory $FASTADIR if you want to write new fastas."
else
mkdir -p $FASTADIR
python3 ./src/preprocess_fasta.py --fasta_file $FASTA_SEQS1 \
--outdir $FASTADIR
echo "Writing fastas of each sequence to $FASTADIR"
fi

#List 2
FASTADIR=$OUTDIR/fasta2/
if [ -f "$FASTADIR/id_seqs.csv" ]; then
  echo Fastas exist...
  echo "Remove the directory $FASTADIR if you want to write new fastas."
else
mkdir $FASTADIR
python3 ./src/preprocess_fasta.py --fasta_file $FASTA_SEQS2 \
--outdir $FASTADIR
echo "Writing fastas of each sequence to $FASTADIR"
fi
wait