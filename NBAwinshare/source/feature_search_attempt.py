import seasonalregressor
import data_wrangle
import clustering
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sb
from sklearn.metrics import mean_squared_error
from helper_functions import weighted_mean_multi_col_weight as wm2
from helper_functions import weighted_mean_one_col_weight as wm1
import pickle

advanced = data_wrangle.read_all_advanced('../data/advanced')
pergame  = data_wrangle.read_all_pergame('../data/per_game')
seasonal = data_wrangle.clean_and_join_seasonal_dataframe(advanced, pergame)
demographic = data_wrangle.read_demographic_data('../data/player_data.csv')
fullstats = data_wrangle.add_years_in_league(seasonal, demographic)

cols_to_train_from_correlation = ['WS',
 'OWS',
 'VORP',
 'DWS',
 'MP_total',
 'PS/G',
 'FG',
 'MP_pergame',
 'GS',
 'FT',
 '2P',
 'FTA',
 'FGA',
 '2PA',
 'DRB',
 'TRB',
 'BPM',
 'G',
 'TOV',
 'STL',
 'PER',
 'OBPM']

#create 10 random samples per feature_length
k = 20
num_features = [5, 10, 15]

srtemp = seasonalregressor.SeasonalRegressor(columns_to_train=cols_to_train_from_correlation)

with open('../train_test.pkl', 'rb') as f:
    trainnames, testnames = pickle.load(f)

fulltrain, fulltest = srtemp.create_train_test_split(fullstats, trainnames, testnames)
actuals = data_wrangle.get_actuals_for_years_5_thru_9(fullstats, testnames)

functions = ['default', wm1, wm2]
scores = {}

for num in num_features:
    cols_to_train_list = []
    for i in range(k):
        cols_to_traink = list(np.random.choice(cols_to_train_from_correlation, size = num, replace=False))
        cols_to_train_list.append(cols_to_traink)
    for function in functions:
        for cols_to_train in cols_to_train_list:
            print("Attempting: ",num, function, cols_to_train)
            sr = seasonalregressor.SeasonalRegressor(columns_to_train=cols_to_train, function=function)
            sr = sr.fit(fulltrain)
            pred_dict = sr.predict(fulltest)
            predictions = sr.unpack_prediction_dictionary(pred_dict)
            score = mean_squared_error(actuals, predictions)
            scores[str(function)+str(cols_to_train)] = score
            print(str(function)+str(cols_to_train), '|||', score)

minscore = min(scores.values())
for key, score in scores.items():
    if score == minscore:
        print("Min score is :", score)
        print('Min key is ', key)


#sr = sr.fit(fulltrain)
#
# pred_dict = sr.predict(fulltest)
#
# predictions = sr.unpack_prediction_dictionary(pred_dict)
#
# actuals = data_wrangle.get_actuals_for_years_5_thru_9(fullstats, testnames)
#
# score = mean_squared_error(actuals, predictions)
