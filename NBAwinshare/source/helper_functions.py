
def weighted_mean(group, avg_name, weight_name):
    '''
    Computes a weighted mean -- for calling with pandas groupby.agg functionality
    '''
    d = group[avg_name]
    w = group[weight_name]

    try:
        return (d*w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()
