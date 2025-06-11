#!/bin/bash
#SBATCH -J ppi_network
#SBATCH -o ppi_network_out
#SBATCH -e ppi_network_error
#SBATCH -t 01:00:00 # Set to 2 days

#SBATCH -p cpu_p
#SBATCH --qos cpu_normal

#SBATCH --ntasks=1
#SBATCH -c 6
#SBATCH --mem=20G
#SBATCH --nice=10000

### set source
source $HOME/.bashrc

### activate SpeedPPI environment
conda activate speed_ppi_dev

cd $HOME/test_speedppi/SpeedPPI/

### directory where to store the 2 dataframes
OUTDIR="$HOME/tiamani/phages_vs_bacterias/ppi_network"

### PDOCKQ score for filtering
PDOCKQ_T=0.5

#4. Merge all predictions to construct a PPI network.
#When the pDockQ > 0.5, the PPV is >0.9 (https://www.nature.com/articles/s41467-022-28865-w, https://www.nature.com/articles/s41594-022-00910-8)
#The default threshold to construct edges (links) is 0.5
python3 ./src/build_ppi.py --pred_dir $OUTDIR/ \
--pdockq_t $PDOCKQ_T --outdir $OUTDIR/

