from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

from bienes_inmuebles.preprocesar.csv_plot import CSVPlot

class NO_Supervisado(CSVPlot):
    def __init__(self, df):
        self.df = df

    def pca(self, n=2):
        pca = PCA(n_components=n)
        pca.fit(self.df)
        return pca.transform(self.df)

    def tsne(self,n=2):
        X_embedded = TSNE(n_components=n).fit_transform(self.df)
        return X_embedded

    def unam(self):
        pass

    """Clustering"""
    def kmeans_clustering(self,n_cluster=2, random_state=0):
        kmeans = KMeans(n_clusters=n_cluster, random_state=random_state).fit(self.df)
        labels = kmeans.labels_
        #kmeans.predict([[0, 0], [12, 3]])
        centroide = kmeans.cluster_centers_
        return kmeans, labels, centroide


if __name__ == "__main__":
    no_supervisado = NO_Supervisado("../../data/csv_barcelona.csv")