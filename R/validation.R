library(ggplot2)

setwd("~/Dropbox/insight-data-science/project/strava_buddies/R/")
f.validation  <- "validation.csv"
f.random.sim  <- "random_similarities.csv"

df.validation <- read.csv(f.validation)
df.random.sim <- read.csv(f.random.sim, header=FALSE, col.names=c("trial", "random_similarity"))

df.random.sim$n_activities <- sample(1:15, size=500, replace=TRUE)


ggplot(df.validation, aes(x=miles, y=fract_below)) +
    geom_point() +
    theme_minimal() +
    geom_hline(aes(yint=fract_below_random), color="red") 

ggplot(df.validation, aes(x=n_activities, y=min)) +
    geom_point() +
    theme_minimal() +
    geom_hline(aes(yint=min_random), color="red") 
    

p <-    
    ggplot(df.validation, aes(x=n_activities, y=median)) +
    geom_point(color="#167ebb") +
    geom_point(data=df.random.sim, aes(x=n_activities, y=random_similarity), color="gray50") +
    xlab("Number of activities considered") +
    ylab("Median similarity") +
    xlim(c(0,16)) + ylim(c(0, 0.6))

pdf("median_similarity_vs_random.pdf", width=5, height=5, useDingbats=FALSE)
p
dev.off()

