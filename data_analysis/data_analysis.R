library(psych)
library(plyr)
library(ggpubr)

## Load data
all_data <- read.csv("MAIR.csv", sep=";", stringsAsFactors = FALSE)
participant_data <- all_data[-(1:2),19:37]
participant_data <- participant_data[,-(14:18)]
IOS_data <- participant_data[,13:14]
participant_data <- participant_data[,-13]

## Cronbach alpha
participant_cronbach <- data.frame()
for(i in 1:nrow(participant_data)){
  participant_cronbach <- rbind(participant_cronbach,as.numeric(participant_data[i,-13]))
}
participant_cronbach <- rename(participant_cronbach, c("X5"="Q2", "X3"="Q3", "X1"="Q4", "X2"="Q5", "X5.1"="Q6", "X4"="Q7", "X5.2"="Q8", "X4.1"="Q9", "X4.2"="Q10", "X2.1"="Q11", "X5.3"="Q12", "X4.3"="Q13"))
alpha(participant_cronbach)

## Split data into lowercase and uppercase
# lowercase = 1 and uppercase = 2
participant_lowercase <- data.frame()
participant_uppercase <- data.frame()
for(i in 1:nrow(participant_data)){
  if(participant_data[i,ncol(participant_data)] == 1){
    participant_lowercase <- rbind(participant_lowercase, as.numeric(participant_data[i,-13]))
  }else{
    participant_uppercase <- rbind(participant_uppercase, as.numeric(participant_data[i,-13]))
  }
}
participant_lowercase <- rename(participant_lowercase, c("X5"="Q2", "X3"="Q3", "X1"="Q4", "X2"="Q5", "X5.1"="Q6", "X4"="Q7", "X5.2"="Q8", "X4.1"="Q9", "X4.2"="Q10", "X2.1"="Q11", "X5.3"="Q12", "X4.3"="Q13"))
participant_uppercase <- rename(participant_uppercase, c("X5"="Q2", "X3"="Q3", "X1"="Q4", "X2"="Q5", "X5.1"="Q6", "X4"="Q7", "X5.2"="Q8", "X4.1"="Q9", "X4.2"="Q10", "X2.1"="Q11", "X5.3"="Q12", "X4.3"="Q13"))

## Compute the total points for each participant
lowercase <- c()
for(j in 1:nrow(participant_lowercase)){
  lowercase[j] <- rowSums(participant_lowercase[j,])
}

uppercase <- c()
for(k in 1:nrow(participant_uppercase)){
  uppercase[k] <- rowSums(participant_uppercase[k,])
}

## shapiro.test
shapiro.test(lowercase)
shapiro.test(uppercase)

## plot
plot_data <- data.frame()
case_vector <- c(rep("lowercase", length(lowercase)), rep("uppercase", length(uppercase)))
plot_data <- rbind(plot_data, as.data.frame(case_vector))
values_vector <- c(lowercase, uppercase)
plot_data <- cbind(plot_data, values_vector)
ggboxplot(plot_data, x = "case_vector", y = "values_vector", palette = c("#00AFBB", "#E7B800"), ylab = "Frequency", xlab = "Cases")
qqnorm( plot_data$values_vector[plot_data$case_vector=="lowercase"], main='Lowercase')
qqline( plot_data$values_vector[plot_data$case_vector=="lowercase"] )
qqnorm( plot_data$values_vector[plot_data$case_vector=="uppercase"], main='Uppercase')
qqline( plot_data$values_vector[plot_data$case_vector=="uppercase"] )
hist(lowercase)
hist(uppercase)
ggdensity(lowercase, main = "Density plot", xlab = "Lowercase")
ggdensity(uppercase, main = "Density plot", xlab = "Uppercase")

## f.test
var.test(values_vector ~ case_vector, data = plot_data)

## t.test
t.test(lowercase, uppercase)

## IOS
IOS_lowercase <- data.frame()
IOS_uppercase <- data.frame()
for(i in 1:nrow(IOS_data)){
  if(IOS_data[i,ncol(IOS_data)] == 1){
    IOS_lowercase <- rbind(IOS_lowercase, as.numeric(IOS_data[i,-2]))
  }else{
    IOS_uppercase <- rbind(IOS_uppercase, as.numeric(IOS_data[i,-2]))
  }
}

## Compute the total points for each participant
IOS_l_means <- colMeans(IOS_lowercase)
IOS_u_means <- colMeans(IOS_uppercase)
IOS_l_sums <- colSums(IOS_lowercase)
IOS_u_sums <- colSums(IOS_uppercase)




