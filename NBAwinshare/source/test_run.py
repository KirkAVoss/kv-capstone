import data_wrangle

advanced = data_wrangle.read_all_advanced('../data/advanced')
pergame  = data_wrangle.read_all_pergame('../data/per_game')
seasonal = data_wrangle.clean_and_join_seasonal_dataframe(advanced, pergame)
demographic = data_wrangle.read_demographic_data('../data/player_data.csv')
newseasonal = data_wrangle.add_years_in_league(seasonal,demographic)
print(newseasonal.head())
