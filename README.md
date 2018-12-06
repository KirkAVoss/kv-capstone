# NBA Win-Share Estimator with Emphasis on Predicting Career Shape Following Rookie Deal Termination:

My goal is to predict NBA player performance during years 5-9 of his career, based on the player's statistics from years 1-4.  Currently, I use "Win Shares" as the measure of performance.

I use a collection of regressors--each regressor predicts a single year.

## Background and Motivation

I have practiced as a lawyer for almost a decade.  I also love watching sports.  So I am interested in how leagues structure their player contracts--and I find the National Basketball Association's format particularly interesting.

National Basketball Association ("NBA") contracts for rookies are are guided by the collective bargaining agreement ("CBA") between the NBA and NBA players's union.  Rookie contracts are set by a scale--each player can negotiate their contract between 80% to 120% of the scale.  However, every rookie contract follows the same format--a two year contract, followed by two years of "team options."  This means that the drafting team has the option to continue to employ the player on the "rookie scale."  The player has little negotiating power.

For talented players, this team option means that the first time an NBA team must make a "real" salary determination is between a player's 2nd and 3rd years.  And again, between the 3rd and 4th years, the team can exercise its option to keep the player employed.  But these 3rd and 4th year option *prices* are set on the rookie scale.  So there's not much price negotiation at this point in a player's career.

The first "good" opportunity for a payday comes on the player's foray into free-agency.  Thus, for players with on-court success in the early stages of their career (thus, their respective team has exercised its 3rd and 4th year option under the rookie payscale), this payday opportunity arrives between the players' 4th and 5th year.

Consequently, there is a need to objectively assess the player's ability to help a team win basketball games following the expiration of the player's rookie deal.  Often, contracts for professional athletes pay the athlete for their performance in *the past*.  In other words, contracts reflect the player's previous performance, but because of age (or other factors), that performance declines during the course of their "big" contract.  That leaves team management with underperforming, expensive assets.  

But in the rookie-deal context, teams are betting on the come.  Young players have often not reached their full potential when they are entering their fourth year.  This can result in GM's placing emphasis on player *potential*, and not what the player will likely contribute to a winning team.  *See, e.g.*, Andrew Wiggins signing a 5-year, $147 million "supermax" extension with Minnesota at the conclusion of his rookie deal.  That ties up roughly 30% of Minnesota's salary cap with one player.  What if that player is a bust?  Can we accurately predict the player's performance to avoid paying players who won't actually perform?

Using historic and current game and season stats, I attempt to predict the shape of an NBA player's career based on their contribution to winning basketball--memorialized in the number of wins that player provides for his team (e.g., Win Shares).

## Previous Approaches

The most notable work related to predicting player performance has been FiveThirtyEight.com's CARMELO player projection system.  FiveThirtyEight.com iterates on the CARMELO system annually and should provide a good baseline for comparison.

CARMELO's backbone ["is an algorithm that compares current players to past ones who had statistically similar profile through the same age."](https://fivethirtyeight.com/features/our-nba-player-projections-are-ready-for-2018-19/)  CARMELO mostly relies on a blend of RPM (real-plus-minus) and BPM (box-plus-minus). *Id*.  The CARMELO system also uses in-season ELO ratings (hence the "ELO" in CARMELO) to update the ranking.  FiveThirtyEight is currently mulling over overhauling their in-season update mechanic. *Id*.


## Methodology and Technology Stack

I utilized the standard data science technology stack, as seen below:
[!!!IMAGE!!!!]

For data collection, I scraped Basketball-Reference.com for initial datasets for all players from 1997 to the previous completed season--2018.  To pull advanced stats, I utilized Data Miner--an app that can be used with Google Chrome--and created a "recipe" to scrape data.  

I also downloaded a database that contained player demographic data, including the year each player entered the NBA. I stored this data in CSV format.

In my SeasonalRegressor class, I utilized a collection of random forest regressors from scikit-learn to predict player performance. Each random forest predicts a specific year--year 5 through 9.  I hope to add the ability to use gradient boosted trees to my SeasonalRegressor class in the future.

## EDA

The data were generally well formatted.  Very few NANs had to be filled--and most were related to players with very low minutes and who played few seasons.  So, those players were generally irrelevant to the year 5-9 predictions.  For example, some player data contained NANs for 3-point percentage (because they were bigs who never took a 3) or free-throw percentage (because they never took a free throw).  I filled those values with zero.

In the below, we can see that many players only play one or two seasons.  There's a steep drop off to year 2, and a slightly less steep drop to season 3.  

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "All Player Seasons")

Note that this plot includes players multiple times--Dirk Nowitzki appears 20 times--once per each season he played.

So the size for train and test sets was significantly less than the full number of players.  In fact, since 1997, there were only 306 players that played at least on game in seasons 1-9.  A total of 2022 unique players have been in the league in that period--that's only 15%.

## Challenges

### Adding "Years in the League"

My initial data that I pulled from Basketball-reference.com, while generally complete, did not include the year the player entered the NBA.  To filter data based on years 1-9 of a player's career, I needed the player's initial season. I found some data that include the player's rookie year and used it to create the *Seasons_number* field in my data (i.e. the number of seasons the player has been in the NBA).

### Database Collisions

A related issue arose when I started seeing *Season_number* results that were nonsensical.  Sure, Patrick Ewing had a long, wonderful career, but he didn't play 30 years in the Association.  I discovered that numerous players had the same name--so joining my dataframes on player name was problematic.  There are several Juniors in the league: Ewing, Tim Hardaway, Glenn Robinson, and Gary Payton. Further, there's also some more common names for unrelated players--e.g., Mike James and Chris Johnson. To solve this, I manually had to clean some of the data and write logic to differentiate players in my data input module (*data_wrangle*).

### Mitigating Injuries

Injuries make predicting performance difficult.  When a good player misses a good portion of their season, that can throw off predictions for a non-rate-based stat like Win-Shares, especially if the player is the best player on his team.

One way to mitigate this was to only include players that had data for seasons 1-9 in my train-test split, which required some filtering.

Another issue is that a pure average of the first four seasons of data did not *seem* like it would accurately capture trends in performance, especially when players improved, but may have missed time in third or fourth years. My earliest results actually showed the opposite--a "regular" mean of seasons 1-4 outperformed my model with various weighted means.

But, as I selected different features to train upon and reduced the number of features trained, I found that a weighted mean (with weights equal to *Seasons_number* * games played in that season) tended to provide smaller errors.

## Feature Search

I wrote a "grid" search script--although for this search I did not optimize hyperparameters for my regressors.  Instead, I attempted to find the optimal number of features, what those features were, and the best "mean" function for averaging players' first four years in the Association.  

My best results XXXX.


## Example Output

My test set included a wide range of players, from (future) Hall-of-Famers (Kobe Bryant, Dwyane Wade, Steve Nash) to excellent/very good players (Shawn Marion, Antwan Jamison, Stephon Marbury, and Cuttino Mobley) to guys at the league minimum-level (Shannon Brown).

Generally, for the best players, the model tends to under-predict the player's performance.

<img src=“images/Kobe_Bryant.png” width=“200" height=“100” />]

[Steve]

[Dwyane Wade]

You can also see the dip at year 5 of Wade's actual win shares.  This result is a function of a couple things.  First, Dwyane Wade missed about a third of the season--so it's hard to accumulate win shares when you aren't on the floor.  Second, the Heat weren't very good.  They won a measly 15 games.  So while Wade did not play very much, he still accounted for about 30% of the Heat's wins.  Not half bad.

But this also highlights using a non-rate-based stat like win shares as a the measure of performance.  Good players on bad teams are

For good--but not great--players, the model seemed to bounce around between over- and under-predicting.

[Antawn Jamison]

[Cuttino Mobley]

For the players closer to the league minimum level, the model tended to over-predict the player's performance.

[Shannon Brown]

[Jakob]

## LeBron is Good, Machine Learning Told me So.

LeBron is an outlier.

I performed a hierarchical clustering analysis with player data from years one through four. Hierarchical clustering iteratively groups observations (here, players) together based on their similarities. These similiarities are displayed on a dendrogram. The height of connections between players indicates their similarity--the lower the height of the connection, the more similar the players are.

This dendrogram shows the linkage between players using "average" linkage--which means that the distance between two clusters is the average distance between each point in one cluster to another. For a distance metric, I used Eucilidean distance (the straight-line distance between two points).

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "All Player Seasons")

## Next Steps

* Explore using different regressors--especially Gradient Boosted Trees.

* Incorporate shot selection data (distance of each shot, pulled from play-by-play data).

* Provide an actual salary recommendation.
