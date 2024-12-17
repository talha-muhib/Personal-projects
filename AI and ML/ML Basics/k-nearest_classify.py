#Supervised learning algorithm 2

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

data = load_breast_cancer()
print(data.feature_names) #Features of tumors
print(data.target_names) #Target is malignant or benign tumor

#split into training and testing data (data.data is the features of the dataset)
x_train, x_test, y_train, y_test = train_test_split(np.array(data.data), np.array(data.target), test_size=0.2)

clf = KNeighborsClassifier(n_neighbors=3) #3 nearest neighbors
clf.fit(x_train, y_train) #train the model using training data
print(clf.score(x_test, y_test)) #test how well the model performs