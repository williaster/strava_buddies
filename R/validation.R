library(ggplot2)

setwd("~/Dropbox/insight-data-science/project/strava_buddies/R/")
load(".RData")

#....................................................................................
# variables and helper functions
orange <- "#f74f00"
blue   <- "#167ebb"
grey   <- "gray50"

get.sd <- function(y, n=1) {
    y.mean <- mean(y)
    y.sd   <- sd(y)
    result <- c(mean(y) - sd(y), mean(y) + sd(y))
    names(result) <- c("ymin", "ymax")
    data.frame(y=y.mean, ymin=y.mean - (n*y.sd), ymax=y.mean + (n*y.sd))
}

get.random <- function(f, algorithm) {
    df.f <- read.csv(f, header=FALSE, col.names=c("trial", "median"))
    df   <- data.frame(median = df.f[,"median"],
                       n_activities = sample(1:15, size=nrow(df.f), replace=TRUE),
                       algorithm    = algorithm )
    df
}

get.user.df <- function(f.stravabuddies, f.randomfriends, f.random, athlete) {   
    df.stravabuddies <- read.csv(f.stravabuddies)[,c("median", "n_activities")]
    df.stravabuddies["algorithm"] <- "stravabuddies"
   
    df.friends <- get.random(f.randomfriends, "friends")
    df.random  <- get.random(f.random, "random")
    
    df.final <- do.call(rbind, list(df.stravabuddies, df.friends, df.random))
    df.final["athlete"] <- athlete
    df.final
}

#....................................................................................
# chris files
f.c.bigbins           <- "chris/validation_chris_50x-bins.csv"
f.c.random.sim        <- "chris/random_medians_chris.csv"
f.c.random.friend.sim <- "chris/random_friend_medians_chris.csv"

# rob files
f.r.bigbins           <- "rob/validation_rob_50x-bins.csv"
f.r.random.sim        <- "rob/random_medians_rob.csv"
f.r.random.friend.sim <- "rob/random_friend_medians_rob.csv"

# nicole files
f.n.bigbins           <- "nicole/validation_nicole_50x-bins.csv"
f.n.random.sim        <- "nicole/random_medians_nicole.csv"
f.n.random.friend.sim <- "nicole/random_friend_medians_nicole.csv"

#....................................................................................
#

df.chris  <- get.user.df(f.c.bigbins, f.c.random.friend.sim, f.c.random.sim, "Athlete 3")
df.rob    <- get.user.df(f.r.bigbins, f.r.random.friend.sim, f.r.random.sim, "Athlete 2")
df.nicole <- get.user.df(f.n.bigbins, f.n.random.friend.sim, f.n.random.sim, "Athlete 1")

# rob has outliers
df.rob   <- subset(df.rob, median >= 0.275)
df.final <- do.call(rbind, list(df.chris, df.rob, df.nicole))

p <- ggplot(df.final, aes(x=n_activities, y=median, color=algorithm, fill=algorithm)) +
    geom_point(alpha=0.25) + 
    scale_color_manual(values=c(blue, grey, orange)) +
    scale_fill_manual(values=c(blue, grey, orange)) +
    xlab("Number of activities considered") +
    ylab("Median similarity") + 
    stat_summary(fun.data = "get.sd", geom="smooth") +
    xlim(c(0,16)) + #ylim(c(0.2, 0.7)) +
    facet_wrap(~athlete, ncol=3, scales="free_y") +
    #geom_vline(xint=2, linetype="dashed") +
    theme_bw() +
    theme(legend.position="none")


p.nofriends <- ggplot(subset(df.final, algorithm %in% c("random", "stravabuddies")), 
                      aes(x=n_activities, y=median, color=algorithm, fill=algorithm)) +
    geom_point(alpha=0.25) + 
    scale_color_manual(values=c(grey, orange)) +
    scale_fill_manual(values=c(grey, orange)) +
    xlab("Number of activities considered") +
    ylab("Median similarity") + 
    stat_summary(fun.data = "get.sd", geom="smooth") +
    xlim(c(0,16)) + #ylim(c(0.2, 0.7)) +
    facet_wrap(~athlete, ncol=3, scales="free_y") +
    theme_bw() +
    theme(legend.position="none")

pdf("median_similarity_vs_random_vs_friends_all.pdf", width=11, height=3.5, useDingbats=FALSE)
p
dev.off()

pdf("median_similarity_vs_random_all.pdf", width=11, height=3.5, useDingbats=FALSE)
p.nofriends
dev.off()