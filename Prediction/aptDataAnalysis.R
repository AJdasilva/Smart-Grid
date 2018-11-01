# Some data visualizations

hdat <- readRDS("/Applications/Personal/UMass/Applied_Math_Project_2/Smart_Grid/data/apartment_electrical_2014.rds");
attach(hdat)
colnames(hdat)
library(data.table)
setnames(hdat, old=c("year","month","date","hour","minute","second","Power kW","apartment"), 
         new=c("yr","mon","day","hour","min","sec","pow","apt"))
subhdat <- hdat[hdat$apt=="Apt1_2014",]
subhdat$date <- as.Date(with(subhdat, paste(yr, mon, day,sep="-")), "%Y-%m-%d")
subhdat$date
plot(subhdat$date,subhdat$pow,
     main="Apartment 1 Power For 2014",xlab="Time(min)", 
     ylab="Power (kW)")
hist(subhdat$pow)

# combine them all (yikes)
setwd('/Applications/Personal/UMass/Applied_Math_Project_2/Smart_Grid/data/temp/')
filenames <- list.files(full.names=TRUE)
electrical.all <- lapply(filenames,function(i){
  read.csv(i, header=FALSE)
})
df <- do.call(rbind.data.frame, electrical.all)
write.csv(df,"all_electrical.csv", row.names=FALSE)


# Apartment 2 for years 2014-2016 ORGANIZE THE DATA
samp1dat <- read.csv("/Applications/Personal/UMass/Applied_Math_Project_2/Smart_Grid/data/temp/Apt2_2014.csv",header=F);
samp2dat <- read.csv("/Applications/Personal/UMass/Applied_Math_Project_2/Smart_Grid/data/temp/Apt2_2015.csv",header=F);
samp3dat <- read.csv("/Applications/Personal/UMass/Applied_Math_Project_2/Smart_Grid/data/temp/Apt2_2016.csv",header=F);
sampdat <- rbind(samp1dat, samp2dat,samp3dat) # Combined data set
colnames(sampdat) = c("DATE","POWER") # Change column names
sampdat$DATE <- as.Date(sampdat$DATE,"%Y-%m-%d") # Simplify date to just be year, month, day

# Take average power for each day:
sampdat <- aggregate(cbind(sampdat$POWER)~DATE, sampdat, mean)
colnames(sampdat) = c("DATE","AVGPOWER") # Change column names

# Plot day VS power for three years
plot(sampdat$DATE,sampdat$AVGPOWER,
     main="Apartment 2 Power For 14,15,16",xlab="Time(days)", 
     ylab="Power (kW)")
lines(lowess(sampdat$DATE,sampdat$AVGPOWER, f=.25))

# Oraganize data to not include the year so data overlays..?
# (probably a better way to do this, just playing around)
sampdat$DATESHORT <- format(sampdat$DATE, format="%m/%d")
sampdat$DATESHORT <- as.Date(sampdat$DATESHORT,"%m/%d")

plot(sampdat$DATESHORT,sampdat$AVGPOWER,
     main="Apartment 2 Power For 14,15,16",xlab="Time(days)", 
     ylab="Power (kW)", xlim=c(as.Date("2018-01-01"),as.Date("2018-12-31")))
lines(lowess(sampdat$DATESHORT,sampdat$AVGPOWER, f=.25, delta=0),color=red)

# lets work with all electrical... (yikes)
# bigMFer <- read.csv("/Applications/Personal/UMass/Applied_Math_Project_2/Smart_Grid/data/temp/all_electrical.csv",header=F);
# colnames(bigMFer) = c("DATE","POWER") # Change column names
# bigMFer$DATE <- as.Date(bigMFer$DATE,"%Y-%m-%d") # Simplify date to just be year, month, day
# # Take average power for each day:
# bigMFer <- aggregate(cbind(bigMFer$POWER)~DATE, bigMFer, mean)
# colnames(bigMFer) = c("DATE","AVGPOWER") # Change column names
# # Oraganize data to not include the year so data overlays..?
# # (probably a better way to do this, just playing around)
# bigMFer$DATE <- format(bigMFer$DATE, format="%m/%d")
# bigMFer$DATE <- as.Date(bigMFer$DATE,"%m/%d")
# 
# plot(bigMFer$DATESHORT,bigMFer$AVGPOWER,
#      main="Apartment 2 Power For 14,15,16",xlab="Time(days)",
#      ylab="Power (kW)")


