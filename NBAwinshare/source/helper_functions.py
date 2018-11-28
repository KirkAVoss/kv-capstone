import pandas as pd
import numpy as np

def weighted_mean_one_col_weight(df, cols, weights='Seasons_number'):
    '''
    Computes a weighted mean -- for calling with pandas groupby.agg functionality
    With the weights being in one column
    '''
    return pd.Series(np.average(df[cols], weights=df[weights], axis=0), cols)

    '''
    d = group[avg_name]
    w = group[weight_name]

    try:
        return (d*w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()
    '''
