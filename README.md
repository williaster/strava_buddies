##STRAVA buddies 
for a live demo, see [www.STRAVAbuddies.com](http://www.stravabuddies.com)

###Idea
This is a proof-of-principle data science web application for the 2014C session of [Insight Data Science](http://www.insightdatascience.com). The general problem I attempt to solve is how to find __good__ (in the sense of fitness ability and matched patterns of activity) running or cycling partners. In contrast to team sports, these activities are often performed alone despite the motivation, regularity, or simple anti-loneliness benefits associated with running or riding with others. 

As demonstrated by the fact that millions of people run and bike each day, there is a lot of potential for finding workout partners, yet most people don't. Here are three major scenarios that contribute to why this is the case:

1. You are new to an area, or for some reason you literally don't know anyone who runs or bikes in your area.
2. Because of your job, school, commute, partner, kids, ... you have _extremely_ limited flexibility for when you can fit running or biking into your schedule.
3. The people you _do_ know that run or bike are way _better_ or way _worse_ than you are; you aren't a good match at a fitness level.

Hence __STRAVA buddies__.

###Execution
I saw an opportunity to solve this problem using data from a social fitness, activity tracking and analytics site called [Strava](https://www.strava.com). (If you haven't used their service, you should.) Using a snapshot of Bay Area athlete activity patterns and metrics, I built a workout partner recommender for Strava users based on their own activities. (this is just a proof of principle, you can't use your own account. I'm sorry.) Here's a schematic of the algorithm, including specific metrics I looked at:

![STRAVA buddies algorithm](app/static/imgs/algorithm-01.jpg?raw=true "STRAVA buddies algorithm")

###Validation
These simple metrics and imperfect data actually ended up working pretty well. Recommendations are actually hard to validate, but I compared the performance of STRAVA buddies vs randomly chosen athletes in the Bay Area. It clearly did better, but better than random isn't that hard. A less naive algorithm is choosing your current Strava friends. Surprisingly, Strava buddies actually suggests better matches than your current friends! This was true across all athletes I tested, illustrating the utility that the service could provide.

![STRAVA buddies validation](app/static/imgs/validation-01.jpg?raw=true "STRAVA buddies validation")

An interesting feature that you can see from looking at just three athletes is that baseline similiarity varies a fair amount. For example, random suggestsions for Athlete 2 do better than for Athlete 1 or 3. If you were Strava and had comprehensive data for more authenticated athletes, exploring the similarity matrix for more athletes would be an interesting future direction. 

####Still reading?
Marginally more information can be found [here](http://www.stravabuddies.com/slides_wide)
