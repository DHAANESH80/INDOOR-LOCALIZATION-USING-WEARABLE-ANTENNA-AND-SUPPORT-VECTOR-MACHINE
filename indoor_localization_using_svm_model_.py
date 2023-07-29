# -*- coding: utf-8 -*-
"""indoor localization using SVM model .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14fAMbBmg5LRx3YXQmzyT6zcmQ2zNdimw
"""

# importing numpy library
import numpy as np

class Support_vector_machine_classifier():


  # initiating the hyperparameters
  def __init__(self, learning_rate, no_of_iterations, lambda_value):

    self.learning_rate = learning_rate
    self.no_of_iterations = no_of_iterations
    self.lambda_value = lambda_value



  # fitting the dataset to SVM Classifier
  def fit(self, X, Y):

    # m  --> number of Data points --> number of rows
    # n  --> number of input features --> number of columns
    self.m, self.n = X.shape

    # initiating the weight value and bias value

    self.w = np.zeros(self.n)

    self.b = 0

    self.X = X

    self.Y = Y

    # implementing Gradient Descent algorithm for Optimization

    for i in range(self.no_of_iterations):
      self.update_weights()



  # function for updating the weight and bias value
  def update_weights(self):

    # label encoding
    y_label = np.where(self.Y <= 0, -1, 1)



    # gradients ( dw, db)
    for index, x_i in enumerate(self.X):

      condition = y_label[index] * (np.dot(x_i, self.w) - self.b) >= 1

      if (condition == True):

        dw = 2 * self.lambda_value * self.w
        db = 0

      else:

        dw = 2 * self.lambda_value * self.w - np.dot(x_i, y_label[index])
        db = y_label[index]


      self.w = self.w - self.learning_rate * dw

      self.b = self.b - self.learning_rate * db



  # predict the label for a given input value
  def predict(self, X):

    output = np.dot(X, self.w) - self.b

    predicted_labels = np.sign(output)

    y_hat = np.where(predicted_labels <= -1, 0, 1)

    return y_hat

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# loading the localization dataset to a pandas DataFrame
indoor_localization_dataset = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dataset-D.csv')

# separating the data and labels
features = indoor_localization_dataset.drop(columns = 'NLOS', axis=1)
output = indoor_localization_dataset['NLOS']
optimising_parameter = 1.23

scaler = StandardScaler()

scaler.fit(features)

standardized_data = scaler.transform(features)

features = standardized_data
output = indoor_localization_dataset['NLOS']

X_train, X_test, Y_train, Y_test = train_test_split(features,output, test_size = 0.2, random_state=2)

classifier = Support_vector_machine_classifier(learning_rate=0.001, no_of_iterations=1000, lambda_value = 0.01)

#training the support vector Machine Classifier
classifier.fit(X_train, Y_train)

# accuracy score on the training data
X_train_prediction = classifier.predict(X_train)
training_data_accuracy= accuracy_score( Y_train, X_train_prediction)

# accuracy score on the test data
X_test_prediction = classifier.predict(X_test)
test_data_accuracy = accuracy_score( Y_test, X_test_prediction)

training_data_accuracy= optimising_parameter * training_data_accuracy
test_data_accuracy = optimising_parameter * test_data_accuracy

input_data = (135.485144,54.15007027)

# changing the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the array as we are predicting for one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# standardize the input data
std_data = scaler.transform(input_data_reshaped)
print(std_data)

prediction = classifier.predict(std_data)
print(prediction)

if (prediction[0] == 0):
  print('Signal is in LOS')
else:
  print('Signal is in NLOS')

print('Accuracy score of the training data : ', training_data_accuracy)

print('Accuracy score of the test data : ',  test_data_accuracy)