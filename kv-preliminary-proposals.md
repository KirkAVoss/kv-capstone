## KV Capstone Preliminary Proposal 

**Capstone Ideas**:

My three capstone proposals are (in order of data-availability, highest to lowest):

1. A win-share estimator for NBA players.
2. A outcome predictor for Destiny player-versus-player ("PVP") matches.
3. A commercial real estate ("CRE") deal classifier.

**NBA Win-Share Estimator**:

1. High level description of project.

I want to predict the effectiveness of NBA players--especially those coming off their Rookie contracts.  More specifically, I want to analyze season-based stats and game-specific stats to get an objective prediction of how young NBA players will fare when during their first "big" (i.e., non-Rookie) contract.

2. What question or problem are you trying to solve?

Because Rookie contracts are set by the NBA's collective bargaining agreement ("CBA"), the first time any NBA executive has to make a "real" contract decision for the rookie is after the expiration of the Rookie contract.  That can lead to drastically over paying Rookies based on perceived skill or potential--versus what the Rookie actually provides to the team (e.g., portions of wins accountable to the Rookie's performance).  I hope to help provide an objective guidepost for the player's salary.

3. How will you present your work?  
  * Web app--I'd prefer to develop a web-app, but I have zero web app experience, so I will probably default to slides
4. What are your data sources?

I expect to be able to get most of my data from Basketball-Reference.com, but I may have to scrape some from ESPN or pull some from Synergy (but they have a paywall, so I'd like to avoid that)

5. What’s your next step towards making this your project.

I need to pull the available data from Basketball-Reference.com

**Destiny PVP Analyzer**

1. High level description of project.

I want to predict the outcome of Destiny PVP matches.  Destiny--an online-only FPS where you shoot aliens (and other people) in the face in search of better loot--has various game modes were teams of differing sizes compete.  One team wins based on the game mode (total enemies defeated, rounds won, territory controlled, etc.)

2. What question or problem are you trying to solve?

One of the major issues with any multi-player game is proper matchmaking (the process of finding opponents waiting in queue).  Lop-sided teams can run up the score quickly against less-skilled (or less coordinated) opponents--ruining the fun of those less-skilled players, causing them to stop playing.   If Bungie (Destiny's developer) can predict with certainty that one team will crush the other, then it could either reshuffle teams or find a different match.   

3. How will you present your work?  
  * Web app--Again, I'd prefer to develop a web-app, but I have zero web app experience, so I will probably default to slides.
4. What are your data sources?

My data will likely come from Bungie's Destiny API, along with information available at DestinyTracker.com.

5. What’s your next step towards making this your project.

I have been able to pull Playstation-player data from Bungie's API (by player name) , but not  XBox- or PC-player data.  I need to figure out if I can only retrieve player-data, or if I can get match-level data without having to scrape for a bunch of users (whose handles it will be difficult to collect).  

**CRE Deal Classifier**

1. High level description of project.

I want to classify the outcome of potential CRE deals (successful or not).  I want to analyze various deal metrics to automate the process of deal analysis

2. What question or problem are you trying to solve?

CRE analysis, while it _should be_ objective, suffers from all things that have human involvement--personal bias. Some analysts push a deal for personal reasons (they originate them, they fall in love with some aspect of the deal). I want to create a first-pass filter to remove suspect deals--saving time and man-hours.

3. How will you present your work?  
  * Slides--Again, I'd prefer to develop a web-app, but given this information would likely be proprietary, a slide presentation probably makes the most sense 
4. What are your data sources?

My data would come from a small regional bank in South Texas, most likely in the form of numerous Excel spreadsheets.  I have a familial relationship with the bank's Chief Credit Officder, so I can probably get the data without too much trouble (probably an NDA or even without an NDA with some data sanitation on the bank's end). My overriding concern is that there is simply not enough deals to train a model (probably less than 100 deals). 

5. What’s your next step towards making this your project.

I have had discussions about getting the data. I will follow-up during review week.  It will probably be a fun project regardless of whether I do it as my capstone.   