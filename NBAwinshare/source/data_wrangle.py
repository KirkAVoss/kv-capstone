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

    return joined_df.sort_values(['Player', 'Season'], ascending=[True, True])


def read_demographic_data(filename):
    '''
    Reads in demographic data of the player, including, most importantly for this analysis, start-year and end-year
    Input: filename (path to file of player_data.csv)
    Returns: dataframe of demo info
    '''
    df = pd.read_csv(filename)
    return df
