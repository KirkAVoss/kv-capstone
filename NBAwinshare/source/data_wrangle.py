import pandas as pd
import re
from os import listdir
import matplotlib.pyplot as plt


def read_advanced_season_stats(filepath):
    '''
    Function reads in the file at 'filepath' and returns a dataframe of the advanced stats
    Inputs: filepath--a path to the file (*advanced.csv)
    Returns: dataframe of per season advanced stats
    '''

    #Right now the Rk column is left in, I might want to combine it (zeropadded) with the season id to get
    #a unique player-row for the join, instead of doing a player-season-join

    df = pd.read_csv(filepath)
    #pull the seasonal years from the filepath
    years = re.findall(r"\d\d\d\d",filepath)
    #remove the "blank" columns that were added via the data mining recipe
    df.drop(['Blank', 'Blank.1'], axis=1, inplace=True)
    #Get the ending year for the season
    df['Season'] = int(years[-1])

    #Handle multiple teams, initialize to the 'Tm' field
    df['Teams'] = df['Tm']

    #Get rid of multiple rows per season per player
    df = reduce_traded_players_to_one_row(df)

    #rename minutes_played to avoid the collision with the _per_season minutes_played column
    df.rename({'MP':'MP_total'}, axis='columns', inplace=True)

    return df #.sort_values(['Season', 'Player'], ascending=[True, True])

def read_pergame_season_stats(filepath):
    '''
    Function reads in the file at 'filepath' and returns a dataframe of the per_game stats
    Inputs: filepath--a path to the file (*advanced.csv)
    Returns: dataframe of per season advanced stats
    '''
    df = pd.read_csv(filepath)
    #pull the seasonal years from the filepath
    years = re.findall(r"\d\d\d\d",filepath)
    df['Season'] = int(years[-1])

    #Handle multiple teams, initialize to the 'Tm' field (We're going to drop this, but it's needed to work with
    #reduced_traded_players_to_one_row)
    df['Teams'] = df['Tm']

    #Get rid of multiple rows per season per player
    df = reduce_traded_players_to_one_row(df)

    #Let's drop the columns that are duplicative of the advanced stats
    columns_to_drop = ['Pos', 'Age', 'Tm', 'G', 'Teams']
    df.drop(columns_to_drop, axis=1, inplace=True)

    df.rename({'MP':'MP_pergame'}, axis='columns', inplace=True)

    return df #.sort_values(['Season', 'Player'], ascending=[True, True])

def reduce_traded_players_to_one_row(df):
    '''
    Reduces the traded players in the dataframe to one row.  Should be called on an individual seasonal dataframe
    because that's how the function was tested. Puts the invidual teams in a comma-delimited string
    ***Input DF is modified by this function***

    Input: seasonal dataframe (per_game or advanced)
    return: formatted dataframe (the same one passed in) with one row per payer
    '''
    #Each player that has been traded has 'TOT' in the Team column
    for player in df[df['Tm']=='TOT']['Player']:
        #get the unique teams in the list
        teams = list(df[df['Player']==player]['Tm'].unique())
        #remove the 'TOT' in the list
        teams.remove('TOT')
        #print('Should append: ', ','.join(teams))

        #Put the multiple teams in the 'Teams' field for the TOT column and player
        df.loc[(df['Tm']=='TOT') & (df['Player']==player), 'Teams'] = ','.join(teams)

    #Because the 'TOT' row appears first, we can drop duplicates
    df.drop_duplicates(subset=['Player'], inplace=True)

    return df

def read_all_advanced(pathtodir):
    '''
    Read every advanced stat file into separate dataframes
    Concats the per_season dataframes together, and returns a big dataframe

    Input: pathtodir -- the path to the directory that contains the per_season advanced stat csv files
    NOTE: the directory should only have advanced stat files within.  Do not mix file types.
    Returns: dataframe of all advanced stats, uncleaned
    '''
    #get the individual files
    files = listdir(pathtodir)
    #get a list of dataframes, one for every file
    dataframes = [read_advanced_season_stats(pathtodir + '/' + file) for file in files]
    #assemble the dataframes together, and return them.
    return pd.concat(dataframes).sort_values(['Season', 'Player'], ascending=[True, True])

def read_all_pergame(pathtodir):
    '''
    Read every per_game stat file (one for each season) into separate dataframes
    Concats the per_game dataframes together, and returns a dataframe that contain the per_game_stats for every
    season in the directory

    Input: pathtodir -- the path to the directory that contains the per_season per_game stat csv files
    NOTE: the directory should only have per_game stat files within.  Do not mix file types within the directory.
    Returns: dataframe of all per_game stats, uncleaned
    '''
    #get the individual files
    files = listdir(pathtodir)
    #print(files)
    #get a list of dataframes, one for every file
    #Had some bad data, so had to troubleshoot, seems to be working now after fixing some of the csvs
    #for file in files:
    #    print('Reading',file)
    #    df = read_pergame_season_stats(pathtodir + '/' + file)
    dataframes = [read_pergame_season_stats(pathtodir + '/' + file) for file in files]
    #assemble the dataframes together, and return them.
    return pd.concat(dataframes).sort_values(['Season', 'Player'], ascending=[True, True])


def plot_histogram(df, colname, season, bins=10, xlabel = None, alpha = .25):
    '''
    Plots a histogram of the dataframe, based on the column name and the season
    df: input dataframe (pandas dataframe)
    colname: e.g., 'WS' for Win shares (string)
    season: e.g, 2018 (integer)

    Returns: Nothing
    '''
    df[df['Season'] == season][colname].hist(bins=bins)
    plt.title(colname + ' for the ' + str(season) + ' Season')
    plt.ylabel('Count')
    plt.xlabel(xlabel)

def clean_and_join_seasonal_dataframe(df_advanced, df_pergame):
    '''
    Fills the seasonal dataframes with 0 for their nans and returns a joined, cleaned dataframe
    Inputs: df_pergame dataframe, read in by read_pergame_season_stats
            df_advanced dataframe, read in by read_advanced_season_stats

    Returns: combined dataframe of pergame and advanced stats
    '''

    #Merge on dataframe, by player and season
    joined_df = pd.merge(df_advanced, df_pergame, how='left', left_on=['Player','Season'], right_on = ['Player','Season'])

    #Based on EDA, most of the stats with NANs come from low-minutes players who haven't done much in-game
    #also, using the fill in-place because I've had trouble with fillna not working in the past.
    joined_df.fillna(0, inplace=True)

    #dropped the ranks if they are still in (might modify earlier)
    if 'Rk_x' in joined_df:
        joined_df.drop('Rk_x',axis=1, inplace=True)
    if 'Rk_y' in joined_df:
        joined_df.drop('Rk_y',axis=1, inplace=True)

    #Reset the index because it looks weird
    joined_df = joined_df.reset_index(drop=True)

    #Get rid of basketball reference's * used to denote HOF players
    joined_df['Player'] = joined_df['Player'].str.replace('*', '', regex=False)

    #Handle repeated names
    repeats = ['Charles Jones', 'Charles Smith', 'Chris Johnson', 'Chris Wright',
       'Dee Brown', 'Gary Payton', 'Glen Rice', 'Glenn Robinson',
       'Marcus Williams', 'Mike James', 'Patrick Ewing',
       'Reggie Williams', 'Tim Hardaway']

    #Patrick Ewing Splits
    joined_df.loc[(joined_df['Player']=='Patrick Ewing') & (joined_df['Season'] < 2003),'Player']= "Patrick Ewing (i)"
    joined_df.loc[(joined_df['Player']=='Patrick Ewing') & (joined_df['Season'] > 2003),'Player']= "Patrick Ewing (ii)"

    #Charles Jones Splits
    joined_df.loc[(joined_df['Player']=='Charles Jones') & (joined_df['Season'] < 1999),'Player']= "Charles Jones (i)"
    joined_df.loc[(joined_df['Player']=='Charles Jones') & (joined_df['Season'] >= 1999),'Player']= "Charles Jones (ii)"

    #Chris Johnson Splits (they overlapped, so differentiate on position)
    joined_df.loc[(joined_df['Player']=='Chris Johnson') & (joined_df['Pos'] == 'C'),'Player']= "Chris Johnson (i)"
    joined_df.loc[(joined_df['Player']=='Chris Johnson') & (joined_df['Pos'] == 'SF'),'Player']= "Chris Johnson (ii)"

    #Charles Smith Splits (they overlapped, so differentiate on position)
    joined_df.loc[(joined_df['Player']=='Charles Smith') & (joined_df['Season'] < 1998),'Player']= "Charles Smith (i)"
    joined_df.loc[(joined_df['Player']=='Charles Smith') & (joined_df['Season'] >=1998),'Player']= "Charles Smith (ii)"


    #Chris Wright (they overlapped, so differentiate on position)
    joined_df.loc[(joined_df['Player']=='Chris Wright') & (joined_df['Pos'] == 'SF'),'Player']= "Chris Wright (i)"
    joined_df.loc[(joined_df['Player']=='Chris Wright') & (joined_df['Pos'] == 'SG'),'Player']= "Chris Wright (ii)"

    #Dee Brown Splits
    joined_df.loc[(joined_df['Player']=='Dee Brown') & (joined_df['Season'] < 2003),'Player']= "Dee Brown (i)"
    joined_df.loc[(joined_df['Player']=='Dee Brown') & (joined_df['Season'] > 2006),'Player']= "Dee Brown (ii)"

    #Gary Payton Splits
    joined_df.loc[(joined_df['Player']=='Gary Payton') & (joined_df['Season'] < 2008),'Player']= "Gary Payton (i)"
    joined_df.loc[(joined_df['Player']=='Gary Payton') & (joined_df['Season'] > 2016),'Player']= "Gary Payton (ii)"

    #Glen Rice Splits
    joined_df.loc[(joined_df['Player']=='Glen Rice') & (joined_df['Season'] < 2005),'Player']= "Glen Rice (i)"
    joined_df.loc[(joined_df['Player']=='Glen Rice') & (joined_df['Season'] > 2013),'Player']= "Glen Rice (ii)"

    #Glenn Robinson
    joined_df.loc[(joined_df['Player']=='Glenn Robinson') & (joined_df['Season'] < 2006),'Player']= "Glenn Robinson (i)"
    joined_df.loc[(joined_df['Player']=='Glenn Robinson') & (joined_df['Season'] > 2014),'Player']= "Glenn Robinson (ii)"

    #Marcus was more difficult, I edited the data to make SAS-F Marcus to be 'Marcus (ii)''

    #Mike James
    joined_df.loc[(joined_df['Player']=='Mike James') & (joined_df['Season'] < 2015),'Player']= "Mike James (i)"
    joined_df.loc[(joined_df['Player']=='Mike James') & (joined_df['Season'] > 2015),'Player']= "Mike James (ii)"

    #Reggie Williams
    joined_df.loc[(joined_df['Player']=='Reggie Williams') & (joined_df['Season'] < 1998),'Player']= "Reggie Williams (i)"
    joined_df.loc[(joined_df['Player']=='Reggie Williams') & (joined_df['Season'] > 1998),'Player']= "Reggie Williams (ii)"

    #Tim Hardaway Splits
    joined_df.loc[(joined_df['Player']=='Tim Hardaway') & (joined_df['Season'] < 2004),'Player']= "Tim Hardaway (i)"
    joined_df.loc[(joined_df['Player']=='Tim Hardaway') & (joined_df['Season'] > 2004),'Player']= "Tim Hardaway (ii)"

    #Tony Mitchell Splits (both played in 2014)
    joined_df.loc[(joined_df['Player']=='Tony Mitchell') & (joined_df['Tm'] == 'DET'),'Player']= "Tony Mitchell (92)"
    joined_df.loc[(joined_df['Player']=='Tony Mitchell') & (joined_df['Tm'] == 'MIL'),'Player']= "Tony Mitchell (89)"


    return joined_df.sort_values(['Player', 'Season'], ascending=[True, True])


def read_demographic_data(filename):
    '''
    Reads in demographic data of the player, including, most importantly for this analysis, start-year and end-year
    Input: filename (path to file of player_data.csv)
    Returns: dataframe of demo info
    '''
    df = pd.read_csv(filename)
    return df


def add_years_in_league(df_seasonal, df_demographic):
    '''
    Adds the number of years the player has been in the league to the seasonal dataframe.
    Calculates the delta from the demo database
    Inputs: df_seasonal -- the output of the clean_and_join_seasonal_dataframe function
            df_demographic -- the output of the read_demographic_data function

    Returns: df_seasonal_plus_years_in_league

    '''
    #Was going to loop through and get unique names, realized that could be obviated by left-join
    #names_in_demo = set(df_demographic['name'].unique())
    #names_in_seaonal = set(df_seasonal['Player'].unique())

    #Left merge the two dataframes on player name, which exclude the old-timers that aren't in 1997+
    joinedup = pd.merge(df_seasonal, df_demographic.loc[:,['name', 'year_start']], how='left', left_on=['Player'], right_on = ['name'])

    #The players that aren't in the demo table are 1st year G-league-level guys
    joinedup.loc[joinedup['year_start'].isnull(),'year_start']= 2018
    #Cast the year_start column to int because Pandas is goofy
    joinedup['year_start'] = joinedup['year_start'].astype(int)

    #Get the season number in the table, which is just the number of years the player has been in the league
    #Note that the player's rookie year starts at 1
    joinedup['Seasons_number'] = joinedup['Season'] - joinedup['year_start'] + 1

    #Dropped the name and year_start--don't think it makes sense to duplicate the name and year_start repeats
    joinedup.drop(['name','year_start'],axis=1,inplace=True)

    return joinedup
