from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
from Bio import SeqIO
import os
import sys

input_file = sys.argv[1]

#empty alignment with same species
snpalign = MultipleSeqAlignment([])
alignment = AlignIO.read(input_file, "fasta")
for i in alignment:
    blankseq = SeqRecord(Seq(""), id=i.id)
    snpalign.append(blankseq)

letters = ['A', 'C', 'T', 'G']
for i in range(alignment.get_alignment_length()):
    bases = "".join(set(alignment[:, i]))
    if set(bases).issubset(set(letters)):   #only keep all DNA, no gaps etc
        if len(bases) == 2:   #keep biallelic
            snpalign  = snpalign + alignment[:, i:i+1]  #add column


#save as fasta
with open(sys.argv[1]+".fasta", "w") as handle:
    count = SeqIO.write(snpalign, handle,'fasta-2line')

#remove newline after sample name
#remove >
#remove _
#separate bases and reorder columns
#swap ACGT for 1234
#awk '{printf "%s%s",$0,(NR%2?" ":"\n")}' snps.fasta  | sed -e 's/>//g' -e 's/_/ /g' -e 's/\<unknown description//g' | awk '{gsub(/./,"& ",$3);print $2$1,$1,$3}' | sed -e 's/A/0/g' -e 's/C/1/g' -e 's/G/2/g' -e 's/T/3/g' > snps_for_structure.str
