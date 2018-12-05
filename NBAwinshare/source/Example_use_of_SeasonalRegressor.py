import seasonalregressor
import data_wrangle
import clustering
from helper_functions import weighted_mean_multi_col_weight as wm2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sb
from sklearn.metrics import mean_squared_error
import pickle

#Read in data, and create dataframes
advanced = data_wrangle.read_all_advanced('../data/advanced')
pergame  = data_wrangle.read_all_pergame('../data/per_game')
seasonal = data_wrangle.clean_and_join_seasonal_dataframe(advanced, pergame)
demographic = data_wrangle.read_demographic_data('../data/player_data.csv')
fullstats = data_wrangle.add_years_in_league(seasonal, demographic)

#These are the best columns from my feature search, given the interrelationship
#between FGA, 2P, and FG, this could probably be further streamlined.
cols_to_train = ['OBPM', 'FGA', 'DRB', '2P', 'FG']

#Insantiate a seasonal regressor object
sr = seasonalregressor.SeasonalRegressor(columns_to_train=cols_to_train, function=wm2)

with open('./train_test.pkl', 'rb') as f:
    trainnames, testnames = pickle.load(f)

fulltrain, fulltest = sr.create_train_test_split(fullstats, trainnames, testnames)

#fit the regressor to the train-set
sr = sr.fit(fulltrain)
#The sr predict method returns a dictionary of predictions (player -> seasons 5:9)
pred_dict = sr.predict(fulltest)
#The unpack_prediction_dictionary method converts the dictionary to a row of values
predictions = sr.unpack_prediction_dictionary(pred_dict)
#We want the actual wins from the tests data to score against the predictions
actuals = data_wrangle.get_actuals_for_years_5_thru_9(fullstats, testnames)
#Calculate the MSE
score = mean_squared_error(actuals, predictions)

print("MSE Score: ", score)
print("RMSE Score: ", score**.5)

#Create the dataframe, using the same columns we trained on
df = sr.create_avg_dataframe_for_first_four_seasons(fullstats,columns_to_use=cols_to_train)

#Let's get the closest 5 players, using the same features as our random forest
closest = clustering.get_x_nearest_players(df, x=5)
for player, closeguys in closest.items():
    print("Player: ", player, ":", closeguys)
