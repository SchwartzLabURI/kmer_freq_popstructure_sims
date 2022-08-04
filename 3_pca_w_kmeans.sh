#!/bin/bash
#SBATCH --job-name="pca"
#SBATCH --time=100:00:00  # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=1   # processor core(s) per node
#SBATCH --mail-user="rsschwartz@uri.edu" #CHANGE TO user email address
#SBATCH --mail-type=END,FAIL

cd $SLURM_SUBMIT_DIR

module purge


module load matplotlib/3.3.3-intel-2020b
module load SciPy-bundle/2020.11-intel-2020b
module load scikit-learn/0.23.2-intel-2020b

F=human_3pop.fa
k=21 #change

kmer_prof_dir="${F/.fa/}_${k}_mers/sorted/"

python 3_pca_w_kmeans_80_percent_variance.py ${kmer_prof_dir}

