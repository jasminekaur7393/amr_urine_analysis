###Zone-wise analysis
library(readr)
library(plyr)
library(dplyr)
library(ggplot2)

set.seed(100)

#pdf("./figures/pseudo_mdr_heatmap.pdf", height = 6, width = 8)

#amr_data <- read_csv(file="data/final/same_zone.csv")
#amr_data <- read_csv(file="data/mdr/Enterococcus_mdr.csv")
#amr_data <- read_csv(file="data/mdr/Escherichia coli _mdr.csv")
#amr_data <- read_csv(file="data/mdr/Klebsiella_mdr.csv")
amr_data <- read_csv(file="data/mdr/Pseudomonas aeruginosa_mdr.csv")

#organism = "Enterococcus"

#amr_data <- filter(amr_data, organism_name == organism)

amr_data <- filter(amr_data, mdr == TRUE)


summary(amr_data)

#antibiotics <- c("Amikacin" , "Piperacillin-tazobactam", "Trimethoprim-sulfamethoxazole", "Nitrofurantoin" , "Imipenem" , "Meropenem" , "Ciprofloxacin" , "Cefotaxime" , "Ertapenem" , "Levofloxacin" , "Fosfomycin" , "Cefazolin" , "Colistin")
#antibiotics <- c("Amikacin" , "Piperacillin-tazobactam" , "Nitrofurantoin" , "Imipenem" , "Meropenem" , "Ciprofloxacin" , "Trimethoprim-sulfamethoxazole" , "Cefotaxime" , "Ertapenem" , "Levofloxacin" , "Fosfomycin" , "Cefazolin" , "Colistin")
#antibiotics <- c("Vancomycin" , "Nitrofurantoin" , "Linezolid" , "Teicoplanin" , "Ampicillin" , "Ciprofloxacin" , "Fosfomycin", "Gentamicin HL")
antibiotics <- c("Amikacin" , "Meropenem" , "Piperacillin-tazobactam" , "Ciprofloxacin" , "Imipenem" , "Cefepime" , "Ceftazidime" , "Gentamicin" , "Levofloxacin" , "Tobramycin" , "Colistin")

amr_data_zone <- dlply(.data = amr_data, .variables = "zone")

zone_count <- sapply(amr_data_zone,nrow)
zone_df <- data.frame(zone=names(zone_count), count=zone_count) 

getSummaryAMR <- function(xx) {
  colNames <- antibiotics
  summary_amr <- list()
  print(xx)
  for(i in 1:length(colNames)){
    print(colNames[i])
    ytab <- table(xx[,colNames[i]])
    if(length(ytab) == 0){
      df_ <- data.frame(Var1=c('I','R','S'),Freq=c(0,0,0))
    }else{
      df_ <- data.frame(ytab)
    }
    sum_count <- sum(df_$Freq)
    if(sum_count > 0) {
      df_ <- transform(df_, Freq = Freq/sum_count) 
    }
    print(df_)
    df_$antibiotic <- colNames[i]
    summary_amr[[i]] <- df_
  }
  summary_amr_df <- ldply(summary_amr)
  return(summary_amr_df)
}

amr_summary <- lapply(amr_data_zone, getSummaryAMR)

names(amr_summary) <- names(amr_data_zone)

amr_summary_df <- ldply(amr_summary,.id = 'zone')

amr_summary_df <- amr_summary_df[amr_summary_df$Freq != 0,]


amr_summary_df_patter <- dlply(amr_summary_df,'Var1')
library(reshape2)
xx <- dcast(amr_summary_df_patter[[2]], formula = zone~antibiotic,value.var = "Freq")
xx_mat <-as.matrix(xx[,-1])
rownames(xx_mat) <- xx$zone
xx_mat[is.na(xx_mat)] <- 0
xx_mat <- xx_mat *100

library("gplots")
col <- rev(heat.colors(999))

hm <- heatmap.2(xx_mat, trace="none",cexCol=0.9, cexRow=0.9, cellnote=round(xx_mat), notecol="black", density.info="none", margins=c(12,10),  col=col, scale = "column")

#dev.off()