# -*- coding: utf-8 -*-
"""Logistic Regression_mahdi_saieedi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-ulLNHE38mNLjjESwfbiQHozIEcv6lcn

### Full Name : Mahdi Saieedi
### Student Number : 401207254
___

## P1: Introduction (5 points)
The dataset comprises various independent variables serving as predictors for loan results and one dependent variable, "Loan_Status." The independent variables include Gender, Marital status, Dependents, and so on. Initially, we conduct data exploration to understand the dataset better. Then, we do some data preprocessing to ready the data for the regression model. Finally, we train a regression model to predict the outcome.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""The cell below will download the dataset."""

!gdown 1sG5yPXWK7a6wFlsVc2XCjNkwCxdcsstM

"""TODO: Load the dataset as a dataframe. Check for duplicate rows and if there are any, delete them. Display the first 10 rows. (5 points)"""

df = pd.read_csv('/content/Loan_Data.csv')
dup_rows = df[df.duplicated()]
print(dup_rows.index)
df.head(10)

df

"""## P2: Data Exploration (18 points)
In this section, we perform some data exploration to get a better understanding of the data.

TODO: Display the count of each unique value in the 'property_area' column. (3 points)
"""

area_counts = df['Property_Area'].value_counts()
print(area_counts)

"""TODO: Plot the correlation between different features. (use sns.heatmap) (3 points)"""

corr = df.corr()
sns.heatmap(corr, xticklabels=corr.columns,yticklabels=corr.columns,
            cmap='RdBu_r',annot=True,linewidth=0.5)

"""TODO: Plot a bar chart combining the 'Gender' and 'Loan_Status' columns (hint: use crosstab in pandas). Additionally, plot count plots for the 'Married' and 'Self_Employed' columns. (3 points)"""

ct = pd.crosstab(df.Gender, df.Loan_Status)
ct.plot(kind='bar', stacked=True, color=['red','blue'])

sns.countplot(x='Married', data=df)

sns.countplot(x='Self_Employed', data=df)

"""TODO: Plot a pie chart for the 'Education' column. (3 points)"""

edu_counts = df['Education'].value_counts()
labels = edu_counts.index
sizes = edu_counts.values
colors = ['green', 'red']
plt.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%')
plt.axis('equal')
plt.title('Education Counts')
plt.tight_layout()
plt.show()

"""TODO: Plot a box plot for the combination of 'Loan_Status' and 'ApplicantIncome' columns. (3 points)"""

plt.figure(figsize=(6, 6))
sns.boxplot(x='Loan_Status', y='ApplicantIncome', data=df)

"""TODO: Plot a histogram of the 'ApplicantIncome' column with 10 bins. (3 points)"""

plt.hist(df['ApplicantIncome'], bins=10)
plt.xlabel('Applicant Income')
plt.ylabel('Frequency')
plt.title('Histogram of Applicant Income')
plt.show()

"""## P3: Pre-processing (20 points)
In this section, we perform some pre-processing to make the data ready for the model.

TODO: Check for any null value. (2 point)
"""

df.isnull().values.any()

null_cols = df.isnull().any()
null_cols

sum_null_col = df.isnull().sum()
sum_null_col

nul_df = df[df.isnull().any(axis=1)]
nul_df

"""TODO: As you can observe, there are some null values. Given the significance of credit history for loan status prediction, we cannot impute null values for this specific column. Therefore, delete all rows containing null values in the 'credit history' column. For other columns, fill null entries with the mode for non-float/int columns and with the mean for float/int columns. (8 points)"""

df.dropna(subset=['Credit_History'], inplace=True)

df

for col in df.columns:
  if not pd.api.types.is_numeric_dtype(df[col]):
    df[col].fillna(df[col].mode()[0], inplace=True)
  else:
    df[col].fillna(df[col].mean(), inplace=True)

#check if there is any null value again in any columns
sum_null_col = df.isnull().sum()
sum_null_col

"""TODO: There are some columns that are entirely independent of our dependent variable, such as Loan_ID. Please drop this column. (2 points)"""

df.drop('Loan_ID', axis=1, inplace=True)
df

"""TODO: Separate the data into independent variables and the target variable. (1 point)"""

x = df[['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
        'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
        'Loan_Amount_Term', 'Credit_History', 'Property_Area']]
y = df[['Loan_Status']]

y

x

"""TODO: Use LabelEncoder to transform categorical variables into numeric variables. (3 points)"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
x['Encoded_Gender'] = le.fit_transform(x['Gender'])
x['Encoded_Married'] = le.fit_transform(x['Married'])
x['Encoded_Education	'] = le.fit_transform(x['Education'])
x['Encoded_Self_Employed'] = le.fit_transform(x['Self_Employed'])
x['Encoded_Property_Area'] = le.fit_transform(x['Property_Area'])
y['Encoded_Loan_Status'] = le.fit_transform(y)

x

y

x.drop(columns = ['Gender', 'Married', 'Education', 'Self_Employed',
                  'Property_Area'], axis=1, inplace=True)
y.drop('Loan_Status', axis=1, inplace=True)

x

y

"""TODO: Use StandardScaler for independant variables. (3 points)"""

type(x['Dependents'][610])

#we can not to this beacause there are several data points in Dependents columns
#labeled as +3 which are strings so we converts them to integer first
for index, row in x.iterrows():
  if x['Dependents'][index] == '3+':
    x['Dependents'][index] = float(3)
    print(index)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(x)
X_scaled = scaler.transform(x)

"""TODO: Divide data to train and test. (1 point)"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=1)

"""## P3: SKLearn Regression Model (10 points)

In this section, we perform logistic regression to predict the outcome.
Then we draw confusion matrix to see the accuracy of the model.

TODO: Train a logistic regression model using `sklearn` (6 points). Then use `sklearn`'s confusion matrix to check the result. (4 points)
"""

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(metrics.accuracy_score(y_test, y_pred))

# Calculate confusion matrix
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
print(cnf_matrix)

sns.heatmap(cnf_matrix, annot=True, fmt="d")
plt.title("Confusion matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

"""## P4: Custom Regression Model (32 points)

TODO: Imeplement the Logistic Regression model. Complete these methods: `loss`, `loss_derivative`, `predict` and for loop of fit function. (27 points)
"""

# class GDLogisticRegression:
#     def __init__(self, n_features, max_iter=50000, lr=0.0001, tol=1e-6, momentum=0.9):
#         self.N = n_features
#         self.beta = np.zeros((self.N+1,))
#         self.max_iter = max_iter
#         self.lr = lr
#         self.tol = tol
#         self.momentum = momentum

#     def loss(self, X, y):
#         z = np.dot(X, self.beta)
#         y_hat = 1 / (1 + np.exp(-z))
#         return -np.mean(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))

#     def loss_derivative(self, X, y):
#         z = np.dot(X, self.beta)
#         y_hat = 1 / (1 + np.exp(-z))
#         return (y_hat - y).T @ X

#     def predict(self, X_test, threshold=0.5):
#         z = np.dot(X_test, self.beta)
#         y_hat = 1 / (1 + np.exp(-z))
#         y_pred = np.where(y_hat >= threshold, 1, 0)
#         return y_pred

#     def fit(self, X_train, y_train):
#         X_train_new = np.concatenate((X_train, np.ones((X_train.shape[0], 1))), axis=1)
#         last_loss = 0
#         momentum = 0
#         for _ in range(self.max_iter):
#             loss = self.loss(X_train_new, y_train)
#             if abs(loss - last_loss) < self.tol:
#               break
#             last_loss = loss
#             gradients = self.loss_derivative(X_train_new, y_train)
#             momentum = self.momentum * momentum - self.lr * gradients
#             float_array = np.array([momentum])
#             self.beta += int(float_array)
#             return self

class GDLogisticRegression:
    def __init__(self, n_features, max_iter=50000, lr=0.0001, tol=1e-6, momentum=0.9):
        self.N = n_features + 1
        self.beta = np.zeros(self.N)
        self.max_iter = max_iter
        self.lr = lr
        self.tol = tol
        self.momentum = momentum

    def loss(self, X, y):
        predictions = self.sigmoid(X @ self.beta)
        loss = -np.mean(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
        return loss

    def loss_derivative(self, X, y):
        predictions = self.sigmoid(X @ self.beta)
        gradients = X.T @ (predictions - y) / X.shape[0]
        return gradients

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict(self, X_test, threshold=0.5):
        predictions = self.sigmoid(X_test @ self.beta)
        labels = np.where(predictions > threshold, 1, 0)
        return labels

    def fit(self, X_train, y_train):
        X_train_new = np.concatenate((X_train, np.ones((X_train.shape[0], 1))), axis=1)
        last_loss = 0
        momentum = 0

        for _ in range(self.max_iter):
            gradients = self.loss_derivative(X_train_new, y_train)

            # Apply momentum
            velocity = self.momentum * momentum - self.lr * gradients
            momentum = velocity

            self.beta += velocity

            current_loss = self.loss(X_train_new, y_train)
            if np.abs(current_loss - last_loss) < self.tol:
                break

            last_loss = current_loss

"""TODO: Predict the "Outcome" for the testing samples. (5 points)"""

def check_for_strings(arr):
  sw = 0
  arr_df = pd.DataFrame(arr)
  for index, row in arr_df.iterrows():
      for col, value in row.items():
          if type(value) is str:
            sw = 1
            print(f"Index: {index} Column: {col}, Value: {value}")

  if sw == 0:
    print("there is no string")

check_for_strings(X_train)

check_for_strings(y_train)

check_for_strings(X_test)

type(X_test), type(X_train), type(y_train)

y_train_nd = y_train.to_numpy()

X_train.shape , type(y_train_nd) ,y_train_nd.shape , y_train.shape

y_train_reshaped = y_train_nd.reshape(-1,)

model2 = GDLogisticRegression(n_features=X_train.shape[1])
model2.fit(X_train, y_train_reshaped)

y_pred_2 = model.predict(X_test)

"""# P5: Evaluation (15 points)

TODO: Calculate `precision`, `recall`, and `f1-score macro` using your own code. (Search what f1-score and recall are) **(each part 5 points)**
"""

def precision(y_true, y_pred):
  y_true = y_true.squeeze()
  true_pos = np.sum(y_true * y_pred)
  false_pos = np.sum(y_pred * (1 - y_true))
  if true_pos + false_pos == 0:
    return 0
  else:
    return true_pos / (true_pos + false_pos)

def recall(y_true, y_pred):
  y_true = y_true.squeeze()
  true_pos = np.sum(y_true * y_pred)
  false_neg = np.sum((1 - y_true) * (1 - y_pred))
  if true_pos + false_neg == 0:
    return 0
  else:
    return true_pos / (true_pos + false_neg)

def f1_score(y_true, y_pred):
  p = precision(y_true, y_pred)
  r = recall(y_true, y_pred)
  if p + r == 0:
    return 0
  else:
    return 2 * p * r / (p + r)

type(y_pred_2), y_pred_2, y_pred_2.shape

y_test_nd = y_test.to_numpy()

type(y_test), y_test, y_test.shape

precision(y_test , y_pred_2)

recall(y_test , y_pred_2)

f1_score(y_test , y_pred_2)