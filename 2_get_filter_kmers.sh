#!/bin/bash
#SBATCH --job-name="kmers pickled"
#SBATCH --time=100:00:00  # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=1   # processor core(s) per node
#SBATCH --mail-user="rsschwartz@uri.edu" #CHANGE TO user email address
#SBATCH --mail-type=END,FAIL

cd $SLURM_SUBMIT_DIR

module purge


module load Python/3.6.6-foss-2018b
module load Jellyfish/2.2.10-foss-2018b

F=human_3pop.fa #change
k=9 #change

kmer_prof_dir="${F/.fa/}_${k}_mers/sorted"

python 2_get_filter_kmers.py $kmer_prof_dir 

