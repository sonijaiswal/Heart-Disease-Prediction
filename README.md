# Installation

-   1 - clone repo
-   2 - create a virtual environment and activate
-   -   pip install virtualenv
-   -   virtualenv envname
-   -   envname\scripts\activate
-   3 - cd into project
-   4 - pip install -r requirements.txt
-   5 - python manage.py runserver

Comparative Analysis of Algorithms for Heart Disease Prediction

Overview
This project develops an end-to-end machine learning solution for the prediction of the presence or absence of heart disease based on clinical data. This project is based on best practices that are widely used in biomedical data analysis.
The system is developed as a decision-support system and shows how machine learning can be used to help with early disease risk prediction based on medical attributes.

Dataset
Source: UCI Machine Learning Repository – Cleveland Heart Disease Dataset
Instances: 303 patient records
Features: 13 clinical attributes including age, chest pain type, resting blood pressure, cholesterol level, ECG results, maximum heart rate, exercise-induced angina, and others
Target: Binary classification
1 → Presence of heart disease
0 → Absence of heart disease

Preprocessing & Pipeline Design

The dataset represents a typical real-world biomedical dataset with limited samples, mixed feature types, and clinically meaningful class imbalance considerations.
A modular and reproducible supervised learning pipeline was developed, which included the following components:
Data loading and validation
Missing data handling
Correlation-based feature analysis
Feature standardization (scaling)
Reproducible train-test split (80/20 and 75/25 splits)
The above-mentioned pipeline design is based on principles of clarity, reproducibility, and modularity, which are followed in large-scale biomedical data processing.
Models Evaluated


The following machine learning models were implemented and evaluated under the same experimental setup:

Logistic Regression (baseline)
Support Vector Machine (SVM)
K-Nearest Neighbors (KNN)
Random Forest
This comparative setup enables systematic analysis of linear vs. non-linear models on structured clinical data.

Evaluation Strategy

Model performance was evaluated using multiple metrics to ensure robust assessment:

Accuracy
Precision
Recall
F1-score
Confusion matrices

Special attention was given to precision–recall trade-offs, particularly minimizing false negatives, which is critical in medical and biomedical decision-making contexts where missed diagnoses can have serious consequences.

Results

Best-performing model: Random Forest

Performance: ~90% accuracy with strong stability across evaluation splits

Random Forest demonstrated superior performance due to its ability to capture non-linear interactions among clinical features, which are common in biomedical datasets.

Detailed confusion matrices and metric summaries are included to support transparent evaluation.

Deployment

To demonstrate translation from offline analysis to practical use, the trained model was deployed as a web-based application:

Backend: Django

Database: SQLite

This deployment showcases how ML models can be integrated into operational clinical decision-support systems, bridging the gap between research and real-world application.

Tools & Technologies

Python

scikit-learn

NumPy, Pandas

Matplotlib / Seaborn

Django

SQLite

Jupyter Notebook

Author

Soni Jaiswal
Machine Learning | Data Analytics 
