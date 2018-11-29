from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from scipy.spatial.distance import cdist, pdist, euclidean
from sklearn.cluster import KMeans
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

    return newdf, playergroups

def make_dendrogram(dataframe, linkage_method, metric, color_threshold=None, fontsize=12., savefile=None):
    '''
    This function creates and plots the dendrogram created by hierarchical clustering.

    INPUTS: Pandas Dataframe, string, string, int, fontsize (float), savefile (string)

    OUTPUTS: None
    '''
    distxy = squareform(pdist(dataframe.values, metric=metric))
    Z = linkage(distxy, linkage_method)
    plt.figure(figsize=(54, 20))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Players')
    plt.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=fontsize,  # font size for the x axis labels
        labels = dataframe.index,
        color_threshold = color_threshold
    )
    if savefile:
        plt.savefig(savefile,bbox_inches='tight',dpi=1000)
    plt.show()
