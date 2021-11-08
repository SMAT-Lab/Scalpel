#!/usr/bin/env python
# coding: utf-8
# In[113]:
import numpy as np
import tensorflow as tf
# In[114]:
with open('reviews.txt', 'r') as f:
    reviews = f.read()
with open('labels.txt', 'r') as f:
    labels = f.read()
# In[115]:
reviews[:2000]
# In[116]:
from string import punctuation
all_text = ''.join([c for c in reviews if c not in punctuation])
reviews = all_text.split('\n')
all_text = ' '.join(reviews)
words = all_text.split()
# In[117]:
all_text[:2000]
# In[118]:
words[:100]
# In[119]:
from collections import Counter
# Create your dictionary that maps vocab words to integers here
word_counts = Counter(words)
sorted_vocab = sorted(word_counts)
int_to_vocab = {i+1: word for i, word in enumerate(sorted_vocab)}
vocab_to_int = {word: i for i, word in int_to_vocab.items()}
# Convert the reviews to integers, same shape as reviews list, but with integers
reviews_ints = []
for review in reviews:
    reviews_ints.append([vocab_to_int[word] for word in review.split()])
# In[120]:
# Convert labels to 1s and 0s for 'positive' and 'negative'
labels = labels.split('\n')
labels = np.array([1 if i == 'positive' else 0 for i in labels])
labels[:10]
# In[121]:
from collections import Counter
review_lens = Counter([len(x) for x in reviews_ints])
print("Zero-length reviews: {}".format(review_lens[0]))
print("Maximum review length: {}".format(max(review_lens)))
# In[122]:
# Filter out that review with 0 length
# Get index of 0 length review
zero_index = [i for i, review in enumerate(reviews_ints) if len(review) == 0][0]
print("Total reviews before delete: %i\nTotal labels before delete: %i" % (len(reviews_ints), len(labels)))
# Remove 0 length review and its corresponding label
del reviews_ints[zero_index]
labels = np.delete(labels, zero_index)
print("\nTotal reviews after delete: %i\nTotal labels after delete: %i" % (len(reviews_ints), len(labels)))
# In[123]:
seq_len = 200
# Generate the blank features array
features = np.zeros((len(reviews_ints), seq_len), dtype=np.int)
for i, review in enumerate(reviews_ints):
    # Get truncated review
    truncated_review = np.array(review[:seq_len])
    # Append truncated review to end of each feature row array
    features[i, -len(truncated_review):] = truncated_review
# In[124]:
features[:10,:100]
# In[125]:
split_frac = 0.8
i_split = int(len(features) * split_frac)
train_x, val_x = features[:i_split], features[i_split:]
train_y, val_y = labels[:i_split], labels[i_split:]
i_split = int(len(val_x) * 0.5)
val_x, test_x = val_x[:i_split], val_x[i_split:]
val_y, test_y = val_y[:i_split], val_y[i_split:]
print("\t\t\tFeature Shapes:")
print("Train set: \t\t{}".format(train_x.shape), 
      "\nValidation set: \t{}".format(val_x.shape),
      "\nTest set: \t\t{}".format(test_x.shape))
# In[126]:
# Define hyperparameters
lstm_size = 256
lstm_layers = 1
batch_size = 500
learning_rate = 0.001
# In[127]:
n_words = len(vocab_to_int)
# Create the graph object
graph = tf.Graph()
# Add nodes to the graph
with graph.as_default():
    inputs_ = tf.placeholder(tf.int32, [None, None], name='inputs')
    labels_ = tf.placeholder(tf.int32, [None, None], name='labels')
    keep_prob = tf.placeholder(tf.float32, name='keep_prob')
# In[128]:
# Size of the embedding vectors (number of units in the embedding layer)
embed_size = 300 
with graph.as_default():
    embedding = tf.Variable(tf.random_uniform((n_words, embed_size), -1, 1))
    embed = tf.nn.embedding_lookup(embedding, inputs_)
# In[129]:
with graph.as_default():
    # Your basic LSTM cell
    lstm = tf.contrib.rnn.BasicLSTMCell(lstm_size)
    
    # Add dropout to the cell
    drop = tf.contrib.rnn.DropoutWrapper(lstm, output_keep_prob=keep_prob)
    
    # Stack up multiple LSTM layers, for deep learning
    cell = tf.contrib.rnn.MultiRNNCell([drop] * lstm_layers)
    
    # Getting an initial state of all zeros
    initial_state = cell.zero_state(batch_size, tf.float32)
# In[130]:
with graph.as_default():
    outputs, final_state = tf.nn.dynamic_rnn(cell, embed, initial_state=initial_state)
# In[131]:
with graph.as_default():
    predictions = tf.contrib.layers.fully_connected(outputs[:, -1], 1, activation_fn=tf.sigmoid)
    cost = tf.losses.mean_squared_error(labels_, predictions)
    
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)
# In[132]:
with graph.as_default():
    correct_pred = tf.equal(tf.cast(tf.round(predictions), tf.int32), labels_)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
# In[133]:
def get_batches(x, y, batch_size=100):
    
    n_batches = len(x)//batch_size
    x, y = x[:n_batches*batch_size], y[:n_batches*batch_size]
    for ii in range(0, len(x), batch_size):
        yield x[ii:ii+batch_size], y[ii:ii+batch_size]
# In[134]:
test_acc = []
with tf.Session(graph=graph) as sess:
    saver.restore(sess, tf.train.latest_checkpoint('checkpoints'))
    test_state = sess.run(cell.zero_state(batch_size, tf.float32))
    for ii, (x, y) in enumerate(get_batches(test_x, test_y, batch_size), 1):
        feed = {inputs_: x,
                labels_: y[:, None],
                keep_prob: 1,
                initial_state: test_state}
        batch_acc, test_state = sess.run([accuracy, final_state], feed_dict=feed)
        test_acc.append(batch_acc)
    print("Test accuracy: {:.3f}".format(np.mean(test_acc)))