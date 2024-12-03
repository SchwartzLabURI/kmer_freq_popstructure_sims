library(tidyverse)

for (k in c(9, 11, 13, 15, 17, 19, 21)){
  p = 1
  s = 1
  f = paste0("P", p, "_", s, "_", k, "_mers_sorted.fa")
  print(f)
  H <- read.csv(f, sep = " ", header = FALSE)
  ggplot(H, aes(V2)) + geom_histogram()
  ggsave(paste0(f, ".pdf"))
}
