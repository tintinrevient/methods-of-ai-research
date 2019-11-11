# function to create dataframes to use with cronbach alpha
create_crobach_dataframe <- function(participant_data){
  participant_cronbach <- data.frame()
  for(i in 1:nrow(participant_data)){
    participant_cronbach <- rbind(participant_cronbach, as.numeric(participant_data[i,-ncol(participant_data)]))
  }
  return(participant_cronbach)
}

# split function
split_participants <- function(participant_data){
  participant_lowercase <- data.frame()
  participant_uppercase <- data.frame()
  for(i in 1:nrow(participant_data)){
    if(participant_data[i,ncol(participant_data)] == 1){
      participant_lowercase <- rbind(participant_lowercase, as.numeric(participant_data[i,-ncol(participant_data)]))
    }else{
      participant_uppercase <- rbind(participant_uppercase, as.numeric(participant_data[i,-ncol(participant_data)]))
    }
  }
  return(list(participant_lowercase, participant_uppercase))
}

# participant score
participant_score <- function(participant_lower_upper){
  lowercase <- c()
  uppercase <- c()
  for(j in 1:nrow(participant_lower_upper[[1]])){
    # rowMeans or rowSums
    lowercase[j] <- rowMeans(participant_lower_upper[[1]][j,])
  }
  for(k in 1:nrow(participant_lower_upper[[2]])){
    uppercase[k] <- rowMeans(participant_lower_upper[[2]][k,])
  }
  return(list(lowercase, uppercase))
}

plot_dataframe <- function(IOS_lower_upper, lower_upper){
  IOS <- c(IOS_lower_upper[[1]]$X2, IOS_lower_upper[[2]]$X2)
  anova_data <- data.frame()
  case_vector <- c(rep(0, length(lower_upper[[1]])), rep(1, length(lower_upper[[2]])))
  anova_data <- rbind(anova_data, as.data.frame(case_vector))
  values_vector <- c(lower_upper[[1]], lower_upper[[2]])
  anova_data <- cbind(anova_data, values_vector)
  anova_data <- cbind(anova_data, IOS)
  anova_data <- rename(anova_data, c("case_vector" = "lettercase", "values_vector" = "friendliness"))
  return(anova_data)
}

plotting <- function(anova_data, lower_upper){
  ggboxplot(anova_data, x = "lettercase", y = "friendliness", palette = c("#00AFBB", "#E7B800"), ylab = "Frequency", xlab = "Cases")
  qqnorm( anova_data$friendliness[anova_data$lettercase==0], main='Lowercase')
  qqline( anova_data$friendliness[anova_data$lettercase==0] )
  qqnorm( anova_data$friendliness[anova_data$lettercase==1], main='Uppercase')
  qqline( anova_data$friendliness[anova_data$lettercase==1] )
  hist(lower_upper[[1]])
  hist(lower_upper[[2]])
  ggdensity(lower_upper[[1]], main = "Density plot", xlab = "Lowercase")
  ggdensity(lower_upper[[2]], main = "Density plot", xlab = "Uppercase")
}

bar_plotting <-function(lower_upper, anova_data){
  pd <- data.frame()
  pd <- rbind(pd, as.data.frame(c("lowercase", "uppercase")))
  pd <- cbind(pd, c(mean(lower_upper[[1]]), mean(lower_upper[[2]])))
  bar <- barplot(c(mean(lower_upper[[1]]), mean(lower_upper[[2]])), xlab="Lettercase", ylab = "Friendliness score", ylim = c(0, 5), names.arg=c("Lowercase", "Uppercase")) 
  segments(bar, c(mean(lower_upper[[1]]), mean(lower_upper[[2]])) - c(sd(lower_upper[[1]]), sd(lower_upper[[2]])), bar, c(mean(lower_upper[[1]]), mean(lower_upper[[2]])) + c(sd(lower_upper[[1]]), sd(lower_upper[[2]])), lwd = 1.5)
  arrows(bar, c(mean(lower_upper[[1]]), mean(lower_upper[[2]])) - c(sd(lower_upper[[1]]), sd(lower_upper[[2]])), bar, c(mean(lower_upper[[1]]), mean(lower_upper[[2]])) + c(sd(lower_upper[[1]]), sd(lower_upper[[2]])), lwd = 1.5, angle = 90, code = 3, length = 0.05)
  boxplot(friendliness ~ lettercase, data = anova_data)
}
