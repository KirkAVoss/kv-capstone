## Final Capstone Proposal

**NBA Win-Share Estimator**:

1. Background and Motivation

National Basketball Association ("NBA") contracts for rookies are are guided by the collective bargaining agreement ("CBA") between the NBA and NBA players's union.  Rookie contracts are set by a scale--each player can negotiate their contract between 80% to 120% of the scale.  However, every rookie contract follows the same format--a two year contract, followed by two years of "team options."  This means that the drafting team has the option to continue to employ the player on the "rookie scale."  The player has little negotiating power.

For talented players, this team option means that the first time an NBA team must make a "real" salary determination is between a player's 2nd and 3rd years.  And again, between the 3rd and 4th years, the team can exercise its option to keep the player employed.  But these 3rd and 4th year option *prices* are set on the rookie scale.  So there's not much price negotiation at this point in a player's career.

The first "good" opportunity for a payday comes on the player's foray into free-agency.  Thus, for players with success in the early stages of their career, this opportunity arrives between their 4th and 5th year.

Consequently, there is a need to objectively assess the player's ability to help a team win basketball at this stage.  Often, contracts for professional athletes pay the athlete for their performance in *the past*.  In other words, contracts reflect the player's previous performance, but because of age (or other factors), that performance declines during the course of their "big" contract.  That leaves team management with underperforming, expensive assets.

Using historic and current game and season stats, I attempt to predict the shape of an NBA player's career based on their contribution to winning basketball--memorialized in the number of wins that player provides for his team (e.g., Win Shares).  I seek to correlate those wins to a salary range, as a percentage of salary cap.

*Previous Approaches*

The most notable work related to predicting player performance has been FiveThirtyEight.com's CARMELO player projection system.  FiveThirtyEight.com iterates on the CARMELO system annually and should provide a good baseline for comparison.

CARMELO's backbone "is an algorithm that compares current players to past ones who had statistically similar profile through the same age." See https://fivethirtyeight.com/features/our-nba-player-projections-are-ready-for-2018-19/.  CARMELO mostly relies on a blend of RPM (real-plus-minus) and BPM (box-plus-minus). Id.  The CARMELO system also uses in-season ELO ratings (hence the "ELO" in CARMELO) to update the ranking.  FiveThirtyEight is currently mulling over overhauling their in-season update mechanic.

Obviously, I intend to utilize an approach that leverages advanced stats such as BPM to predict career arcs, but I also want to explore how (or even *if*) a player's teammates affect his development.  To wit, in his Hall-of-Fame induction speech, Steve Nash thanked Michael Finley (a former Dallas Maverick borderline-All Star in the late 90s and early 00s) for his influence on both Nash and Dirk Nowitzki during their developmental years.  Hopefully, playing with efficient, non-ball dominant veterans early in a player's career has a positive impact of their career arcs.  It will be interesting to see if the data supports this.

2.  Methodology and Technology Stack (Data Sources and Format)

I scraped Basketball-Reference.com for initial datasets for all players from 1997 to the previous completed season.  To pull advanced stats, I utilized the Google Chrome extension Data Miner and created a "recipe" to gather data.  Currently, I have this data stored in CSV format.  I have also pulled pre-1997 stats for players, but that data exclude advanced stats.  The current data size is around 13 MB.

For historical salary information, I plan on scarping hoopshype.com.

<Data processing comprised . . .>


3. How will you present your work?  
  * Web app--I'd still prefer to create a web-app, but working with some web-based technology last week reminded me of why I often avoided it.  If I am far enough along, I may try to do a web-app, but I suspect that I will make slides.

4. Potential Problems

I suspect that the changing landscape in the *post-Warriors* meta will make predicting by position more difficult, as positions seem to matter much less.  I want to avoid manually classifying players as much as possible (like calling Kevin Durant a shooting big, or try to force Kristaps Porzingas into a mold). One solution might be to ignore position, but as the NBA converges to a wing-centric meta (big 2s, regular 3s, and stretch 4s), that will prove difficult.



5. Next Steps

My next steps are to pull salary information and determine if I can pull historical advanced stats.
