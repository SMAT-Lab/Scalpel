import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    
    for i in range(len(series) - window_size):
        x_temp = []
        for j in range(window_size):
            x_temp.append(series[i + j])
        X.append(x_temp)
        y.append(series[i+window_size])
        

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    model.add(Dense(1))
    return model


### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    punctuation = ['!', ',', '.', ':', ';', '?']
    #Convert to lowercase
    text = text.lower()

    #Get the length of the text and initialize a counter
    length = len(text)
    i = 0

    #Iterate through each character and if the character is not approved,
    #then delete the character
    while i < length:
        if (ord(text[i]) < 97 or ord(text[i]) > 122) and (text[i] != " " and text[i] not in punctuation):
            text = text[:i] + text[i+1:]
            length = len(text)
            i-=1 #reposition the counter since we decreased by a letter
        i+= 1
    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    for i in range(0, len(text) - window_size, step_size):
        inputs.append(text[i:i + window_size])
        outputs.append(text[i+window_size])
        
    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    model.add(Dense(num_chars))
    model.add(Activation('softmax'))
    return model
