#faststructure instructions for personal mac

#convert fa file to structure format with get_var_sites_from_fasta (python3)

#conda activate py2

STR_FOLDER=/Users/rachelschwartz/anaconda3/pkgs/faststructure-1.0-py27h549429d_0/bin

for FOLDER in sim*; do

  DATA_FOLDER=/Users/rachelschwartz/Desktop/URI/papers/pop_structure_kmer_freq/sims/faststructure/$FOLDER

  F=${FOLDER}.fa.str #has .str.str so this is no extension

  for K in $(seq 2 6); do
    python $STR_FOLDER/structure.py  -K $K --input=${DATA_FOLDER}/$F  --output=${DATA_FOLDER}/${F}.structuretest --full --seed=100 --format=str
  done

  python ${STR_FOLDER}/chooseK.py --input=${DATA_FOLDER}/${F}.structuretest

done

#  python ${STR_FOLDER}/distruct.py -K 3 --input=${DATA_FOLDER}/${F}.structuretest --output=${DATA_FOLDER}/${F}.structuretest_distruct.svg  --popfile=${DATA_FOLDER}/3pop
