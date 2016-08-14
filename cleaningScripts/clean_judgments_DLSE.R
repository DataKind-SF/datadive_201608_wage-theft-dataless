library(data.table)
library(plyr)
library(stringr)

## cleaning Judgments recorded in the State of California Superior Court 
## by the  Labor Commissioner's Division of Labor Standards Enforcement (DLSE).

oda <- read.csv("~/datadive_201608_wage-theft/data/HQ03531 SJO ODA Judgments-1.csv", stringsAsFactors = F)
sjo <- read.csv("~/datadive_201608_wage-theft/data/SJOjudgements2-3.csv", stringsAsFactors = F)
oda <- as.data.table(oda)
sjo <- as.data.table(sjo)

# combining two santa clara datasets
oda <- mutate(oda, date.filed = as.character(""), Defendant.Address = as.character("")) %>%
  select(1, 7, 2, 8, 3:6) 
names(oda) <- names(sjo)
sjo_oda <- rbind(sjo, oda)

#address cleaning
sjo_oda$Defendant.Address <- gsub("  ", " ", sjo_oda$Defendant.Address)
sjo_oda[Defendant.Address != '', c('street.address', 'City') := tstrsplit(Defendant.Address, "\n")]

sjo_oda[grep("-", City), City := substr(City, -4, -1)] # remove extra long zipcodes

sjo_oda[Defendant.Address != '', c('city', 'statezip') := tstrsplit(City, ", ")]


# fixes cases when no comma between city and state
sjo_oda$city <- ifelse(!is.na(as.numeric(str_sub(sjo_oda$city, -5, -1))), 
                       substr(sjo_oda$city, 1, nchar(sjo_oda$city)-8), sjo_oda$city)

sjo_oda$statezip <- ifelse(!is.na(as.numeric(str_sub(sjo_oda$city, -5, -1))), 
                           substr(sjo_oda$city, 8), sjo_oda$statezip)
sjo_oda[, c('state', 'zipcode') := tstrsplit(statezip, ' ')]

# remove intermediate columns
sjo_oda[, City := NULL]
sjo_oda[, statezip := NULL]

# correcting data types
sjo_oda[, Judicial.District := as.factor(Judicial.District)]
sjo_oda[, total.with.court.fees := as.numeric(gsub(",","",total.with.court.fees))]
sjo_oda[, total.amt..of.pltf.award := as.numeric(gsub(",","",total.amt..of.pltf.award))]
sjo_oda[, sum(total.with.court.fees, na.rm = T), by = Judicial.District]
#fix dates
sjo_oda[, date.filed := as.Date(date.filed, "%m/%d/%Y")]
sjo_oda[, judgment.date := as.Date(judgment.date, "%m/%d/%Y")]

