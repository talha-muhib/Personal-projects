#Supervised learning algorithm 4

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC #Support Vector Classifier
from sklearn.neighbors import KNeighborsClassifier #Using this to compare accuracy with SVM

#Building off the SVM code, now we import the decision tree and random forest classifiers 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

data = load_breast_cancer()
print(data.feature_names) #Features of tumors
print(data.target_names) #Target is malignant or benign tumor

X = data.data
Y = data.target

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

#Kernel is linear and soft margin = 3
clf = SVC(kernel="linear", C=3)
clf.fit(x_train, y_train) #train the model using training data

clf2 = KNeighborsClassifier(n_neighbors=3)
clf2.fit(x_train, y_train) #train the model using training data

clf3 = DecisionTreeClassifier()
clf3.fit(x_train, y_train) #train the model using training data

clf4 = RandomForestClassifier()
clf4.fit(x_train, y_train) #train the model using training data

#test how well the model performs
print(f'SVC: {clf.score(x_test, y_test)}')
print(f'KNN: {clf2.score(x_test, y_test)}')
print(f'DTC: {clf3.score(x_test, y_test)}')
print(f'RFC: {clf4.score(x_test, y_test)}')