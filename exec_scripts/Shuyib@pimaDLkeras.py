#!/usr/bin/env python
# coding: utf-8
# In[218]:
# I'll start by importing the data 
# importing modules that we'll need for the analysis
import pandas as pd
import numpy as np
df = pd.read_csv("diabetes.csv") # importing our data into the notebook
print(df.head(5)) # Examine first columns
print ("") # spacing for better reading
print (df.columns) # All the columns, we'll work with, they are formatted correctly
# In[219]:
# Examining row object of columns, and a doing some summary statistics
print (df.info())
# we have 9 columns and 768 rows
# Doesn't need additional cleaning for the column names they are consistent except BMI
# Since it's already an acronymn i suppose that was the best way to format it.
print ("")
print (df.describe())
# there's something wrong with some columns, i think they are missing values for some columns such as BloodPressure since
# there are zeros in the minimum BMI as well as Glucose,BloodPressure,SkinThickness and Insulin
# Let's count the number of these occurences and draw some plots.
# In[220]:
#print(df.BMI.value_counts()); print ("") # 11 missing BMI records
#print(df.Glucose.value_counts()); print ("") # 5 missing
#print(df.BloodPressure.value_counts()); print ("") # 35 missing records
#print(df.SkinThickness.value_counts()); print ("") # 227 missing records Not sure about this one.
#print(df.Insulin.value_counts()); print ("") # 374 missing records
# Saving up on space
# i've already indicated the answers to the number of missing values for some colums
# percentage of data missing
missing = 11 + 5 + 35 + 374 # adding up the missing value occurences
msg = "About {}% missing data points in the pima indians dataset if i'm not wrong."
print (msg.format(round(missing/768 * 100))) # finding the percentage of missing data on the columns.
# I'll use an imputation strategy in the workflow to deal with missing data
# In[221]:
# exploratory visualisation to see if there is any correlation between columns
# import necessary modules/packages
import matplotlib.pyplot as plt
import seaborn as sns
sns.set() 
#plt.title("Pairplot between the different columns of the dataset.")
sns.pairplot(df, vars = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin"])
sns.pairplot(df, vars = ["BMI","DiabetesPedigreeFunction","Age", "Outcome"])
plt.show()
# In[222]:
# some variables seem correlated. Let's try finding the pearson correlation coefficient for one.
# I'll try a correlation between Glucose column and Insulin
Glucoins = np.corrcoef(df.Insulin, df.Glucose)
print (Glucoins); print ("")
# that wasn't what i expected. 0.3 is  really low positive correlation
# I learned how to format heatmaps in seaborn so i'll draw one.
# Specify the columns
cols = df[df.columns].corr()
plt.title("Heatmap to see correlation of different variables in the pima indians dataset")
sns.heatmap(cols, annot = True)
plt.show()
# In[223]:
# Converting the dataframe into a numpy matrix
# this is a necessary step to proceed with the analysis of the data set for the algorithm in the library to work 
target = df['Outcome'].values
predictors = df.drop('Outcome', axis = 1).values
print (target)
print (predictors)
# In[224]:
# first try with Keras
# Call the necessary modules
from keras.models import Sequential
from keras.layers import Dense
# Specify model architecture
model = Sequential()
# add first layer
model.add(Dense(12, input_dim = 8, kernel_initializer = 'uniform',activation = 'relu')) # minus the target variable
# add second layer
model.add(Dense(8, kernel_initializer = 'uniform', activation = 'relu')) 
# add an output layer
model.add(Dense(1, kernel_initializer = 'uniform', activation = 'sigmoid')) 
# compile the model
model.compile(optimizer='adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
# Fit the model
model.fit(predictors, target)
# In[225]:
from keras.callbacks import EarlyStopping
# Specify model architecture
model2 = Sequential()
# add first layer
model2.add(Dense(12, input_dim = 8, kernel_initializer = 'uniform',activation = 'relu')) # minus the target variable
# add second layer
model2.add(Dense(8, kernel_initializer = 'uniform', activation = 'relu')) 
# add an output layer
model2.add(Dense(1, kernel_initializer = 'uniform', activation = 'sigmoid')) 
# compile the model
model2.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
# adding the early stopping 
early_stopping_monitor = EarlyStopping(patience=2)
# fit the model and notice the addition arguments
# Fit the model and split the data
model2.fit(predictors, target, epochs = 30, validation_split = 0.2, callbacks = [early_stopping_monitor])
# In[226]:
#from keras.optimizers import SGD
#n_cols = predictors.shape[1]
#input_shape = (n_cols,)
#def get_new_model(input_shape = input_shape):
    #model3 = Sequential()
    #model3.add(Dense(100, activation='relu', input_shape = input_shape))
    #model3.add(Dense(100, activation='relu'))
    #model3.add(Dense(2, activation='softmax'))
    #return model3
#lr_to_test = [.000001, 0.01, 1]
# loop over learning rates
#for lr in lr_to_test:
    #print('\n\nTesting model with learning rate: %f\n'%lr )
    #model = get_new_model()
    #my_optimizer = SGD(lr=lr)
    #model.compile(optimizer = my_optimizer, loss = 'categorical_crossentropy')
    #model.fit(predictors, target)
# In[227]:
#from keras.optimizers import 
#def get_new_model(input_shape = (n_cols,)):
    #model4 = Sequential()
    #model4.add(Dense(12, input_dim = 8, kernel_initializer = 'uniform',activation = 'relu')) # minus the target variable
    #model4.add(Dense(8, kernel_initializer = 'uniform', activation = 'relu')) 
    #model4.add(Dense(1, kernel_initializer = 'uniform', activation = 'sigmoid')) 
    #return(model)
#lr_to_test = [.000001, 0.01, 1]
# loop over learning rates
#for lr in lr_to_test:
    #model = get_new_model()
    #my_optimizer = SGD(lr=lr)
    #model.compile(optimizer = my_optimizer, loss = 'categorical_crossentropy')
    #model.fit(predictors, target)
# In[228]:
# Model inspection
model.summary() ; print ("")
model.get_weights()
# In[229]:
early_stopping_monitor = EarlyStopping(patience=2)
model3 = Sequential()
# add first layer doubled number of units
model3.add(Dense(24, input_dim = 8, kernel_initializer = 'uniform', activation = 'relu')) # minus the target variable
# add second layer
model3.add(Dense(16, kernel_initializer = 'uniform', activation = 'relu')) 
# add an output layer
model3.add(Dense(1, kernel_initializer = 'uniform', activation = 'sigmoid')) 
# compile the model
model3.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
# Fit previous model
model2_train = model2.fit(predictors, target, epochs = 15, validation_split = 0.2, callbacks = [early_stopping_monitor],
                         verbose = False)
# Fit new model3
model3_train = model3.fit(predictors, target, epochs = 15, validation_split = 0.2, callbacks = [early_stopping_monitor],
                         verbose = False)
# Compare the two with graph
plt.plot(model2_train.history['val_loss'], 'r', model3_train.history['val_loss'], 'g')
plt.title("Comparing different validation scores of two models in different epochs")
plt.xlabel('Epochs')
plt.ylabel('Validation score')
plt.show()
# In[230]:
model3 = Sequential()
# add first layer doubled 
model3.add(Dense(150, input_dim = 8, kernel_initializer = 'uniform', activation = 'sigmoid')) # minus the target variable
# add second layer
model3.add(Dense(150, kernel_initializer = 'uniform', activation = 'relu')) 
# add third layer
model3.add(Dense(150, kernel_initializer = 'uniform', activation = 'relu')) 
# add fourth layer
model3.add(Dense(150, kernel_initializer = 'uniform', activation = 'relu'))
# add fifth layer
model3.add(Dense(150, kernel_initializer = 'uniform', activation = 'relu'))
# add an output layer
model3.add(Dense(1, kernel_initializer = 'uniform', activation = 'sigmoid')) 
# compile the model
model3.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
# Fit previous model
model2_train = model2.fit(predictors, target, epochs = 15, validation_split = 0.2, callbacks = [early_stopping_monitor],
                         verbose = False)
# Fit new model3
model3_train = model3.fit(predictors, target, epochs = 15, validation_split = 0.2, callbacks = [early_stopping_monitor],
                         verbose = False)
# Compare the two with graph
plt.plot(model2_train.history['val_loss'], 'r', model3_train.history['val_loss'], 'g')
plt.title("Comparing different validation scores of two models in different epochs")
plt.xlabel('Epochs')
plt.ylabel('Validation score')
plt.show()
# In[231]:
# Look at the previous model
model.summary() ; print ("")
model.get_weights()
# In[232]:
# Testing model 3
model3 = Sequential()
# add first layer doubled 
model3.add(Dense(150, input_dim = 8, kernel_initializer = 'uniform', activation = 'sigmoid')) # minus the target variable
# add second layer
model3.add(Dense(150, kernel_initializer = 'uniform', activation = 'relu')) 
# add third layer
model3.add(Dense(150, kernel_initializer = 'uniform', activation = 'relu')) 
# add fourth layer
model3.add(Dense(150, kernel_initializer = 'uniform', activation = 'relu'))
# add fifth layer
model3.add(Dense(150, kernel_initializer = 'uniform', activation = 'relu'))
# add an output layer
model3.add(Dense(1, kernel_initializer = 'uniform', activation = 'sigmoid')) 
# compile the model
model3.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
# adding the early stopping 
early_stopping_monitor = EarlyStopping(patience=2)
# fit the model and notice the addition arguments
# Fit the model
model2.fit(predictors, target, epochs = 30, validation_split = 0.2, callbacks = [early_stopping_monitor])