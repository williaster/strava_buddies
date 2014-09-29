library(ggplot2)
orange <- "#f74f00"
blue   <- "#167ebb"
grey   <- "gray50"

getSD <- function(y, n=1) {
    y.mean <- mean(y)
    y.sd   <- sd(y)
    result <- c(mean(y) - sd(y), mean(y) + sd(y))
    names(result) <- c("ymin", "ymax")
    data.frame(y=y.mean, ymin=y.mean - (n*y.sd), ymax=y.mean + (n*y.sd))
}

setwd("~/Dropbox/insight-data-science/project/strava_buddies/R/chris")
#load(".RData")
f.bigbins           <- "validation_chris_40x-bins.csv"
f.random.sim        <- "random_medians_chris.csv"
f.random.friend.sim <- "random_friend_medians_chris.csv"


df.bigbins  <- read.csv(f.bigbins)
df.stravabuddies <- df.bigbins[,c("median", "n_activities")]
df.stravabuddies["algorithm"] <- "stravabuddies"

df.random.sim <- read.csv(f.random.sim, header=FALSE, 
                          col.names=c("trial", "median"))
df.random.sim$n_activities <- sample(1:15, size=500, replace=TRUE)
df.random <- df.random.sim[,c("median", "n_activities")]
df.random["algorithm"] <- "random"


df.random.friend.sim <- read.csv(f.random.friend.sim, header=FALSE, 
                                 col.names=c("trial", "median"))
df.random.friend.sim$n_activities <- sample(1:15, size=500, replace=TRUE)
df.friends <- df.random.friend.sim[,c("median", "n_activities")]
df.friends["algorithm"] <- "friends"





df.final <- do.call(rbind, list(df.stravabuddies, df.friends, df.random))

p<- ggplot(df.final, aes(x=n_activities, y=median, color=algorithm, fill=algorithm)) +
    geom_point(alpha=0.25) + 
    scale_color_manual(values=c(blue, grey, orange)) +
    scale_fill_manual(values=c(blue, grey, orange)) +
    xlab("Number of activities considered") +
    ylab("Median similarity") + 
    stat_summary(fun.data = "getSD", geom="smooth") +
    xlim(c(0,16)) #+ ylim(c(0, 0.6))


pdf("validation_algs_chris.pdf", width=5, height=5, useDingbats=FALSE)
p
dev.off()
