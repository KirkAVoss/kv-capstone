import data_wrangle

advanced = data_wrangle.read_all_advanced('../data/advanced')
pergame  = data_wrangle.read_all_pergame('../data/per_game')
seasonal = data_wrangle.clean_and_join_seasonal_dataframe(advanced, pergame)
demographic = data_wrangle.read_demographic_data('../data/player_data.csv')

print(seasonal.head())
print(demographic.head())
