


sed s/N//g <GRCh38_full_analysis_set_plus_decoy_hla.fa >GRCh38_full_analysis_set_plus_decoy_hla_noN.fa #slim doesn't like Ns

grep -n 'chr' GRCh38_full_analysis_set_plus_decoy_hla_noN.fa

head -3556522 GRCh38_full_analysis_set_plus_decoy_hla_noN.fa > GRCh38_full_analysis_set_plus_decoy_hla_noN_chr1.fa

grep "\S" GRCh38_full_analysis_set_plus_decoy_hla_noN_chr1.fa >GRCh38_full_analysis_set_plus_decoy_hla_noN_chr1_noblanks.fa

sed 's/M/A/g' GRCh38_full_analysis_set_plus_decoy_hla_noN_chr1_noblanks.fa > GRCh38_full_analysis_set_plus_decoy_hla_noN_chr1_noblanks_noM.fa

sed 's/R/A/g' GRCh38_full_analysis_set_plus_decoy_hla_noN_chr1_noblanks_noM.fa > GRCh38_full_analysis_set_plus_decoy_hla_noN_chr1_noblanks_noMR.fa

head -1000 GRCh38_full_analysis_set_plus_decoy_hla_noN_chr1_noblanks_noMR.fa > GRCh38_full_analysis_set_plus_decoy_hla_noN_chr1_noblanks_noMRsmall3.fa

#now run slimgui

