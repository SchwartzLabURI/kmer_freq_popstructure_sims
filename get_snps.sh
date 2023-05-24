#!/bin/bash
#SBATCH --job-name="snps"
#SBATCH --time=10:00:00  # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=1   # processor core(s) per node
#SBATCH --mail-user="rsschwartz@uri.edu" #CHANGE TO user email address
#SBATCH --mail-type=END,FAIL

cd $SLURM_SUBMIT_DIR

module purge

module load SciPy-bundle/2020.11-foss-2020b

filename=sim1_basic2b_2pop.fa

python get_var_sites_from_fasta.py $filename

awk '{printf "%s%s",$0,(NR%2?" ":"\n")}' ${filename}.fasta  | sed -e 's/>//g' -e 's/_/ /g' -e 's/<unknown description//g' | awk '{gsub(/./,"& ",$3);print $2$1,$3}' | sed -e 's/A/0/g' -e 's/C/1/g' -e 's/G/2/g' -e 's/T/3/g' > ${filename}.str

rm ${filename}.str.str
while read line
do
    echo '# # # # # '$line >> ${filename}.str.str
    echo '# # # # # '$line >> ${filename}.str.str
done < ${filename}.str

mv ${filename}.str.str structure_runs

rm ${filename}.str
