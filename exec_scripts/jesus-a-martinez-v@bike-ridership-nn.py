#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# In[2]:
# Change accordingly
data_path = 'Bike-Sharing-Dataset/hour.csv'
rides = pd.read_csv(data_path)
# In[3]:
rides.head()  # Peak first 5 rows
# In[4]:
hours_in_a_day = 24
days_to_plot = 10
split_point = days_to_plot * hours_in_a_day
rides[:split_point].plot(x='dteday', y='cnt')
# In[5]:
dummy_fields = ['season', 'weathersit', 'mnth', 'hr', 'weekday']
for dummy_field in dummy_fields:
    dummies = pd.get_dummies(rides[dummy_field], prefix=dummy_field, drop_first=False)
    rides = pd.concat([rides, dummies], axis=1)
fields_to_drop = [
    'instant', 
    'dteday', 
    'season', 
    'weathersit',              
    'weekday', 
    'atemp', 
    'mnth', 
    'workingday', 
    'hr'
]
data = rides.drop(fields_to_drop, axis=1)
data.head()
# In[6]:
quant_features = ['casual', 'registered', 'cnt', 'temp', 'hum', 'windspeed']
# Store scalings in a dictionary so we can convert back later
scaled_features = {}
for quant_feature in quant_features:
    mean, std = data[quant_feature].mean(), data[quant_feature].std()
    scaled_features[quant_feature] = [mean, std]
    data.loc[:, quant_feature] = (data[quant_feature] - mean) / std
# In[7]:
# Save the last 21 days
number_of_test_days = 21
split_point = number_of_test_days * hours_in_a_day
test_data = data[-split_point:]
data = data[:-split_point]
# Separate the data into features and targets
target_fields = ['cnt', 'casual', 'registered']
features, targets = data.drop(target_fields, axis=1), data[target_fields]
test_features, test_targets = test_data.drop(target_fields, axis=1), test_data[target_fields]
# In[8]:
# Hold out the last 60 days of the remaining data as a validation set
number_of_validation_days = 60
split_point = number_of_validation_days * hours_in_a_day
train_features, train_targets = features[:-split_point], targets[:-split_point]
val_features, val_targets = features[-split_point:], targets[-split_point:]
# In[9]:
def sigmoid(x): 
    return 1. / (1. + np.exp(-x))
class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        # Initialize weights
        self.weights_input_to_hidden = np.random.normal(0.0, self.hidden_nodes ** -0.5, 
                                       size=(self.hidden_nodes, self.input_nodes))
        self.weights_hidden_to_output = np.random.normal(0.0, self.output_nodes ** -0.5, 
                                       size=(self.output_nodes, self.hidden_nodes))
        
        self.lr = learning_rate
        
        # Activation function is the sigmoid function
        self.activation_function = sigmoid
    
    def train(self, inputs_list, targets_list):
        
        # Convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T
        n_inputs = inputs.shape[0]
        
        ############# Forward pass #############
        # Hidden layer
        hidden_inputs = np.dot(self.weights_input_to_hidden, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # Output layer
        final_inputs = np.dot(self.weights_hidden_to_output, hidden_outputs)
        final_outputs = final_inputs
        
        
        ############# Backward pass ############# 
        # Output error (the gradient is just 1)
        output_errors = targets - final_outputs
        output_grad = 1
        
        # Hidden error & gradient
        hidden_errors = np.dot(self.weights_hidden_to_output.T, output_errors)
        hidden_grad = hidden_outputs * (1 - hidden_outputs)
        
        # Update weights
        self.weights_hidden_to_output += self.lr * np.dot(output_errors * output_grad, hidden_outputs.T)
        self.weights_input_to_hidden += self.lr * np.dot(hidden_errors * hidden_grad, inputs.T)
 
        
    def run(self, inputs_list):
        # Run a forward pass through the network
        inputs = np.array(inputs_list, ndmin=2).T
        
        # Hidden layer
        hidden_inputs = np.dot(self.weights_input_to_hidden, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # Output layer
        final_inputs = np.dot(self.weights_hidden_to_output, hidden_outputs)
        final_outputs = final_inputs
        
        return final_outputs
# In[10]:
def MSE(y, Y):
    """
    Calculates mean squared error between the target values and the neural network's predictions.
    :param y: Neural network predictions.
    :param Y: Actual target values.
    """
    return np.mean((y - Y) ** 2)
# In[11]:
import sys
### Hyperparameters ###
epochs = 500
learning_rate = 0.05
hidden_nodes = 10
output_nodes = 1
batch_size = 128
number_of_inputs = train_features.shape[1]
network = NeuralNetwork(number_of_inputs, hidden_nodes, output_nodes, learning_rate)
losses = {'train':[], 
          'validation':[]}
def print_epoch_progress_message(epoch, epochs, train_loss, val_loss):
    progress_message = str(100 * epoch / float(epochs))[:4]
    train_loss_message = str(train_loss)[:5]
    val_loss_message = str(val_loss)[:5]
    
    sys.stdout.write("\rProgress: " +  progress_message                     + "% ... Training loss: " + train_loss_message                      + " ... Validation loss: " + val_loss_message + "\n")
    
    
for epoch in range(epochs):
    # Go through a random batch of batch_size records from the training data set
    batch = np.random.choice(train_features.index, size=batch_size)
    for record, target in zip(train_features.iloc[batch].values, 
                              train_targets.iloc[batch]['cnt']):
        network.train(record, target)
    
    # Printing out the training progress
    predicted_train_y = network.run(train_features)
    actual_train_y =  train_targets['cnt'].values
    train_loss = MSE(predicted_train_y, actual_train_y)
    
    predicted_val_y = network.run(val_features)
    actual_val_y = val_targets['cnt'].values
    val_loss = MSE(predicted_val_y, actual_val_y)
    
    print_epoch_progress_message(epoch, epochs, train_loss, val_loss)
    
    losses['train'].append(train_loss)
    losses['validation'].append(val_loss)
# In[12]:
plt.plot(losses['train'], label='Training loss')
plt.plot(losses['validation'], label='Validation loss')
plt.legend()
# plt.ylim(ymax=0.5)
# In[13]:
fig, ax = plt.subplots(figsize=(8,4))
mean, std = scaled_features['cnt']
predictions = network.run(test_features) * std + mean
ax.plot(predictions[0], label='Prediction')
ax.plot((test_targets['cnt'] * std + mean).values, label='Data')
ax.set_xlim(right=len(predictions))
ax.legend()
dates = pd.to_datetime(rides.iloc[test_data.index]['dteday'])
dates = dates.apply(lambda d: d.strftime('%b %d'))
ax.set_xticks(np.arange(len(dates))[12::24])
_ = ax.set_xticklabels(dates[12::24], rotation=45)
# In[14]:
import unittest
inputs = [0.5, -0.2, 0.1]
targets = [0.4]
test_w_i_h = np.array([[0.1, 0.4, -0.3], 
                       [-0.2, 0.5, 0.2]])
test_w_h_o = np.array([[0.3, -0.1]])
class TestMethods(unittest.TestCase):
    
    ###############################
    # Unit tests for data loading #
    ###############################
    
    def test_data_path(self):
        # Test that file path to dataset has been unaltered
        self.assertTrue(data_path.lower() == 'bike-sharing-dataset/hour.csv')
        
    def test_data_loaded(self):
        # Test that data frame loaded
        self.assertTrue(isinstance(rides, pd.DataFrame))
    
    ########################################
    # Unit tests for network functionality #
    ########################################
    def test_activation(self):
        network = NeuralNetwork(3, 2, 1, 0.5)
        # Test that the activation function is a sigmoid
        self.assertTrue(np.all(network.activation_function(0.5) == 1 / (1 + np.exp(-0.5))))
    def test_train(self):
        # Test that weights are updated correctly on training
        network = NeuralNetwork(3, 2, 1, 0.5)
        network.weights_input_to_hidden = test_w_i_h.copy()
        network.weights_hidden_to_output = test_w_h_o.copy()
        
        network.train(inputs, targets)
        print('network.weights_hidden_to_output', network.weights_hidden_to_output)
        print('network.weights_input_to_hidden', network.weights_input_to_hidden)
        
        self.assertTrue(np.allclose(network.weights_hidden_to_output, 
                                    np.array([[ 0.37275328, -0.03172939]])))
        
        self.assertTrue(np.allclose(network.weights_input_to_hidden,
                                    np.array([[ 0.10562014,  0.39775194, -0.29887597],
                                              [-0.20185996,  0.50074398,  0.19962801]])))
    def test_run(self):
        # Test correctness of run method
        network = NeuralNetwork(3, 2, 1, 0.5)
        network.weights_input_to_hidden = test_w_i_h.copy()
        network.weights_hidden_to_output = test_w_h_o.copy()
        self.assertTrue(np.allclose(network.run(inputs), 0.09998924))
suite = unittest.TestLoader().loadTestsFromModule(TestMethods())
unittest.TextTestRunner().run(suite)