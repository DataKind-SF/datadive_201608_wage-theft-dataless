library(data.table)
library(plyr)
library(dplyr)
library(stringr)

whd <- as.data.frame(fread("~/Dropbox/datadive_wagetheft/data/whd_whisard.csv"))

colnames(whd)
str(whd$naic_cd)

getShortCode <- function(currCode, depth){
  if(nchar(currCode) < depth) return("")
  return(substr(currCode, 1, depth))
}

whd$naic_cd_lvl1 <- vapply(whd$naic_cd, function(x) getShortCode(x, 1), character(1))
whd$naic_cd_lvl2 <- vapply(whd$naic_cd, function(x) getShortCode(x, 2), character(1))
whd$naic_cd_lvl3 <- vapply(whd$naic_cd, function(x) getShortCode(x, 3), character(1))
whd$naic_cd_lvl4 <- vapply(whd$naic_cd, function(x) getShortCode(x, 4), character(1))
whd$naic_cd_lvl5 <- vapply(whd$naic_cd, function(x) getShortCode(x, 5), character(1))
whd$naic_cd_lvl6 <- vapply(whd$naic_cd, function(x) getShortCode(x, 6), character(1))

# write.csv(whd, "~/Dropbox/datadive_wagetheft/data/processedWhdData/whd_whisard.naicNumericLevels.csv",
#           row.names = FALSE)

##################
# add human readable names
naicsCodes <- data.frame(fread("~/Dropbox/datadive_wagetheft/data/sandbox/NAICS/2012_NAICS_Structure_FINAL.csv"))
colnames(naicsCodes) <- c("code", "name")
# trim leading and trailing whitespace
naicsCodes <- naicsCodes %>% mutate(name = str_trim(name))
stopifnot(length(unique(naicsCodes$code)) == nrow(naicsCodes))



for(i in 2:6){
  print(i)
  temp <- subset(naicsCodes, nchar(code) == i)
  lvlColIdx <- which(colnames(whd) == paste0("naic_cd_lvl", i))
  whdSelect <- whd[, lvlColIdx, drop = FALSE]
  colnames(whdSelect)[1] <- "code"
  whdSelect <- join(whdSelect, temp)
  newColName <-  paste0("naic_description_lvl", i)
  colnames(whdSelect)[2] <- newColName
  whdSelect[,2][is.na(whdSelect[,2])] <- ""
  stopifnot(all(whdSelect$code == whd[,lvlColIdx]))
  whd <- cbind(whd, whdSelect[, newColName])
  colnames(whd)[ncol(whd)] <- newColName
  
}

write.csv(whd, "~/Dropbox/datadive_wagetheft/data/processedWhdData/whd_whisard.naicHumanReadableLevels.v3.csv",
          row.names = FALSE)
unique(whd$naic_description_lvl2)


###########################
###########################
# trash (old code)
# getHumanName <- Vectorize(function(code){
#   if(! code %in% naicsCodes$code) return("")
#   names <- naicsCodes$name[which(naicsCodes$code == code)]
#   if(length(names) > 2) warning(paste0("more than one name for code ", code))
#   return(names)
# })
# 
# 
# ###########################
# # slow! could have done this faster...
# # there are no level 1 codes
# whd <- whd %>% mutate(naic_description_lvl2 = getHumanName(naic_cd_lvl2))
# whd <- whd %>% mutate(naic_description_lvl3 = getHumanName(naic_cd_lvl3))
# whd <- whd %>% mutate(naic_description_lvl4 = getHumanName(naic_cd_lvl4))
# whd <- whd %>% mutate(naic_description_lvl5 = getHumanName(naic_cd_lvl5))
# whd <- whd %>% mutate(naic_description_lvl6 = getHumanName(naic_cd_lvl6))
# 
# 
# View(whd[,grepl("naic", colnames(whd))])
# length(which(whd$naic_description_lvl2 == ""))



