import pandas as pd
import numpy as np

def weighted_mean_one_col_weight(df, cols, weights='Seasons_number'):
    '''
    Computes a weighted mean -- for calling with pandas groupby.agg functionality
    With the weights being in one column
    '''
    return pd.Series(np.average(df[cols], weights=df[weights], axis=0), cols)

def weighted_mean_multi_col_weight(df, cols, weights=['Seasons_number', 'G']):
    '''
    Computes a weighted mean -- for calling with pandas groupby.agg functionality
    With the weights derived from the seasons times the number of games played
    in that season
    '''
    new_weights = df[weights[0]] * df[weights[1]]

    return pd.Series(np.average(df[cols], weights=new_weights, axis=0), cols)
