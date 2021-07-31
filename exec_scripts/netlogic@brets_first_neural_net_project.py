#!/usr/bin/env python
# coding: utf-8
# In[1622]:
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# In[1623]:
data_path = 'Bike-Sharing-Dataset/hour.csv'
rides = pd.read_csv(data_path)
# In[1624]:
rides.head()
# In[1625]:
rides[:24*10].plot(x='dteday', y='cnt')
# In[1626]:
dummy_fields = ['season', 'weathersit', 'mnth', 'hr', 'weekday']
for each in dummy_fields:
    dummies = pd.get_dummies(rides[each], prefix=each, drop_first=False)
    rides = pd.concat([rides, dummies], axis=1)
fields_to_drop = ['instant', 'dteday', 'season', 'weathersit', 
                  'weekday', 'atemp', 'mnth', 'workingday', 'hr']
data = rides.drop(fields_to_drop, axis=1)
data.head()
# In[1627]:
quant_features = ['casual', 'registered', 'cnt', 'temp', 'hum', 'windspeed']
# Store scalings in a dictionary so we can convert back later
scaled_features = {}
for each in quant_features:
    mean, std = data[each].mean(), data[each].std()
    scaled_features[each] = [mean, std]
    data.loc[:, each] = (data[each] - mean)/std
# In[1628]:
# Save data for approximately the last 21 days 
test_data = data[-21*24:]
# Now remove the test data from the data set 
data = data[:-21*24]
# Separate the data into features and targets
target_fields = ['cnt', 'casual', 'registered']
features, targets = data.drop(target_fields, axis=1), data[target_fields]
test_features, test_targets = test_data.drop(target_fields, axis=1), test_data[target_fields]
# In[1629]:
# Hold out the last 60 days or so of the remaining data as a validation set
train_features, train_targets = features[:-60*24], targets[:-60*24]
val_features, val_targets = features[-60*24:], targets[-60*24:]
# In[1630]:
class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        # Initialize weights
        self.weights_input_to_hidden = np.random.normal(0.0, self.input_nodes**-0.5, 
                                       (self.input_nodes, self.hidden_nodes))
        self.weights_hidden_to_output = np.random.normal(0.0, self.hidden_nodes**-0.5, 
                                       (self.hidden_nodes, self.output_nodes))
        self.lr = learning_rate
        
        #### TODO: Set self.activation_function to your implemented sigmoid function ####
        #
        # Note: in Python, you can define a function with a lambda expression,
        # as shown below.
        self.activation_function = lambda x :  (1 / (1 + np.exp(-x)))  # Replace 0 with your sigmoid calculation.
        
        ### If the lambda code above is not something you're familiar with,
        # You can uncomment out the following three lines and put your 
        # implementation there instead.
        #
        #def sigmoid(x):
        #    return 0  # Replace 0 with your sigmoid calculation here
        #self.activation_function = sigmoid
                    
    
    def train(self, features, targets):
        ''' Train the network on batch of features and targets. 
        
            Arguments
            ---------
            
            features: 2D array, each row is one data record, each column is a feature
            targets: 1D array of target values
        
        '''
        n_records = features.shape[0]
        
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)
        
        for X, y in zip(features, targets):
            ### this section mirrors the logic
            ### learned in Implementing Backpropagation
            ### Lesson 2 -> Section 16
            #### Implement the forward pass here ####
            ### Forward pass ###
            # TODO: Hidden layer - Replace these values with your calculations.
            # hidden inputs are signals into hidden layer
            # they should be dot producted against the 
            # current input weights to hidden
            hidden_inputs =  np.dot( X, self.weights_input_to_hidden)  # signals into hidden layer
            # output (h) is a result of our sigmoid function
            # against the dot product of the input
            hidden_outputs =  self.activation_function(hidden_inputs) # signals from hidden layer
            # TODO: Output layer - Replace these values with your calculations.
            # using the weight of the hidden output find the dot product
            # against the result of the hidden output
            final_inputs = np.dot( hidden_outputs, self.weights_hidden_to_output )  # signals into final output layer
            
            # notes say activation function is f(x)=x 
            # so in theory these are the same?
            # if activation is needed this final_inputs could be
            # be wrapped in one
            final_outputs =  final_inputs # signals from final output layer
            #### Implement the backward pass here ####
            ### Backward pass ###
            # TODO: Output error - Replace this value with your calculations.
            error = y  - final_outputs # Output layer error is the difference between desired target and actual output.
            # TODO: Calculate the hidden layer's contribution to the error
            # WELL THAT WAS WRONG output_error_term = ( error * (final_outputs*(1-final_outputs))  )  #sigmoid prime
            
            output_error_term = error # ( error * ( 1/final_outputs))
            # print( "output_error_term => "  , output_error_term , " wts ",self.weights_hidden_to_output );
            # THIS IS MY PROBLEM LINE , I DON'T UNDERSTAND SOMETHING
            #   dot product is commutative so I can exchange parameters
            # TODO: Backpropagated error terms - Replace these values with your calculations.
            hidden_error_term = np.dot(  self.weights_hidden_to_output, output_error_term) *                     hidden_outputs * (1 - hidden_outputs )
            # Weight step (hidden to output)
            # print( "output_error_term => "  , output_error_term , " hout ", hidden_outputs );
            delta_weights_h_o += output_error_term * hidden_outputs[:, None]
            
            # Weight step (input to hidden)
            delta_weights_i_h +=  hidden_error_term * X[:, None]  # Weight step (input to hidden)
        # TODO: Update the weights - Replace these values with your calculations.
        self.weights_hidden_to_output += ( self.lr * (delta_weights_h_o / n_records)) # update hidden-to-output weights with gradient descent step
        self.weights_input_to_hidden += (self.lr * (delta_weights_i_h / n_records)) # update input-to-hidden weights with gradient descent step
    def run(self, features):
        ''' Run a forward pass through the network with input features 
        
            Arguments
            ---------
            features: 1D array of feature values
        '''
        
        #### Implement the forward pass here ####
        # TODO: Hidden layer - replace these values with the appropriate calculations.
        hidden_inputs = np.dot(features, self.weights_input_to_hidden) # signals into hidden layer
        hidden_outputs = self.activation_function(hidden_inputs) # signals from hidden layer
        
        # TODO: Output layer - Replace these values with the appropriate calculations.
        final_inputs =  np.dot(hidden_outputs, self.weights_hidden_to_output) # signals into final output layer
        final_outputs = final_inputs # signals from final output layer 
        
        return final_outputs
# In[1631]:
def MSE(y, Y):
    return np.mean((y-Y)**2)
# In[1632]:
import unittest
inputs = np.array([[0.5, -0.2, 0.1]])
targets = np.array([[0.4]])
test_w_i_h = np.array([[0.1, -0.2],
                       [0.4, 0.5],
                       [-0.3, 0.2]])
test_w_h_o = np.array([[0.3],
                       [-0.1]])
class TestMethods(unittest.TestCase):
    
    ##########
    # Unit tests for data loading
    ##########
    
    def test_data_path(self):
        # Test that file path to dataset has been unaltered
        self.assertTrue(data_path.lower() == 'bike-sharing-dataset/hour.csv')
        
    def test_data_loaded(self):
        # Test that data frame loaded
        self.assertTrue(isinstance(rides, pd.DataFrame))
    
    ##########
    # Unit tests for network functionality
    ##########
    def test_activation(self):
        network = NeuralNetwork(3, 2, 1, 0.5)
        # Test that the activation function is a sigmoid
        self.assertTrue(np.all(network.activation_function(0.5) == 1/(1+np.exp(-0.5))))
    def test_train(self):
        # Test that weights are updated correctly on training
        network = NeuralNetwork(3, 2, 1, 0.5)
        network.weights_input_to_hidden = test_w_i_h.copy()
        network.weights_hidden_to_output = test_w_h_o.copy()
        
        network.train(inputs, targets)
        
        self.assertTrue(np.allclose(network.weights_hidden_to_output, 
                                    np.array([[ 0.37275328], 
                                              [-0.03172939]])))
        
        self.assertTrue(np.allclose(network.weights_input_to_hidden,
                                    np.array([[ 0.10562014, -0.20185996], 
                                              [0.39775194, 0.50074398], 
                                              [-0.29887597, 0.19962801]])))
            
    def test_run(self):
        # Test correctness of run method
        network = NeuralNetwork(3, 2, 1, 0.5)
        network.weights_input_to_hidden = test_w_i_h.copy()
        network.weights_hidden_to_output = test_w_h_o.copy()
        self.assertTrue(np.allclose(network.run(inputs), 0.09998924))
suite = unittest.TestLoader().loadTestsFromModule(TestMethods())
unittest.TextTestRunner().run(suite)
# In[1633]:
import sys
### Set the hyperparameters here ###
# iterations( 4500, . 9, 8, 1 ) => Progress: 100.0% ... Training loss: 0.074 ... Validation loss: 0.140
# iterations( 4500, . 9, 10, 1 ) => Progress: 100.0% ... Training loss: 0.060 ... Validation loss: 0.163
# iterations( 4500, .8 , 8, 1 ) => Progress: 100.0% ... Training loss: 0.093 ... Validation loss: 0.137
# iterations( 5000, .8 , 8, 1 ) => Progress: 100.0% ... Training loss: 0.062 ... Validation loss: 0.163
# iterations( 5000, .8 , 10, 1 ) => Progress: 100.0% ... Training loss: 0.058 ... Validation loss: 0.142
# iterations( 5000, .7 , 10, 1 ) => Progress: 100.0% ... Training loss: 0.059 ... Validation loss: 0.146
####################################################################################################
# iterations( 5000, .95 , 10, 1 ) => Progress: 100.0% ... Training loss: 0.056 ... Validation loss: 0.124
###################################################################################################
# iterations( 5000, .90 , 10, 1 ) => Progress: 100.0% ... Training loss: 0.060 ... Validation loss: 0.152
# iterations( 5000, .90 , 12, 1 ) => Progress: 100.0% ... Training loss: 0.054 ... Validation loss: 0.150
# iterations( 6000, .90 , 12, 1 ) => Progress: 100.0% ... Training loss: 0.052 ... Validation loss: 0.151
# iterations( 6000, .90 , 12, 1 ) => Progress: 100.0% ... Training loss: 0.052 ... Validation loss: 0.151
# iterations( 5000, .90 , 4, 1 ) => Progress: 100.0% ... Training loss: 0.074 ... Validation loss: 0.152
# iterations( 5000, .90 , 6, 1 ) => Progress: 100.0% ... Training loss: 0.061 ... Validation loss: 0.166
# Deciding to go with configuration that had lowest validation lost but close times +-.005%
iterations = 5000
learning_rate = .95 # make sure we do not zig zag past convergence
hidden_nodes = 10 # x times our input nodes
output_nodes = 1
N_i = train_features.shape[1]
network = NeuralNetwork(N_i, hidden_nodes, output_nodes, learning_rate)
losses = {'train':[], 'validation':[]}
for ii in range(iterations):
    # Go through a random batch of 128 records from the training data set
    batch = np.random.choice(train_features.index, size=128)
    X, y = train_features.ix[batch].values, train_targets.ix[batch]['cnt']
                             
    network.train(X, y)
    
    # Printing out the training progress
    train_loss = MSE(network.run(train_features).T, train_targets['cnt'].values)
    val_loss = MSE(network.run(val_features).T, val_targets['cnt'].values)
    sys.stdout.write("\rProgress: {:2.1f}".format(100 * ii/float(iterations))                      + "% ... Training loss: " + str(train_loss)[:5]                      + " ... Validation loss: " + str(val_loss)[:5])
    sys.stdout.flush()
    
    losses['train'].append(train_loss)
    losses['validation'].append(val_loss)
# In[1634]:
plt.plot(losses['train'], label='Training loss')
plt.plot(losses['validation'], label='Validation loss')
plt.legend()
_ = plt.ylim()
# In[1635]:
fig, ax = plt.subplots(figsize=(8,4))
mean, std = scaled_features['cnt']
predictions = network.run(test_features).T*std + mean
ax.plot(predictions[0], label='Prediction')
ax.plot((test_targets['cnt']*std + mean).values, label='Data')
ax.set_xlim(right=len(predictions))
ax.legend()
dates = pd.to_datetime(rides.ix[test_data.index]['dteday'])
dates = dates.apply(lambda d: d.strftime('%b %d'))
ax.set_xticks(np.arange(len(dates))[12::24])
_ = ax.set_xticklabels(dates[12::24], rotation=45)