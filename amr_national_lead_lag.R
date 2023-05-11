library(corrplot) 
library(ggcorrplot)
library(GGally)
library(readr)
library(tseries)

st <- c("Enterococcus", "Escherichiacoli ", "Klebsiella", "Pseudomonasaeruginosa")


########### data paths ############
main_path <- "data/for_r/national/"
save_path <- "figures/national_lead_lag/"

check_stationary <- function(series) {
  # print(" ********* Inside check_stationary")
  series_p <- adf.test(series)$p.value
  return(series_p <= 0.05)
}

my_diff <- function(x){x = c(diff(x))}

temp_ccf<- NULL
temp_ccf_pvalue <- NULL

make_stationary_and_calc_ccf <- function(series1, series2, anitibiotic_name1, anitibiotic_name2) {
  # print("Call to make_stationary")
  stat_series1 <- series1
  stat_series2 <- series2
  count<- 0
  
  if(length(stat_series1) != length(stat_series2)) {
    print("------ Diff Num rows detected -------------")
    print(length(stat_series1))
    print(length(stat_series2))
    exit(-1)
  }

  while(check_stationary(stat_series1) == FALSE || check_stationary(stat_series2) == FALSE) {
    stat_series1<- sapply(data.frame(stat_series1),my_diff)
    stat_series2<- sapply(data.frame(stat_series2),my_diff)
    # print("---- Pass inside make_stationary")
    count<- count+1
  }
  print(paste0(anitibiotic_name1, " x ", anitibiotic_name2, "--------------", count))

  ccf_values <- ccf(as.vector(stat_series1), 
                    as.vector(stat_series2), 
                    main = paste0(anitibiotic_name1, " ", anitibiotic_name2))
  ps <- 2 *(1 - pnorm(abs(ccf_values$acf), mean = 0, sd = 1/sqrt(ccf_values$n.used)))
  
  max_ccf_index = which.min(ccf_values$acf)
  max_ccf_p_value = ps[max_ccf_index]
  max_ccf_val = ccf_values$acf[max_ccf_index]
  
  temp_ccf <<- rbind(temp_ccf, c(anitibiotic_name1, 
                                anitibiotic_name2,
                                max_ccf_index-15,
                                max_ccf_val,
                                max_ccf_p_value))
}

for(nam in st) {
  ####### data loading #########
  dat <- read.csv(paste0(main_path, paste0("month_year_", nam, ".csv")))
  dat$date<- NULL
  
  pdf(paste0(save_path, nam, ".pdf"), height = 6, width = 8)
  par(mar =c(10,4,5,2))
  dat_colnames <- colnames(dat)
  for(i in 1:length(dat_colnames)){
    for(j in 1:length(dat_colnames)){
      # print(paste0("Processing columns - ", dat_colnames[i], " x ", dat_colnames[j]))
      series1 <- dat[,i]
      series2 <- dat[,j]
      antibiotic_name1 <- dat_colnames[i]
      antibiotic_name2 <- dat_colnames[j]
      make_stationary_and_calc_ccf(series1, series2, antibiotic_name1, antibiotic_name2)
    }
  }
  dev.off()
}