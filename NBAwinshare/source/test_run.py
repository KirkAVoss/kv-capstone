import seasonalregressor
import data_wrangle
import clustering
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sb
from sklearn.metrics import mean_squared_error
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
 'DRB']

sr = seasonalregressor.SeasonalRegressor(columns_to_train=cols_to_train_from_correlation)

with open('../train_test.pkl', 'rb') as f:
    trainnames, testnames = pickle.load(f)

fulltrain, fulltest = sr.create_train_test_split(fullstats, trainnames, testnames)

#sr = sr.fit(fulltrain)
#
# pred_dict = sr.predict(fulltest)
#
# predictions = sr.unpack_prediction_dictionary(pred_dict)
#
# actuals = data_wrangle.get_actuals_for_years_5_thru_9(fullstats, testnames)
#
# score = mean_squared_error(actuals, predictions)

df, y, _ = sr.create_train_and_predict_X_and_y_of_first_four_seasons(fullstats,5)

# linktype = 'complete'
# metric = 'cosine'
# clustering.make_dendrogram(df.iloc[:,:-2], linktype, metric, color_threshold=None, fontsize=6, savefile='complete_cosine.png')
# linktype = 'average'
# metric = 'euclid'
# clustering.make_dendrogram(df.iloc[:,:-2], linktype, metric, color_threshold=None, fontsize=6, savefile='LBJ_dendro_avg_euc.png')

closest = clustering.get_x_nearest_players(df, x=5)
for player, closeguys in closest.items():
    print("Player: ", player, ":", closeguys)
