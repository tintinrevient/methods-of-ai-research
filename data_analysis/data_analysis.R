library(psych)
library(plyr)
library(ggpubr)
library(mediation)
library(car)

source("analysis_functions.R")

## Load data
{
all_data <- read.csv("MAIR.csv", sep=";", stringsAsFactors = FALSE)
participant_data <- all_data[-(1:2),19:37]
# delete personal data
participant_data <- participant_data[,-(14:18)]
# question about IOS
IOS_data <- participant_data[,13:14]
# delete question about IOS
participant_data <- participant_data[,-13]
# delete questions 6,7 and 8
participant_data <- participant_data[,-(5:7)]
# questions 6,7 and 8
other_questions <- all_data[-(1:2), 19:37]
other_questions <- other_questions[,-(1:4)]
other_questions <- other_questions[,-(4:14)]
# gender question -> q17
gender_data <- all_data[-(1:2),19:37]
gender_data <- gender_data[,-(17:19)]
gender_data <- gender_data[,-(14:15)]
gender_data <- gender_data[,-(5:7)]
gender_data <- gender_data[,-10]
}

## Cronbach alpha
participant_cronbach <- create_crobach_dataframe(participant_data)
other_cronbach <- create_crobach_dataframe(other_questions)
friendliness_alpha <- psych::alpha(participant_cronbach)
other_alpha <- psych::alpha(other_cronbach)

## Split data into lowercase and uppercase
# lowercase = 1 and uppercase = 2
participant_lower_upper <- split_participants(participant_data)

## Compute the total points for each participant
lower_upper <- participant_score(participant_lower_upper)

## IOS
IOS_lower_upper <- split_participants(IOS_data)

## data
# lowercase = 0 and uppercase = 1
anova_data <- plot_dataframe(IOS_lower_upper, lower_upper)

## shapiro.test
shapiro.test(c(lower_upper[[1]], lower_upper[[2]]))

## f.test (homogeneity of variances)
var.test(friendliness ~ lettercase, data = anova_data)

## plot
plotting(anova_data, lower_upper)

## Anova and mediation
model_L <- lm(IOS ~ lettercase, anova_data)
model_F <- lm(friendliness ~ lettercase + IOS, anova_data)
mediation_mediate <- mediate(model_L, model_F, treat = "lettercase", mediator = "IOS", boot = TRUE, sims = 100)
summary(mediation_mediate)
mediation_function <- psych::mediate(friendliness ~ lettercase + (IOS), x = anova_data$lettercase, m = anova_data$IOS, data = anova_data)
mediate.diagram(mediation_function, ylim=c(3,7.5),xlim=c(0,10))
summary(mediation_function)
anova_test <- aov(friendliness ~ lettercase, data = anova_data)
summary(anova_test)

## barplot
bar_plotting(lower_upper, anova_data)

#### GENDER
## Split data into male and female
# male = 1 and female = 2
participant_male_female <- split_participants(gender_data)

## Compute the total points for each participant
male_female <- participant_score(participant_male_female)

## shapiro.test
shapiro.test(c(male_female[[1]], male_female[[2]]))

## t.test
t.test(male_female[[1]], male_female[[2]])

questions <- split_participants(other_questions)
q6 <- list()
q6[[1]] <- questions[[1]][,1]
q6[[2]] <- questions[[2]][,1]

#q78 <- list() 
#q78[[1]] <- questions[[1]][,-1]
#q78[[2]] <- questions[[2]][,-1]
#lower_upper_q78 <- participant_score(q78)

## Correlations
# correlation lowercase with question 6
c_lower_q6 <- cor(lower_upper[[1]], q6[[1]])
# correlation uppercase with question 6
c_upper_q6 <- cor(lower_upper[[2]], q6[[2]])
# correlation lowercase with question 7 and 8
#cor(lower_upper[[1]], lower_upper_q78[[1]])
# correlation uppercase with question 7 and 8
#cor(lower_upper[[2]], lower_upper_q78[[2]])

# mean and sd: age of participants
mean(as.numeric(all_data[-(1:2), 33]))
sd(as.numeric(all_data[-(1:2), 33]))

# variance inflation factors
car::vif(model_F)

# models
plot(model_L)
plot(model_F)

# r.test (correlation tests)
r.test(length(lower_upper[[1]]) , c_lower_q6)
r.test(length(lower_upper[[2]]) , c_upper_q6)
r.test(length(lower_upper[[1]]),c_lower_q6, c_upper_q6)


