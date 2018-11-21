import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
#from sklearn.linear_model import LogisticRegression
#from sklearn.metrics import precision_score, recall_score, confusion_matrix
#import seaborn as sn
#from scipy import stats
#import pickle

class SeasonalRegressor():


    def __init__(self, regressor_type='RF'):
        '''
        Instantiates a model
        Input: regressor_type -- type of regressor used in the prediction algo, defaults to random forest (only option operative)
        '''
        self.years_to_predict = [5, 6, 7, 8, 9]
        self.regressor_dict = {}
        for year in self.years_to_predict:
            self.regressor_dict[year] = RandomForestRegressor(n_jobs=-1)


    def fit(self, X, y):
        '''
        Fit X and Y to the regressor'
        Returns self
        '''

        #need to fit the regressor for each year, which means I either need to break up the train data in acceptable year windows, or handle that here
        #Also need to make sure test / train split has various
        #Random Forest Fit


        return self


    def predict(self, X):
        '''
        Predict win-shares for X.
        Returns y (predictions)

        '''
        #run the model for each classifier
        pass

    def create_train_and_predict_X_and_y_from_seasons_4_and_5(self, df_season_4, \
        df_season_5, columns_to_train, col_to_predict='WS'):
        '''
        This function takes the seasonal information from year 4 (all players and all
        season-4's) and creates an "X" dataframe, and a "y" dataframe for use with training
        Inputs: df_season_4 -- a dataframe filtered to only have year-4 data
                    should NOT have player name as index, it should be in 'Player'
                ***NOTE*** Shouldn't have previous year stats
                df_season_5 -- a dataframe filtered to only have year-5 data
                    should NOT have player name as index, it should be in 'Player'
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
        trainidx = set(df_season4_reduced.index.values)
        predictidx = set(to_predict_dataframe.index.values)
        if not trainidx^predictidx:
            print("Something went wrong with the indices (1):", trainidx^predictidx)
            return None
        elif not (d4_season4_reduced.index.equals(to_predict_dataframe.index):
            print("Something we wrong with indices (2)")

        #return the dataframes
        return df_season_4_reduced, to_predict_dataframe

    #this probably doesn't make sense, but don't want to delete it yet
    def confusion_matrix(self, ytest, ypred):
        '''Function prints the precision score, recall score, and plots the confusion matrix.'''
        tn, fp, fn, tp = confusion_matrix(ytest, ypred).ravel()
        cf= [[tp, fp],[fn, tn]]
        sn.set(font_scale=1.4) #for label size
        print(sn.heatmap(cf, annot=True,annot_kws={'size': 20}, fmt='d'))
        print('Precision Score: {}'.format(precision_score(ytest, ypred)))
        print('Recall Score: {}'.format(recall_score(ytest, ypred)))
