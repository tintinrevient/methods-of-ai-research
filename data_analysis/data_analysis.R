library(psych)
library(plyr)

## Load data
all_data <- read.csv("MAIR.csv", sep=";", stringsAsFactors = FALSE)
participant_data <- all_data[-(1:2),19:37]
participant_data <- participant_data[,-(14:18)]

## Split data into lowercase and uppercase
# lowercase = 1 and uppercase = 2
participant_lowercase <- data.frame()
participant_uppercase <- data.frame()
for(i in 1:nrow(participant_data)){
  if(participant_data[i,ncol(participant_data)] == 1){
    participant_lowercase <- rbind(participant_lowercase, as.numeric(participant_data[i,-14]))
  }else{
    participant_uppercase <- rbind(participant_uppercase, as.numeric(participant_data[i,-14]))
  }
}
participant_lowercase = rename(participant_lowercase, c("X5"="Q2", "X3"="Q3", "X1"="Q4", "X2"="Q5", "X5.1"="Q6", "X4"="Q7", "X5.2"="Q8", "X4.1"="Q9", "X4.2"="Q10", "X2.1"="Q11", "X5.3"="Q12", "X4.3"="Q13", "X2.2"="Q14"))
participant_uppercase = rename(participant_uppercase, c("X5"="Q2", "X3"="Q3", "X1"="Q4", "X2"="Q5", "X5.1"="Q6", "X4"="Q7", "X5.2"="Q8", "X4.1"="Q9", "X4.2"="Q10", "X2.1"="Q11", "X5.3"="Q12", "X4.3"="Q13", "X2.2"="Q14"))

## Compute the total points for each participant
lowercase <- c()
for(j in 1:nrow(participant_lowercase)){
  lowercase[j] <- rowSums(participant_lowercase[j,])
}

uppercase <- c()
for(k in 1:nrow(participant_uppercase)){
  uppercase[k] <- rowSums(participant_uppercase[k,])
}

## t.test
t.test(lowercase, uppercase)

## Cronbach alpha
participant_cronbach <- data.frame()
for(i in 1:nrow(participant_data)){
    participant_cronbach <- rbind(participant_cronbach,as.numeric(participant_data[i,-14]))
}
participant_cronbach = rename(participant_cronbach, c("X5"="Q2", "X3"="Q3", "X1"="Q4", "X2"="Q5", "X5.1"="Q6", "X4"="Q7", "X5.2"="Q8", "X4.1"="Q9", "X4.2"="Q10", "X2.1"="Q11", "X5.3"="Q12", "X4.3"="Q13", "X2.2"="Q14"))
alpha(participant_cronbach)





