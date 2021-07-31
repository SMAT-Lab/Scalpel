#!/usr/bin/env python
# coding: utf-8
# In[1]:
import play as p
p.play()
# In[2]:
# Code goes here 
"""
First you would need to go through the description/meta-data
related to the dataset. It is present in the following file: 
    ./data/pima-indians-diabetes.names
    
Try going through the file and figure out how the dataset has
been structured, what are the features, etc.
The dataset is in the following file:
    ./data/pima-indians-diabetes.csv
Next, open the file in python as we did in the previous exa-
ple and try playing around with it. Try to figure out how to 
extract the data from the file and how to store it.
(HINT: Think of the data strucures in Python)
"""
# code for printing the dataset goes here
fh = open("./data/pima-indians-diabetes.csv")
data=[]
for line in fh:
    temp = line.split(",")
    temp = list( map ( ( lambda x: float( x.strip() ) ),temp ) )
    data.append(temp)
print(data)
# In[3]:
"""
Now try and divide the data that we have into training and testing samples. 
Usual training/testing ratios are 60/40, 70/30 or 80/20
Divide the dataset now into a ratio of 70/30
"""
train_data = []  #This is the training data
test_data = [] #This is the test data
num_data = len(data)
ratio = 0.7
train_data = data[:int(num_data*ratio)]
test_data = data[int(num_data*ratio):]
num_tr_data = len(train_data)
num_te_data = len(test_data)
print(num_tr_data)
print(num_te_data)
# In[4]:
"""
Now we need to find the probabilities of each class. Since we just have 2 here,
you need to find P(0) and P(1).
"""
num_0 = 0
num_1 = 0
for i in train_data:
    if i[-1] == 0:
        num_0+=1
    else:
        num_1+=1
p_0 = num_0/num_tr_data
p_1 = num_1/num_tr_data
print(p_0,p_1)
# In[5]:
"""
Now that we have our class probabilities, let us sort our training set according to the class values.
This means that you need to segregate all the lines depending on the class they belong to.
Fill the separate_class() function appropriately
"""
def separate_class(train_data):
    separated_data = {}
    for i in train_data:
        if i[-1] not in separated_data:
            separated_data[i[-1]] = []
        separated_data[i[-1]].append(i)
    return separated_data
print(separate_class(train_data))
# In[6]:
"""
After we have separated each data entry according to its class, let us find the probability of each attribute
with respect to each class, i.e, P(x_i|y)
How do you suggest we do that? (Think about distributions!)
"""
# In[7]:
"""
Let us now quickly find out the mean and standard deviation. 
Fill the mean() and stddev() according to the given function definitions
'numbers' is an array that is an input for the function
"""
import math
def mean(numbers):
    return sum(numbers)/float(len(numbers))
def stddev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)
print(mean([1,2,3]),stddev([1,2,3]))
# In[8]:
"""
Now just for our convenience, let us accumulate a statistic for all attributes for each class. 
We would call this 'summarizing' our data.
We have already done this for you. You would have to print the output and deduce what it means.
Now, let us combine the summarize() and separate_class() method in order to summarize each attribute
according to the class.
Complete summarize_class() according to the function definition.
"""
def summarize(dataset):
    summaries=[]
    for attribute in range(len(dataset[0])):
        temp = []
        for row in dataset:
            temp.append(row[attribute])
        summaries.append((mean(temp),stddev(temp)))
    del summaries[-1]
    return summaries
def summarize_class(dataset):
    separated = separate_class(dataset)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances)
    return summaries
# In[9]:
"""
Next we code out a function for the gaussian distribution formula as mentioned above.
Fill out the function calculate_probability() according to the function definition provided
"""
def calculate_probability(x, mean, stdev):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
# In[12]:
"""
We now calculate the class probability of each attribute, i.e 
"""
def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.items():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            print(classSummaries[i])
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculate_probability(x, mean, stdev)
    return probabilities
"""
summaries = {0:[(1, 0.5)], 1:[(20, 5.0)]}
inputVector = [1.1, '?']
probabilities = calculateClassProbabilities(summaries, inputVector)
print('Probabilities for each class: ',probabilities)"""
def predict(summaries, inputVector):
    probabilities = calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel
summaries = {'A':[(1, 0.5)], 'B':[(20, 5.0)]}
inputVector = [1.1, '?']
result = predict(summaries, inputVector)
print('Prediction:', result)
def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
		predictions.append(result)
	return predictions
summaries = {'A':[(1, 0.5)], 'B':[(20, 5.0)]}
testSet = [[1.1, '?'], [19.1, '?']]
predictions = getPredictions(summaries, testSet)
print('Predictions: ', predictions)
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0
testSet = [[1,1,1,'a'], [2,2,2,'a'], [3,3,3,'b']]
predictions = ['a', 'a', 'a']
accuracy = getAccuracy(testSet, predictions)
print('Accuracy:', accuracy)
 
    
# In[17]:
def main():
	# prepare model
	summaries = summarize_class(train_data)
	# test model
	predictions = getPredictions(summaries, test_data)
	accuracy = getAccuracy(test_data, predictions)
	print('Accuracy: ',accuracy)
 
main()