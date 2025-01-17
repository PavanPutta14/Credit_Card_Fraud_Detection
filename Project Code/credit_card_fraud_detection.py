# -*- coding: utf-8 -*-
"""Credit Card Fraud Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FvzpBFcaZbFwplhBY6zTXZnwre3O1JkD

# Credit Card Fraud Detection

**Importing Dependencies**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import SMOTE

"""**Loading dataset**"""

data = pd.read_csv('creditcard.csv')

"""**Data Analysis**"""

print("\nHead of the dataset:")
print(data.head())

print("\nTail of the dataset:")
print(data.tail())

print("\nDataset Description:")
print(data.describe())

print("\nDataset Shape:", data.shape)

print("\nDataset Information:", data.info())

data.describe()

print("\nNull values in the dataset:")
print(data.isnull().sum())

"""**Visualization**"""

# Visualization of  bar plot
class_counts = data['Class'].value_counts()
plt.bar(class_counts.index, class_counts.values, color=['blue', 'red'])
plt.xticks([0, 1], ['Normal', 'Fraud'])
plt.title('Class Distribution in Raw Data')
plt.xlabel('Class')
plt.ylabel('Frequency')
plt.show()

# Heatmap to visualize correlations
plt.figure(figsize=(15, 10))
sns.heatmap(data.corr(), cmap='coolwarm', annot=False)
plt.title('Correlation Heatmap of Raw Data')
plt.show()

sc = StandardScaler()
data['Amount'] = sc.fit_transform(pd.DataFrame(data['Amount']))

data = data.drop(['Time'], axis=1)
data = data.drop_duplicates()
print("\nDataset Shape after cleaning:", data.shape)
print(data['Class'].value_counts())

print("\nDataset Shape after cleaning:", data.shape)
print(data['Class'].value_counts())

# Scatter plot of cleaned data
plt.scatter(data.index, data['Amount'], alpha=0.5, c=data['Class'], cmap='coolwarm')
plt.title('Scatter Plot of Transaction Amounts (Cleaned Data)')
plt.xlabel('Index')
plt.ylabel('Standardized Amount')
plt.show()

X = data.drop('Class', axis = 1)
y=data['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

classifiers = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree Classifier": DecisionTreeClassifier()
}

# Evaluate classifiers on the raw data
print("\nEvaluation on Raw Data:")
raw_scores = []
for name, clf in classifiers.items():
    print(f"\n========== {name} ===========")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    raw_scores.append([name, acc, prec, rec, f1])
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1 Score: {f1:.4f}")

"""**Under-Sampling**"""

normal = data[data['Class'] == 0]
fraud = data[data['Class'] == 1]

normal_sample = normal.sample(n=fraud.shape[0])
new_data = pd.concat([normal_sample, fraud], ignore_index=True)

plt.figure(figsize=(12, 6))
plt.scatter(normal.index, normal['Amount'], alpha=0.5, label='Normal Transactions', color='blue')
plt.scatter(fraud.index, fraud['Amount'], alpha=0.5, label='Fraudulent Transactions', color='red')
plt.title('Scatter Plot of Normal vs Fraudulent Transactions')
plt.xlabel('Transaction Index')
plt.ylabel('Transaction Amount')
plt.legend()
plt.show()

# Split the balanced dataset
X = new_data.drop('Class', axis=1)
y = new_data['Class']

new_data.head()

new_data.tail()

new_data.describe()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Evaluate classifiers on the undersampled data
print("\nEvaluation on Undersampled Data:")
undersample_scores = []
for name, clf in classifiers.items():
    print(f"\n========== {name} (Undersampling) ===========")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    undersample_scores.append([name, acc, prec, rec, f1])
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1 Score: {f1:.4f}")

"""**Over-Sampling**"""

# Oversampling using SMOTE
X_res, y_res = SMOTE().fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)

# Evaluate classifiers on the oversampled data
print("\nEvaluation on Oversampled Data:")
oversample_scores = []
for name, clf in classifiers.items():
    print(f"\n========== {name} (Oversampling) ===========")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    oversample_scores.append([name, acc, prec, rec, f1])
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1 Score: {f1:.4f}")

"""**Conclusion***"""

def create_summary_table(scores, title):
    summary_table = pd.DataFrame(scores, columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"])
    summary_table.set_index("Model", inplace=True)
    print(f"\n{title}:")
    print(summary_table)

create_summary_table(raw_scores, "Summary Table for Raw Data")
create_summary_table(undersample_scores, "Summary Table for Undersampled Data")
create_summary_table(oversample_scores, "Summary Table for Oversampled Data")