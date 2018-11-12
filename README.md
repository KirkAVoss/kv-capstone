## Final Capstone Proposal

**NBA Win-Share Estimator**:

1. Background and Motivation

National Basketball Association ("NBA") contracts for rookies are are guided by the collective bargaining agreement ("CBA") between the NBA and NBA players's union.  Rookie contracts are set by a scale--each player can negotiate their contract between 80% to 120% of the scale.  However, every rookie contract follows the same format--a two year contract, followed by two years of "team options."  This means that the drafting team has the option to continue to employ the player on the "rookie scale."  The player has little negotiating power.

For talented players, this team option means that the first time an NBA team must make a "real" salary determination is between a player's 2nd and 3rd years.  And again, between the 3rd and 4th years, the team can exercise its option to keep the player employed.  But these 3rd and 4th year option *prices* are set on the rookie scale.  So there's not much price negotiation at this point in a player's career.

The first "good" opportunity for a payday comes on the player's foray into free-agency.  Thus, for players with success in the early stages of their career, this opportunity arrives between their 4th and 5th year.

Consequently, there is a need to objectively assess the player's ability to help a team win basketball at this stage.  Often, contracts for professional athletes pay the athlete for their performance in *the past*.  In other words, contracts reflect the player's previous performance, but because of age (or other factors), that performance declines.  That leaves team management with underperforming, expensive assets.

Using historic and current game and season stats, I attempt to predict the shape of an NBA player's career based on their contribution to winning basketball--memorialized in the number of wins that player provides for his team (e.g., Win Shares).  I seek to correlate those wins to a salary range, as a percentage of salary cap.

*Previous Approaches*

The most notable approach

2.  Methodology and Technology Stack

I scraped Basketball-Reference.com for initial datasets for all players from 1997 to the previous completed season.  To pull advanced stats, I utilized the Google Chrome extension Data Miner and created a "recipe" to gather data.

For historical salary information, I scraped hoopshype.com.

<Data processing comprised . . .>

<Challenges . . . I suspect that the changing landscape in the *post-Warriors* meta will make predicting by position more difficult>

3. How will you present your work?  
  * Web app--I'd prefer to develop a web-app, but I have zero web app experience, so I will probably default to slides.
4. What are your data sources?

I expect to be able to get most of my data from Basketball-Reference.com, but I may have to scrape some from ESPN or pull some from Synergy Sports (which has a paywall, so I'd like to avoid relying on Synergy).

5. What’s your next step towards making this your project?

I need to pull the available data from Basketball-Reference.com.
