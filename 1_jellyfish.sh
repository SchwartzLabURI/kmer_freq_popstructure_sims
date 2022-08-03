#!/bin/bash
#SBATCH --job-name="jellyfish"
#SBATCH --time=100:00:00  # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=36   # processor core(s) per node
#SBATCH --mail-user="rsschwartz@uri.edu" #CHANGE TO user email address
#SBATCH --mail-type=END,FAIL

cd $SLURM_SUBMIT_DIR

module purge


module load Python/3.6.6-foss-2018b
module load Jellyfish/2.2.10-foss-2018b

F=human_3pop.fa #change this
k=9  #change this

kmer_prof_dir="${F/.fa/}_${k}_mers/" #folder has fasta simulation name and k
mkdir ${kmer_prof_dir}

while read -r ONE; do
    read -r TWO
    sample=$(echo $ONE | sed 's/^>//') #sample name from fasta minus the >
    sample_file="${kmer_prof_dir}${sample}.fa" #output fa for individual sample goes in the folder

    echo -e "${ONE}\n${TWO}" > ${sample_file}

    jf_file="${kmer_prof_dir}${sample}_${k}_mers.jf"
    fa_file="${kmer_prof_dir}${sample}_${k}_mers.fa"

    echo $sample_file $jf_file $fa_file

    jellyfish count ${sample_file} -m ${k} -s 100M -t 36 -L 2 -C --disk -o ${jf_file}
    jellyfish dump ${jf_file} > ${fa_file} -c

    rm ${jf_file}

    sorted_file=${kmer_prof_dir}${sample}_${k}_mers_sorted.fa
    sort $fa_file > $sorted_file
    rm $fa_file

done < $F

mkdir ${kmer_prof_dir}/sorted
mv ${kmer_prof_dir}/*sorted.fa ${kmer_prof_dir}/sorted/
