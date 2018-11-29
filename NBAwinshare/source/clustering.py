import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from scipy.spatial.distance import cdist, pdist, euclidean, squareform

from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn import metrics


def add_cluster_classifier(df):
    newdf = df.copy()
    #take data out of dataframe
    X = df.values
    #standardize the data before giving it to the PCA.
    X = scale(X)
    #transform data into the 14 PCA component-space (picked because it gives 95% of the info)
    reduced_data = PCA(n_components=14).fit_transform(X)
    #Fit the kmeans with 10 clusters
    kmeans = KMeans(n_clusters=10, random_state=42).fit(reduced_data)
    #add the predicted label
    newdf['kmeans_label'] = kmeans.labels_
    playergroups = {}
    for i in range(10):
        playergroups[i] = set(newdf[newdf['kmeans_label']==i].index)

    return newdf, playergroups, kmeans

def make_dendrogram(dataframe, linkage_method, metric, color_threshold=None, fontsize=12., savefile=None):
    '''
    This function creates and plots the dendrogram created by hierarchical clustering.

    INPUTS: Pandas Dataframe, string, string, int, fontsize (float), savefile (string)

    OUTPUTS: None
    '''
    distxy = squareform(pdist(dataframe.values, metric=metric))
    Z = linkage(distxy, linkage_method)
    plt.figure(figsize=(54, 20))
    plt.title('NBA Hierarchical Clustering Dendrogram - Using ' + linkage_method.capitalize() + ' Linkage')
    plt.xlabel('Players')
    plt.ylabel('distance - (' + metric + ')')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=fontsize,  # font size for the x axis labels
        labels = dataframe.index,
        color_threshold = color_threshold
    )
    if savefile:
        print("Attempting to save file:",savefile)
        plt.savefig(savefile,bbox_inches='tight')
    #plt.show()

def get_x_nearest_players(df, x=5):
    '''
    Use KNN to get the most similar players
    Inputs:
        df -needs to be a dataframe with one-row per player data, e.g., from:
            df, _, _ = sr.create_train_and_predict_X_and_y_of_first_four_seasons(fullstats, 5)

        x -will provide the x-closest players

    Returns: Dictionary with player names as keys, value of x mos
    '''
    #take data out of dataframe
    X = df.values
    #standardize the data before KNN.
    X = scale(X)
    #Increment x + 1, because the distances will return each item (0 distance away)
    n = x + 1
    #Fit the nearest neighbor
    nbrs = NearestNeighbors(n_neighbors=n, algorithm='ball_tree').fit(X)
    #Get the distances and corresponding indices -- could have used CDIST as well
    distances, indices = nbrs.kneighbors(X)

    most_similar_players = {}
    #For every player, get the x most similar
    for i,player in enumerate(df.index.values):
        #we want to slice by 1: because the closest index will be with itself
        most_similar_players[player] = list(df.index[indices[i][1:]])

    return most_similar_players
