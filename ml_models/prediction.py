# importing required libraries
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


# loading and reading the dataset

heart = pd.read_csv("heart.csv")

# creating a copy of dataset so that will not affect our original dataset.
heart_df = heart.copy()

# Renaming some of the columns
heart_df = heart_df.rename(columns={"condition": "target"})
print(heart_df.head())

# model building

# fixing our data in x and y. Here y contains target data and X contains rest all the features.
x = heart_df.drop(columns="target")
y = heart_df.target

# splitting our dataset into training and testing for this we will use train_test_split library.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

# feature scaling
scaler = StandardScaler()
x_train_scaler = scaler.fit_transform(x_train)
x_test_scaler = scaler.fit_transform(x_test)


# knn_model= KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2) 88.52%
# svc_model= SVC() 83.61%
# SVC(kernel='linear', max_iter=1000, C=10, probability=True) 83.61%


# rf_model= RandomForestClassifier(n_estimators=20) 91.8%

model = RandomForestClassifier(
    criterion="gini",
    max_depth=7,
    max_features="sqrt",
    min_samples_leaf=2,
    min_samples_split=4,
    n_estimators=180,
)

model.fit(x_train_scaler, y_train)
y_pred = model.predict(x_test_scaler)
p = model.score(x_test_scaler, y_test)
print(p)

print("Classification Report\n", classification_report(y_test, y_pred))
print("Accuracy: {}%\n".format(round((accuracy_score(y_test, y_pred) * 100), 2)))

cm = confusion_matrix(y_test, y_pred)
print(cm)

# Creating a pickle file for the classifier
# filename = "svc_model.pkl"
filename = "rf_model.pkl"
pickle.dump(model, open(filename, "wb"))
