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
heart_df = heart_df.rename(columns={'condition': 'target'})
print(heart_df.head())

# model building

# fixing our data in x and y. Here y contains target data and X contains rest all the features.
x = heart_df.drop(columns='target')
y = heart_df.target

# splitting our dataset into training and testing for this we will use train_test_split library.
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42)

# feature scaling
scaler = StandardScaler()
x_train_scaler = scaler.fit_transform(x_train)
x_test_scaler = scaler.fit_transform(x_test)

# LR_model= LogisticRegression()
# Knn_model= KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
# SVC_model= SVC()
# RF_model= RandomForestClassifier(n_estimators=20)
# DT_model= DecisionTreeClassifier()
model = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
model.fit(x_train_scaler, y_train)
y_pred = model.predict(x_test_scaler)
p = model.score(x_test_scaler, y_test)
print(p)

print('Classification Report\n', classification_report(y_test, y_pred))
print('Accuracy: {}%\n'.format(round((accuracy_score(y_test, y_pred)*100), 2)))

cm = confusion_matrix(y_test, y_pred)
print(cm)

# Creating a pickle file for the classifier
filename = 'svc_model.pkl'
pickle.dump(model, open(filename, 'wb'))
