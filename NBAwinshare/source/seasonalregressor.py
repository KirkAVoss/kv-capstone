import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
#from sklearn.linear_model import LogisticRegression
#from sklearn.metrics import precision_score, recall_score, confusion_matrix
#import seaborn as sn
#from scipy import stats
#import pickle

class SeasonalRegressor():
    '''
    Creates a Seasonal Regressor object
    '''


    def __init__(self, regressor_type='RF', columns_to_train='all'):
        '''
        Instantiates a model
        Input: regressor_type -- type of regressor used in the prediction algo, defaults to random forest (only option operative)
                columnes_to_train -- the columns used to train the model
        '''
        #these are the years to predict
        self.years_to_predict = [5, 6, 7, 8, 9]
        self.regressor_dict = {}
        self.columns_to_train = columns_to_train
        self.column_names = None
        for year in self.years_to_predict:
            if regressor_type == 'RF':
                #Need to figure out how to pass arguments to this thing for grid search purposes
                self.regressor_dict[year] = RandomForestRegressor(n_jobs = -1, oob_score = True, n_estimators = 100)
            else:
                print("Don't know what to do with this, sorry, chief.")


    def fit(self, df_fullstats, df_demographic, col_to_predict='WS'):
        '''
        Fits the df_fullstats data to the regressor dictionary

        Inputs: df_fullstats -- a dataframe that has all data player data in it .
                    Should be result of data_wrangle.add_years_in_league
                    Should NOT have player name as index, it should be in a 'Player'

                df_demographic -- should be the demographic dataframe read in via data_wrangle

                columns_to_train -- a list of columns, from within fullstats to train on.  Defaults to 'all'

                col_to_predict -- The column we are trying to predict from df_fullstats['Season_number']==(last_train_season +  1): 'WS' by default


        Returns self
        '''
        #Fit every year in years to predict
        for year in self.years_to_predict:
            #Create an X and y for each year.  Note the year-1 used as the argument on last_train_season
            X, y, _ = self.create_train_and_predict_X_and_y_for_season_range(df_fullstats, df_demographic, \
            col_to_predict = col_to_predict, columns_to_train = self.columns_to_train, last_train_season= year-1)
            print("Fitting for year:", year)
            #Fit the regressor at each year
            self.column_names = list(X.columns)
            self.regressor_dict[year] = self.regressor_dict[year].fit(X,y)

        return self


    def predict(self, df_fouryearstats):
        '''
        Predict win-shares (by default) for df_fouryearstats, which should have the first-4 years of a player's career
        df_fouryearsstats -- input dataframe with player seasons 1-4, Each season on a different row, with 'Player' as a column,
            not the index.

        Returns y (prediction dictionary with player name as 'key' and list of predictions as 'values')

        '''
        predictions = defaultdict(list)
        #This functionality should mirror what I do in create_train_and_predict
        #Mean should be replaced with a custom function
        playerframe = df_fouryearstats.groupby('Player').mean().sort_index()
        players = set(playerframe.index)

        #Doing nested for-loop so that I can easily keep predictions together
        for year in self.years_to_predict:
            #For each player
            for player in players:
                print("Predicting year:", year, "for player: ",player)
                #Call the regressor for each year,might need to cast to a float
                #Super-readable?
                if self.columns_to_train == "all":
                    predictions[player].append(float(self.regressor_dict[year].predict(playerframe.loc[player,:].values.reshape(1, -1))))
                else:
                    predictions[player].append(float(self.regressor_dict[year].predict(playerframe.loc[player,self.columns_to_train].values.reshape(1, -1))))

        return predictions

    def create_train_and_predict_X_and_y_from_seasons_4_and_5(self, df_season_4, \
        df_season_5, demographic, columns_to_train, col_to_predict='WS'):
        '''
        This function takes the seasonal information from year 4 (all players and all
        season-4's) and creates an "X" dataframe, and a "y" dataframe for use with training
        Inputs: df_season_4 -- a dataframe filtered to only have year-4 data
                    should NOT have player name as index, it should be in 'Player'
                ***NOTE*** Shouldn't have previous year stats
                df_season_5 -- a dataframe filtered to only have year-5 data
                    should NOT have player name as index, it should be in 'Player'

                demographic -- should be the demographic database read in via data_wrangle
                ***NOTE*** Shouldn't have previous year stats
                columns_to_train -- a list of columns, from within df_season_4 to train on
                col_to_predict -- The column we are trying to predict from df_season_5: 'WS' by default

        Returns X - dataframe reduced to columns_to_train that has corresponding values in Y
                y - dataframe containing the col_to_predict, where previous year players
        '''

        #filter the df_season
        df_season_4_reduced = df_season_4[columns_to_train]
        df_season_4_reduced = df_season_4_reduced.set_index('Player').sort_index()

        to_predict = df_season_5[['Player',col_to_predict]]

        #list for rows to add to the predicted dataframe
        rows_to_add = []

        #Get the players from season 4 and season 5
        year4players = set(df_season_4['Player'])
        year5players = set(df_season_5['Player'])

        #Let's check for players that played in year 4 but didn't start in 2015--thus, these are players
        #who should have played in the league in year 5 (maybe they were injured, played in another league, or retired)
        for player in year4players:
            if player not in year5players and not (demographic[demographic['name']==player]['year_start'] == 2015).bool():
                #print(player, "is not in year 5 and didn't start in 2015; started in: ", int(demographic[demographic['name']==player]['year_start']))
                #fill with zeroes
                rows_to_add.append([player, 0])

        #create the to-predict dataframe based on the player name and desired col_to_predict, reset the index, and sort
        to_predict_dataframe = to_predict.append(pd.DataFrame(rows_to_add, columns = ['Player', col_to_predict])).set_index('Player').sort_index()

        #Get the players who are in the to-predict dataframe
        guys_in_the_predict = set(to_predict_dataframe.index.values)

        #We need to remove the 4-year players who have no 5th year
        guys_to_remove_from_year_4df = year4players - guys_in_the_predict
        #We need to remove the 5-year players who have no 4th year (surprisingly many)
        guys_to_remove_from_predict = guys_in_the_predict - year4players

        #Do the removal from the season_4 dataframe
        for player in guys_to_remove_from_year_4df:
            df_season_4_reduced.drop(player,inplace=True)

        #Do the removal from the prediction dataframe
        for player in guys_to_remove_from_predict:
            to_predict_dataframe.drop(player,inplace=True)

        #Do some checking to make sure we didn't screw up
        trainidx = set(df_season_4_reduced.index.values)
        predictidx = set(to_predict_dataframe.index.values)
        #if not trainidx^predictidx:
        #    print("Something went wrong with the indices (1):", trainidx^predictidx)
        #    return None
        if not (df_season_4_reduced.index.equals(to_predict_dataframe.index)):
            print("Something went wrong with indices (2)--don't equal each other")
            return None

        #return the dataframes
        return df_season_4_reduced, to_predict_dataframe

    def create_train_and_predict_X_and_y_for_season_range(self, df_fullstats, \
    demographic, last_train_season=4, columns_to_train='all', col_to_predict='WS'):
        '''
        This function takes the seasonal information from years 1- (all players and all
        season-4's) and creates an "X" dataframe, and a "y" dataframe for use with training
        Inputs: df_fullstats -- a dataframe that has all data player data in it .
                    Should be result of data_wrangle.add_years_in_league
                    Should NOT have player name as index, it should be in a 'Player'

                demographic -- should be the demographic database read in via data_wrangle

                last_train_season - should be the final year to get the train-set.  Used to set the end-date
                    for the X frame.  Thus, last_train_season==4 will return the first four seasons (meaned)

                    The predicted season will be the (last_train_season + 1)

                columns_to_train -- a list of columns, from within fullstats to train on.  Defaults to all

                col_to_predict -- The column we are trying to predict from df_fullstats['Season_number']==(last_train_season +  1): 'WS' by default

        Returns X - dataframe reduced to columns_to_train that has corresponding values in Y
                y - dataframe containing the col_to_predict, where previous year players are in X
                players - set of player names that have full data for years 1-last_train_season+1
        '''

        seasons_needed = set(range(1,last_train_season+1))
        seasons_only_for_train = set(range(1,last_train_season+1))
        season_to_predict = last_train_season+1
        seasons_needed.add(season_to_predict)

        count = 0
        players_with_fulldata = set()

        #for every unique player in fullstats, let's figure out who we have data for in years: 1-last_train_season
        for player in df_fullstats['Player'].unique():
            #get the Season_numbers we have per player
            playerset = set(df_fullstats.loc[df_fullstats['Player']==player, 'Seasons_number'])
            #if the player has every year, append to the set of full players
            if seasons_needed.issubset(playerset):
                #print("Have full-year stats ",player)
                players_with_fulldata.add(player)
                count += 1
        print("Number of players: ", count, " with full season data for seasons:", seasons_needed)


        #Get the player-rows that we want to train and predict upon.  This step could be combined with the next two below,
        #but I include for readability
        df_only_full_players = df_fullstats[(df_fullstats['Player'].isin(players_with_fulldata)) &  (df_fullstats['Seasons_number'] <= last_train_season + 1)]

        #Just want the train set (Seasons 1-last_train_season)
        df_full_train = df_only_full_players[df_only_full_players['Seasons_number'] <=  last_train_season]

        #Get the to-predict set (the season AFTER the last_train_season)
        df_full_predict = df_only_full_players[df_only_full_players['Seasons_number'] ==  last_train_season+1]

        #Here is where I want to apply a custom function, something more heavily weighted towards most recent
        #seasons.  Currently, I just use the built-in groupby-mean.  That doesn't capture trajectories very well.
        #And it certainly screws up if the predict set has something funky in it.  Like Al Horford playing 11 games in year 5
        df_transformed_train = df_full_train.groupby('Player').mean().sort_index()

        #Re-index the predict frame
        df_reindexed_predict = df_full_predict.set_index('Player').sort_index()

        #Error checking, make sure indices are good
        if df_transformed_train.index.equals(df_reindexed_predict.index):
            print("Indices of train set and to-predict set MATCH")
        else:
            print("Indices of train set and to-predict DO NOT match:")
            print(df_transformed_train.index.difference(df_reindexed_predict.index))
            return (None, None, None)

        #filter the columns
        if columns_to_train == "all":
            print("Using all columns")
            X = df_transformed_train
        else:
            print("Using columns: ",columns_to_train)
            X = df_transformed_train[columns_to_train]

        #grab the column to predict as y
        y = df_reindexed_predict.pop(col_to_predict)

        return X, y, players_with_fulldata

    def get_players_first_x_full_years(self, df_fullstats, season=4):
        '''
        Returns the first x years foreach player, if there is full data for that player

        Inputs -- seasons that you need the full data
        '''

        seasons_needed = set(range(1,season+1))

        count = 0
        players_with_fulldata = set()

        #for every unique player in fullstats, let's figure out who we have data for in years: 1-last_train_season
        for player in df_fullstats['Player'].unique():
            #get the Season_numbers we have per player
            playerset = set(df_fullstats.loc[df_fullstats['Player']==player, 'Seasons_number'])
            #if the player has every year, append to the set of full players
            if seasons_needed.issubset(playerset):
                #print("Have full-year stats ",player)
                players_with_fulldata.add(player)
                count += 1
        print("Number of players: ", count, " with full season data for seasons:", seasons_needed)

        #Get the player-rows that we want to predict.  This step could be combined with the next below,
        #but I include for readability
        df_only_full_players = df_fullstats[(df_fullstats['Player'].isin(players_with_fulldata)) &  (df_fullstats['Seasons_number'] <= season)]

        return df_only_full_players

    #Could probably move this function out of the class, or at least make static
    def plot_player_arc(self, playername, predictions, predseasons= [5,6,7,8,9], actuals=None, actualseasons=None):
        '''
        Plots the player arc based on predictions
        Inputs: playername - string - player name for the predictions
                predictions - array of predicted values (Win Shares)
                seasons - the seasons (x-axis)
                actuals - array of actual values to plot against the predicted values
        '''
        plt.title('WinShare Predictions for ' + playername + '')
        plt.ylabel('Win Shares')
        plt.xlabel('Seasons')


        #plot the predicted seasons
        plt.plot(predseasons, predictions)
        if actuals.any():
            plt.plot(actualseasons, actuals)
            plt.xticks(actualseasons)
        else:
            plt.xticks(predseasons)

        plt.legend(['Predictions', 'Actuals'], loc='upper right')
        plt.show()








    # #this probably doesn't make sense, but don't want to delete it yet
    # def confusion_matrix(self, ytest, ypred):
    #     '''Function prints the precision score, recall score, and plots the confusion matrix.'''
    #     tn, fp, fn, tp = confusion_matrix(ytest, ypred).ravel()
    #     cf= [[tp, fp],[fn, tn]]
    #     sn.set(font_scale=1.4) #for label size
    #     print(sn.heatmap(cf, annot=True,annot_kws={'size': 20}, fmt='d'))
    #     print('Precision Score: {}'.format(precision_score(ytest, ypred)))
    #     print('Recall Score: {}'.format(recall_score(ytest, ypred)))
