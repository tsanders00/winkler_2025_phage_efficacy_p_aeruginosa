#!/usr/bin/bash
. /home/viro/xue.peng/software_home/miniconda3/etc/profile.d/conda.sh
conda activate clinker
clinker gbk_jakub_generated/*gbk -i 0.3 -j 50 -o alignmet.aln -p gene.html -mo gene.similarity.matrix --force
