# -*- coding: utf-8 -*-
"""Diabetes_Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aSVDxE0UFyKeK970Udc6j9a31egTxUOo
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

from mlxtend.plotting import plot_decision_regions
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')
# %matplotlib inline

from google.colab import drive
drive.mount('/content/drive')

file_path = '/content/drive/My Drive/Data/diabetes.csv'

data = pd.read_csv(file_path)
print(data.head())
data.dtypes

data_copy = data.copy(deep=True)
data_copy[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']] = data_copy[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']].replace(0, np.NaN)

print(data_copy.isnull().sum())

p = data.hist(figsize=(20, 20))

data_copy['Glucose'].fillna(data_copy['Glucose'].mean(), inplace=True)
data_copy['BloodPressure'].fillna(data_copy['BloodPressure'].mean(), inplace=True)
data_copy['SkinThickness'].fillna(data_copy['SkinThickness'].median(), inplace=True)
data_copy['Insulin'].fillna(data_copy['Insulin'].median(), inplace=True)
data_copy['BMI'].fillna(data_copy['BMI'].median(), inplace=True)

p = data_copy.hist(figsize=(20, 20))

color_wheel = {0: "blue", 1: "orange"}
colors = data["Outcome"].map(lambda x: color_wheel.get(x + 1))
print(data.Outcome.value_counts())
p = data.Outcome.value_counts().plot(kind="bar", color=[color_wheel[val] for val in data["Outcome"]])

plt.subplot(121)
sns.distplot(data['Insulin'])
plt.subplot(122)
data['Insulin'].plot.box(figsize=(16, 5))
plt.show()

plt.subplot(121)
sns.distplot(data['Age'])
plt.subplot(122)
data['Age'].plot.box(figsize=(16, 5))
plt.show()

plt.subplot(121)
sns.distplot(data['BMI'])
plt.subplot(122)
data['BMI'].plot.box(figsize=(16, 5))
plt.show()

plt.subplot(121)
sns.distplot(data['Pregnancies'])
plt.subplot(122)
data['Pregnancies'].plot.box(figsize=(16, 5))
plt.show()

plt.subplot(121)
sns.distplot(data['Glucose'])
plt.subplot(122)
data['Glucose'].plot.box(figsize=(16, 5))
plt.show()

plt.subplot(121)
sns.distplot(data['BloodPressure'])
plt.subplot(122)
data['BloodPressure'].plot.box(figsize=(16, 5))
plt.show()

plt.subplot(121)
sns.distplot(data['SkinThickness'])
plt.subplot(122)
data['SkinThickness'].plot.box(figsize=(16, 5))
plt.show()

plt.subplot(121)
sns.distplot(data['DiabetesPedigreeFunction'])
plt.subplot(122)
data['DiabetesPedigreeFunction'].plot.box(figsize=(16, 5))
plt.show()

plt.figure(figsize=(12, 10))
p = sns.heatmap(data.corr(), annot=True, cmap='RdYlGn')

data_copy.head()

from sklearn.preprocessing import StandardScaler

sc_X = StandardScaler()
X = pd.DataFrame(sc_X.fit_transform(data_copy.drop(['Outcome'], axis=1)),

columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'])

X.head()

y = data_copy.Outcome
y.head()

X = data.drop('Outcome', axis=1)
y = data['Outcome']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier(n_estimators=400)
rfc.fit(X_train, y_train)
rfc_train = rfc.predict(X_train)

from sklearn import metrics
print("Training Accuracy =", format(metrics.accuracy_score(y_train, rfc_train)))

n_estimators_values = [100, 150, 200, 400]
max_depth_values = [None, 10, 20]
min_samples_split_values = [2, 5]
min_samples_leaf_values = [1, 2, 4]

results = []

for n_estimators in n_estimators_values:
    for max_depth in max_depth_values:
        for min_samples_split in min_samples_split_values:
            for min_samples_leaf in min_samples_leaf_values:
                rfc = RandomForestClassifier(n_estimators=n_estimators,
                                             max_depth=max_depth,
                                             min_samples_split=min_samples_split,
                                             min_samples_leaf=min_samples_leaf,
                                             random_state=42)


                rfc.fit(X_train, y_train)

                y_pred = rfc.predict(X_test)
                accuracy = metrics.accuracy_score(y_test, y_pred)

                results.append({
                    'n_estimators': n_estimators,
                    'max_depth': max_depth,
                    'min_samples_split': min_samples_split,
                    'min_samples_leaf': min_samples_leaf,
                    'accuracy': accuracy
                })

results_df = pd.DataFrame(results)

print(results_df.sort_values(by='accuracy', ascending=False).head())

mean_accuracy = results_df.groupby('n_estimators')['accuracy'].mean()

plt.figure(figsize=(10, 6))
plt.plot(mean_accuracy.index, mean_accuracy.values, marker='o', linestyle='-', label='Mean Accuracy')
plt.title('Comparison of Random Forest Performance for Different n_estimators')
plt.xlabel('Number of Estimators (Trees)')
plt.ylabel('Mean Accuracy on Test Set')
plt.legend()
plt.grid(True)
plt.show()

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier(n_estimators=100,max_depth=20 , min_samples_split=5, min_samples_leaf=2)
rfc.fit(X_train, y_train)
rfc_train = rfc.predict(X_train)

print("Training Accuracy =", format(metrics.accuracy_score(y_train, rfc_train)))

predictions = rfc.predict(X_test)
print("Test Accuracy =", format(metrics.accuracy_score(y_test, predictions)))

from sklearn.metrics import classification_report, confusion_matrix

print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))

from sklearn.tree import DecisionTreeClassifier

dtree = DecisionTreeClassifier()
dtree.fit(X_train, y_train)
predictions = dtree.predict(X_test)
print("Test Accuracy =", format(metrics.accuracy_score(y_test, predictions)))

from sklearn.metrics import classification_report, confusion_matrix

print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))

from sklearn.svm import SVC

svc_model = SVC()
svc_model.fit(X_train, y_train)
svc_pred = svc_model.predict(X_test)
print("Test Accuracy =", format(metrics.accuracy_score(y_test, svc_pred)))

from sklearn.metrics import classification_report, confusion_matrix

print(confusion_matrix(y_test, svc_pred))
print(classification_report(y_test, svc_pred))

rfc.feature_importances_
pd.Series(rfc.feature_importances_, index=X.columns).plot(kind='barh')

print(data.head())
print(data.tail())
print(rfc.predict([[0, 95, 40, 29, 150, 37.1, 1.2, 33]]))
print(rfc.predict([[10, 101, 76, 48, 180, 32.9, 0.171, 63]]))