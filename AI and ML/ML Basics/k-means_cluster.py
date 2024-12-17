#Unsupervised learning algorithm 1

from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.datasets import load_digits

digits = load_digits()
data = scale(digits.data)

"""
KMeans parameters:
Number of clusters, 
Starting points of the centroids
Number of initializations of the centroids
"""
model = KMeans(n_clusters=10, init='random', n_init=10)
model.fit(data)