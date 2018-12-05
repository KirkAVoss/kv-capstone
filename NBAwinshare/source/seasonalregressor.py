import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import data_wrangle

import os, sys
sys.path.insert(0, '/Users/kv/workspace/kv-capstone/NBAwinshare/source')

#from helper_functions import weighted_mean_one_col_weight as wm
from helper_functions import weighted_mean_multi_col_weight as wm2

class SeasonalRegressor():
    '''
    Creates a Seasonal Regressor object
    '''


    def __init__(self, regressor_type='RF', columns_to_train='all', function='default'):
        '''
        Instantiates a model
        Input: regressor_type -- type of regressor used in the prediction algo, defaults to random forest (only option operative)
                columnes_to_train -- the columns used to train the model
                function -- the function used to smooth data in the fit and predict methods.  The 'default' option is just the
                pandas.groupby.mean() function
        '''

        self.meanfunc = function

        #these are the years to predict
        self.years_to_predict = [5, 6, 7, 8, 9]
        self.regressor_dict = {}
        self.columns_to_train = columns_to_train
        self.column_names = None
        self.players_with_fulldata = {}
        #For every year we want to predict, create a regressor for that year, and store it in the dictionary.
        for year in self.years_to_predict:
            if regressor_type == 'RF':
                #Need to figure out how to pass arguments to this thing for grid search purposes
                self.regressor_dict[year] = RandomForestRegressor(n_jobs = -1, oob_score = True, n_estimators = 100)
            else:
                print("Don't know what to do with this, sorry, chief.")

    def fit(self, df_fullstats, col_to_predict='WS'):
        '''
        Fits the df_fullstats data to the regressor dictionary objects

        Inputs: df_fullstats -- a dataframe that has all data player data in it .
                    Should be result of data_wrangle.add_years_in_league
                    Should NOT have player name as index, it should be in a 'Player'

                columns_to_train -- a list of columns, from within fullstats to train on.  Defaults to 'all'

                col_to_predict -- The column we are trying to predict from df_fullstats['Season_number']==(last_train_season +  1): 'WS' by default


        Returns self
        '''
        #Fit every year in years to predict
        for year in self.years_to_predict:
            #Create an X and y for each year.  Note the year-1 used as the argument on last_train_season
            X, y, fullplayers = self.create_train_and_predict_X_and_y_of_first_four_seasons(df_fullstats, \
            year, col_to_predict = col_to_predict, columns_to_train = self.columns_to_train)
            self.players_with_fulldata[year] = fullplayers

            #print("Fitting for year:", year)
            #Fit the regressor at each year
            self.column_names = list(X.columns)
            self.regressor_dict[year] = self.regressor_dict[year].fit(X,y)

        return self


    #This was a method when I was contemplating extrapolating out actual data from year 1-4 to use for 5-9
    #I'm leaving it in case I want to come back to it later.
    def fit_bad(self, df_fullstats, df_demographic, col_to_predict='WS'):
        '''
        Fits the df_fullstats data to the regressor dictionary.  Shouldn't use this method, it isn't based on just years 1-4

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
            #print("Fitting for year:", year)
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
        #This will break if columns_to_train is 'all'
        if self.meanfunc == 'default':
            playerframe = df_fouryearstats.groupby('Player').mean().sort_index()
        else:
            playerframe = df_fouryearstats.groupby('Player').apply(self.meanfunc,self.columns_to_train).sort_index()
        players = set(playerframe.index)

        #Doing nested for-loop so that I can easily keep predictions together
        for year in self.years_to_predict:
            #For each player
            for player in players:
                #print("Predicting year:", year, "for player: ",player)
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


    def get_players_first_x_full_years(self, df_fullstats, season=4):
        '''
        Returns the first x years foreach player, if there is full data for that player

        Inputs --   df_fullstats - a dataframe that has all data player data in it .
                    Should be result of data_wrangle.add_years_in_league
                    Should NOT have player name as index, it should be in a 'Player'
                    seasons that you need the full data
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
        #print("Number of players: ", count, " with full season data for seasons:", seasons_needed)

        #Get the player-rows that we want to predict.
        df_only_full_players = df_fullstats[(df_fullstats['Player'].isin(players_with_fulldata)) &  (df_fullstats['Seasons_number'] <= season)]

        return df_only_full_players

    def get_single_player_first_x_full_years(self, df_fullstats, playername, season=4):
        '''
        Returns the first "season"s worth of the player stats, read in via data_wrangle
        Can be used with the predict method--even if there aren't four full seasons
        Inputs: df_fullstats -dataframe of the full player stats for many players
                playername -string- player name to pull

        '''
        return df_fullstats[(df_fullstats['Player']==playername) & (df_fullstats['Seasons_number'] <= season)]

    #Could probably move this function out of the class, or at least make static
    def plot_player_arc(self, df_fullstats, playername, prediction_dict):
        '''
        Plots the player arc based on predictions
        Inputs: df_fullstats - dataframe containing the full stats
                playername - string - player name for the predictions
                prediction_dict - dictionary of predicted values (Win Shares), key is playername
        '''
        x,y = data_wrangle.get_actuals_for_first_x_years(df_fullstats, playername)
        self._plot_player_arc_helper(playername,prediction_dict[playername], actuals = y, actualseasons=x)

    def _plot_player_arc_helper(self, playername, predictions, predseasons= [5,6,7,8,9], actuals=None, actualseasons=None):
        '''
        Helper Function that plots the player arc based on predictions
        Inputs: playername - string - player name for the predictions
                predictions - array of predicted values (Win Shares)
                seasons - the seasons (x-axis)
                actuals - array of actual values to plot against the predicted values
        '''
        plt.style.use('fivethirtyeight')
        plt.title('Win-Share Predictions for ' + playername + '')
        plt.ylabel('Win Shares')
        plt.xlabel('Seasons')

        #plot the predicted seasons
        plt.plot(predseasons, predictions, '.-')
        if actuals.any():
            plt.plot(actualseasons, actuals, '.-')

        plt.xticks(range(1,10))

        plt.legend(['Predictions', 'Actuals'], loc='best')
        plt.show()
        pass

    def plot_feature_importances(self, year_to_plot):
        '''
        Plots the feature importances for a specific regressor

        Input -- year_to_plot - integer - the regressor predictor year to use
        '''

        importances = self.regressor_dict[year_to_plot].feature_importances_
        indices = np.argsort(importances)[::-1]
        # Print the feature ranking
        print("Feature ranking:")

        sortedcolnames = [self.column_names[idx] for idx in indices]

        for f in range(len(self.column_names)):
            print("%d. feature %d | %s | (%f)" % (f + 1, indices[f], self.column_names[indices[f]], importances[indices[f]]))

        # Plot the feature importances of the forest
        plt.figure(figsize=(20,10))
        plt.title("Feature importances")
        plt.bar(range(len(self.column_names)), importances[indices],
               color="r", align="center")
        plt.xticks(range(len(self.column_names)), sortedcolnames, rotation='vertical')
        plt.xlim([-1, len(self.column_names)])
        plt.show()
        pass


    def create_train_and_predict_X_and_y_of_first_four_seasons(self, df_fullstats, \
    year_to_predict, columns_to_train='all', col_to_predict='WS'):
        '''
        This function takes the seasonal information from years 1-4 and creates an "X" dataframe,
        and a "y" dataframe for use with training.  The "y" dataframe will be the predicted year stat
        Inputs: df_fullstats -- a dataframe that has all data player data in it.
                    Should be result of data_wrangle.add_years_in_league
                    Should NOT have player name as index, that info should be in a 'Player'

                year_to_predict - should be the year to predict a specific stats.  Should be in interval [5,9]

                columns_to_train -- a list of columns, from within fullstats to train on.  Defaults to all

                col_to_predict -- The column we are trying to predict from df_fullstats['Season_number']==(year_to_predict): 'WS' by default

        Returns X - dataframe reduced to columns_to_train that has corresponding values in Y
                y - dataframe containing the col_to_predict, where previous year players are in X
                players - set of player names that have full data for years 1-last_train_season+1
        '''

        #Currently, functionality requires data for years 1-4, plus the predict year.
        seasons_needed = set(range(1,4+1)) #range isn't inclusive by default on the ride side of the interval
        seasons_only_for_train = set(range(1,4+1))
        season_to_predict = year_to_predict
        seasons_needed.add(season_to_predict)

        count = 0
        players_with_fulldata = set()

        #for every unique player in fullstats, let's figure out who we have data for in years: 1-4, and season_to_predict
        for player in df_fullstats['Player'].unique():
            #get the Season_numbers we have per player
            playerset = set(df_fullstats.loc[df_fullstats['Player']==player, 'Seasons_number'])
            #if the player has every year, append to the set of full players
            if seasons_needed.issubset(playerset):
                #print("Have full-year stats ",player)
                players_with_fulldata.add(player)
                count += 1
        #print("Number of players: ", count, " with full season data for seasons:", seasons_needed)

        #Get the player-rows that we want to train and predict upon.  This step could be combined with the next two below,
        #but I include for readability
        df_only_full_players = df_fullstats[(df_fullstats['Player'].isin(players_with_fulldata)) &  \
        ((df_fullstats['Seasons_number'] <= 4) | (df_fullstats['Seasons_number'] == season_to_predict))]

        #Just want the train set (Seasons 1-4)
        df_full_train = df_only_full_players[df_only_full_players['Seasons_number'] <=  4]

        #Get the to-predict set (season_to_predict)
        df_full_predict = df_only_full_players[df_only_full_players['Seasons_number'] ==  season_to_predict]

        #Here is where I want to apply a custom function, something more heavily weighted towards most recent
        #seasons.  Originally, I just used the built-in groupby-mean.  That doesn't capture trajectories very well.
        #And it certainly screws up if the predict set has something funky in it.  Like Al Horford playing 11 games in year 5
        if self.meanfunc == 'default':
            df_transformed_train = df_full_train.groupby('Player').mean().sort_index()
        else:
            df_transformed_train = df_full_train.groupby('Player').apply(self.meanfunc,self.columns_to_train).sort_index()

        #Re-index the predict frame
        df_reindexed_predict = df_full_predict.set_index('Player').sort_index()

        #Error checking, make sure indices are good
        if not df_transformed_train.index.equals(df_reindexed_predict.index):
            #print("Indices of train set and to-predict set MATCH")

            print("Indices of train set and to-predict DO NOT match:")
            print(df_transformed_train.index.difference(df_reindexed_predict.index))
            return (None, None, None)

        #filter the columns
        if columns_to_train == "all":
            #print("Using all columns")
            X = df_transformed_train
        else:
            #print("Using columns: ",columns_to_train)
            X = df_transformed_train[columns_to_train]

        #grab the column to predict as y
        y = df_reindexed_predict.pop(col_to_predict)

        return X, y, players_with_fulldata

    def create_avg_dataframe_for_first_four_seasons(self, df_fullstats, columns_to_use='all'):
        '''
        This function takes the seasonal information from years 1-4 and creates an "X" dataframe.
        We're not worried about predicting based on this frame, so we need not be concerned with
        players that are missing seasons
        Inputs: df_fullstats -- a dataframe that has all data player data in it.
                    Should be result of data_wrangle.add_years_in_league
                    Should NOT have player name as index, that info should be in a 'Player' field

                year_to_predict - should be the year to predict a specific stats.  Should be in interval [5,9]

                columns_to_use -- a list of columns, from within fullstats to filter.  Defaults to all.

                col_to_predict -- The column we are trying to predict from df_fullstats['Season_number']==(year_to_predict): 'WS' by default

        Returns X - dataframe reduced to columns_to_train that has corresponding values in Y
                y - dataframe containing the col_to_predict, where previous year players are in X
                players - set of player names that have full data for years 1-last_train_season+1
        '''

        #Grab the First four years
        df_four_years = df_fullstats[df_fullstats['Seasons_number'] <= 4]

        if self.meanfunc == 'default':
            df_transformed = df_four_years.groupby('Player').mean().sort_index()
        else:
            if columns_to_use == 'all':
                df_transformed = df_four_years.groupby('Player').apply(self.meanfunc,df_fullstats.columns).sort_index()
            else:
                df_transformed = df_four_years.groupby('Player').apply(self.meanfunc,columns_to_use).sort_index()

        #print(df_transformed.head().T)

        #filter the columns
        if columns_to_use == "all":
            X = df_transformed
        else:
            X = df_transformed[columns_to_use]

        return X

    def create_train_test_split(self, df_fullstats, trainplayers, testplayers):
        '''
        Create a train_test_split for df_fullstats DataFrame
        trainplayers - list of train players- read in from pkl object, list of players for training
        testplayers  - list of test players- read in from pkl object, list of players for testing--
                        limited to first four seasons to prevent from predicting on future data
        '''
        trainframe = df_fullstats[df_fullstats['Player'].isin(trainplayers)]
        testframe  = df_fullstats[(df_fullstats['Player'].isin(testplayers)) & \
        (df_fullstats['Seasons_number'] <= 4)]

        return trainframe, testframe

    def unpack_prediction_dictionary(self, prediction_dictionary):
        '''
        Unpacks the prediction dictionary (returned by SeasonalRegressor.predict())
        for use with MSE score
        '''

        predictions = []
        for player in sorted(prediction_dictionary.keys()):
            predictions += prediction_dictionary[player]

        return predictions





    # #this probably doesn't make sense, but don't want to delete it yet
    # def confusion_matrix(self, ytest, ypred):
    #     '''Function prints the precision score, recall score, and plots the confusion matrix.'''
    #     tn, fp, fn, tp = confusion_matrix(ytest, ypred).ravel()
    #     cf= [[tp, fp],[fn, tn]]
    #     sn.set(font_scale=1.4) #for label size
    #     print(sn.heatmap(cf, annot=True,annot_kws={'size': 20}, fmt='d'))
    #     print('Precision Score: {}'.format(precision_score(ytest, ypred)))
    #     print('Recall Score: {}'.format(recall_score(ytest, ypred)))
