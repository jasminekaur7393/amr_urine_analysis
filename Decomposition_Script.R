setwd ("~/Documents/AMR_model/amr_urine")

dat <- read.csv("data.csv")
## From the stats package
A <- ts(dat$Imipenem,frequency = 12)
## From the stats package
dc <- decompose(A,type = "additive")
dc$figure
plot(dc)

trend <- as.numeric(na.omit(dc$trend))
df <- data.frame("Month"=1:length(trend),
                    "Value"=trend)

lm <- lm(Value~Month,data=df)
plot(df$Month,df$Value,type="l")
abline(lm)
summary(lm)


