#!/usr/bin/env python
# coding: utf-8
# In[1]:
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
import helper
import problem_unittests as tests
source_path = 'data/small_vocab_en'
target_path = 'data/small_vocab_fr'
source_text = helper.load_data(source_path)
target_text = helper.load_data(target_path)
# In[2]:
view_sentence_range = (0, 10)
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
import numpy as np
print('Dataset Stats')
print('Roughly the number of unique words: {}'.format(len({word: None for word in source_text.split()})))
sentences = source_text.split('\n')
word_counts = [len(sentence.split()) for sentence in sentences]
print('Number of sentences: {}'.format(len(sentences)))
print('Average number of words in a sentence: {}'.format(np.average(word_counts)))
print()
print('English sentences {} to {}:'.format(*view_sentence_range))
print('\n'.join(source_text.split('\n')[view_sentence_range[0]:view_sentence_range[1]]))
print()
print('French sentences {} to {}:'.format(*view_sentence_range))
print('\n'.join(target_text.split('\n')[view_sentence_range[0]:view_sentence_range[1]]))
# In[3]:
def text_to_ids(source_text, target_text, source_vocab_to_int, target_vocab_to_int):
    """
    Convert source and target text to proper word ids
    :param source_text: String that contains all the source text.
    :param target_text: String that contains all the target text.
    :param source_vocab_to_int: Dictionary to go from the source words to an id
    :param target_vocab_to_int: Dictionary to go from the target words to an id
    :return: A tuple of lists (source_id_text, target_id_text)
    """
    # Implement Function
    # Reference material: Character Sequence to Sequence exercise/lectures
#     source_id_text = []
#     source_sentence_text = source_text.split('\n')
#     for sentence in source_sentence_text:
#         source_sentence_text_to_ids = [source_vocab_to_int[word] for word in sentence.split()]
#         source_id_text.append(source_sentence_text_to_ids)
#     target_id_text = []
#     target_sentence_text = target_text.split('\n')
#     for sentence in target_sentence_text:
#         target_sentence_text_to_ids = [target_vocab_to_int[word] for word in sentence.split()]
#         target_sentence_text_to_ids.append(target_vocab_to_int['<EOS>']) 
#         target_id_text.append(target_sentence_text_to_ids)
    
    # More pythonic
    source_sentences = [sentence for sentence in source_text.split('\n')]
    target_sentences = [sentence + ' <EOS>' for sentence in target_text.split('\n')]
    source_id_text= [[source_vocab_to_int[word] for word in sentence.split()] for sentence in source_sentences]
    target_id_text = [[target_vocab_to_int[word] for word in sentence.split()] for sentence in target_sentences]
    
    # print('source_id_text: {}'.format(source_id_text))
    # print('target_id_text: {}'.format(target_id_text))
    return source_id_text, target_id_text
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_text_to_ids(text_to_ids)
# In[4]:
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
helper.preprocess_and_save_data(source_path, target_path, text_to_ids)
# In[5]:
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
import numpy as np
import helper
import problem_unittests as tests
(source_int_text, target_int_text), (source_vocab_to_int, target_vocab_to_int), _ = helper.load_preprocess()
# In[6]:
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
from distutils.version import LooseVersion
import warnings
import tensorflow as tf
from tensorflow.python.layers.core import Dense
# Check TensorFlow Version
assert LooseVersion(tf.__version__) >= LooseVersion('1.1'), 'Please use TensorFlow version 1.1 or newer'
print('TensorFlow Version: {}'.format(tf.__version__))
# Check for a GPU
if not tf.test.gpu_device_name():
    warnings.warn('No GPU found. Please use a GPU to train your neural network.')
else:
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
# In[7]:
def model_inputs():
    """
    Create TF Placeholders for input, targets, learning rate, and lengths of source and target sequences.
    :return: Tuple (input, targets, learning rate, keep probability, target sequence length,
    max target sequence length, source sequence length)
    """
    # Implement Function
    # https://www.tensorflow.org/api_docs/python/tf/placeholder
    inputs = tf.placeholder(tf.int32, shape=(None, None), name='input')
    targets = tf.placeholder(tf.int32, shape=(None, None), name='target')
    learning_rate = tf.placeholder(tf.float32, name='learning_rate')
    keep_probability = tf.placeholder(tf.float32, name='keep_prob')
    target_sequence_length = tf.placeholder(tf.int32, shape=(None,), name='target_sequence_length') 
    max_target_sequence_length = tf.reduce_max(target_sequence_length, name='max_target_len')
    source_sequence_length = tf.placeholder(tf.int32, shape=(None,), name='source_sequence_length')
    
    return inputs, targets, learning_rate, keep_probability, target_sequence_length, max_target_sequence_length, source_sequence_length
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_model_inputs(model_inputs)
# In[8]:
def process_decoder_input(target_data, target_vocab_to_int, batch_size):
    """
    Preprocess target data for encoding
    :param target_data: Target Placehoder
    :param target_vocab_to_int: Dictionary to go from the target words to an id
    :param batch_size: Batch Size
    :return: Preprocessed target data
    """
    # Implement Function
    # Processes the input fed to the decoder
    last_word_id_from_each_batch = tf.strided_slice(target_data, [0, 0], [batch_size, -1], [1, 1])
    preprocessed_target_data = tf.concat([tf.fill([batch_size, 1], target_vocab_to_int['<GO>']), last_word_id_from_each_batch], 1)
    return preprocessed_target_data
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_process_encoding_input(process_decoder_input)
# In[9]:
from imp import reload
reload(tests)
def encoding_layer(rnn_inputs, rnn_size, num_layers, keep_prob, 
                   source_sequence_length, source_vocab_size, 
                   encoding_embedding_size):
    """
    Create encoding layer
    :param rnn_inputs: Inputs for the RNN
    :param rnn_size: RNN Size
    :param num_layers: Number of layers
    :param keep_prob: Dropout keep probability
    :param source_sequence_length: a list of the lengths of each sequence in the batch
    :param source_vocab_size: vocabulary size of source data
    :param encoding_embedding_size: embedding size of source data
    :return: tuple (RNN output, RNN state)
    """
    # Implement Function
    # Embed the encoder
    # https://www.tensorflow.org/api_docs/python/tf/contrib/layers/embed_sequence
    encod_embed_layer_input = tf.contrib.layers.embed_sequence(rnn_inputs, 
                                                               source_vocab_size, 
                                                               encoding_embedding_size)
                                                                # ids,
                                                                # vocab_size=None,
                                                                # embed_dim=None,
                                                                # unique=False,
                                                                # initializer=None,
                                                                # regularizer=None,
                                                                # trainable=True,
                                                                # scope=None,
                                                                # reuse=None
    # Construct a stacked tf.contrib.rnn.LSTMCell
    # https://www.tensorflow.org/api_docs/python/tf/contrib/rnn/LSTMCell
    def make_cell():
        lstm = tf.contrib.rnn.LSTMCell(rnn_size)
        # Wrapped in a tf.contrib.rnn.DropoutWrapper
        # https://www.tensorflow.org/api_docs/python/tf/contrib/rnn/DropoutWrapper
        dropout = tf.contrib.rnn.DropoutWrapper(cell=lstm, output_keep_prob=keep_prob)  # output_keep_prob=1.0,
        return dropout
    enc_cell = tf.contrib.rnn.MultiRNNCell([make_cell() for _ in range(num_layers)])
    
    # Pass cell and embedded input to tf.nn.dynamic_rnn()
    enc_output, enc_state = tf.nn.dynamic_rnn(enc_cell, encod_embed_layer_input, 
                                              sequence_length=source_sequence_length, 
                                              dtype=tf.float32)
    
    return enc_output, enc_state
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_encoding_layer(encoding_layer)
# In[10]:
def decoding_layer_train(encoder_state, dec_cell, dec_embed_input, 
                         target_sequence_length, max_summary_length, 
                         output_layer, keep_prob):
    """
    Create a decoding layer for training
    :param encoder_state: Encoder State
    :param dec_cell: Decoder RNN Cell
    :param dec_embed_input: Decoder embedded input
    :param target_sequence_length: The lengths of each sequence in the target batch
    :param max_summary_length: The length of the longest sequence in the batch
    :param output_layer: Function to apply the output layer
    :param keep_prob: Dropout keep probability
    :return: BasicDecoderOutput containing training logits and sample_id
    """
    # Implement Function
    # Helper for the training process allowing basic training decoder to read the inputs.
    # https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/TrainingHelper
    training_helper = tf.contrib.seq2seq.TrainingHelper(inputs=dec_embed_input,
                                                        sequence_length=target_sequence_length)  
                                                        # time_major=False, name=None)
    
    # Basic decoder
    # https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/BasicDecoder
    training_decoder = tf.contrib.seq2seq.BasicDecoder(cell=dec_cell,
                                                       helper=training_helper,
                                                       initial_state=encoder_state,
                                                       output_layer=output_layer) 
    
    # Obtain the decoder outputs from tf.contrib.seq2seq.dynamic_decode
    # Perform dynamic decoding using the basic training decoder
    training_decoder_output = tf.contrib.seq2seq.dynamic_decode(decoder=training_decoder,
                                                                impute_finished=True,
                                                                maximum_iterations=max_summary_length)[0]
                                                                # output_time_major=False,
                                                                # parallel_iterations=32,
                                                                # swap_memory=False,
                                                                # scope=None)[0]                                                                                 
    
    return training_decoder_output
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_decoding_layer_train(decoding_layer_train)
# In[11]:
def decoding_layer_infer(encoder_state, dec_cell, dec_embeddings, start_of_sequence_id,
                         end_of_sequence_id, max_target_sequence_length,
                         vocab_size, output_layer, batch_size, keep_prob):
    """
    Create a decoding layer for inference
    :param encoder_state: Encoder state
    :param dec_cell: Decoder RNN Cell
    :param dec_embeddings: Decoder embeddings
    :param start_of_sequence_id: GO ID
    :param end_of_sequence_id: EOS Id
    :param max_target_sequence_length: Maximum length of target sequences
    :param vocab_size: Size of decoder/target vocabulary
    :param decoding_scope: TenorFlow Variable Scope for decoding
    :param output_layer: Function to apply the output layer
    :param batch_size: Batch size
    :param keep_prob: Dropout keep probability
    :return: BasicDecoderOutput containing inference logits and sample_id
    """
    # Implement Function
    start_tokens = tf.tile(tf.constant([start_of_sequence_id], dtype=tf.int32), [batch_size], name='start_tokens')
                                        # start_of_sequence_id['<GO>']
    # Helper for the inference process.
    # https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/GreedyEmbeddingHelper
    inference_helper = tf.contrib.seq2seq.GreedyEmbeddingHelper(embedding=dec_embeddings,
                                                                start_tokens=start_tokens,
                                                                end_token=end_of_sequence_id)
                                                                # end_token=end_of_sequence_id['<EOS>'])
    # Basic decoder
    # https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/BasicDecoder
    inference_decoder = tf.contrib.seq2seq.BasicDecoder(cell=dec_cell,
                                                       helper=inference_helper,
                                                       initial_state=encoder_state,
                                                       output_layer=output_layer) 
    # Obtain the decoder outputs from tf.contrib.seq2seq.dynamic_decode
    # Perform dynamic decoding using the basic training decoder
    inference_decoder_output = tf.contrib.seq2seq.dynamic_decode(decoder=inference_decoder,
                                                                impute_finished=True,
                                                                maximum_iterations=max_target_sequence_length)[0]
                                                                # output_time_major=False,
                                                                # parallel_iterations=32,
                                                                # swap_memory=False,
                                                                # scope=None)[0]     
    
    return inference_decoder_output
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_decoding_layer_infer(decoding_layer_infer)
# In[12]:
def decoding_layer(dec_input, encoder_state,
                   target_sequence_length, max_target_sequence_length,
                   rnn_size,
                   num_layers, target_vocab_to_int, target_vocab_size,
                   batch_size, keep_prob, decoding_embedding_size):
    """
    Create decoding layer
    :param dec_input: Decoder input
    :param encoder_state: Encoder state
    :param target_sequence_length: The lengths of each sequence in the target batch
    :param max_target_sequence_length: Maximum length of target sequences
    :param rnn_size: RNN Size
    :param num_layers: Number of layers
    :param target_vocab_to_int: Dictionary to go from the target words to an id
    :param target_vocab_size: Size of target vocabulary
    :param batch_size: The size of the batch
    :param keep_prob: Dropout keep probability
    :param decoding_embedding_size: Decoding embedding size
    :return: Tuple of (Training BasicDecoderOutput, Inference BasicDecoderOutput)
    """
    # Implement Function
    # Embed the target sequences - based in part on Sequence to Sequence exercise
    dec_embeddings = tf.Variable(tf.random_uniform([target_vocab_size, decoding_embedding_size]))
    dec_embed_input = tf.nn.embedding_lookup(dec_embeddings, dec_input)
    
    # Construct the decoder LSTM cell - from encoding_layer above
    def make_cell(rnn_size):
        lstm = tf.contrib.rnn.LSTMCell(rnn_size)
        dropout = tf.contrib.rnn.DropoutWrapper(cell=lstm, output_keep_prob=keep_prob)  # output_keep_prob=1.0,
        return dropout
    dec_cell = tf.contrib.rnn.MultiRNNCell([make_cell(rnn_size) for _ in range(num_layers)])
    
    # Create an output layer to map the outputs of the decoder to the elements of our vocabulary
    output_layer = Dense(target_vocab_size, 
                         kernel_initializer = tf.truncated_normal_initializer(mean = 0.0, stddev=0.1))
    # Use the your decoding_layer_train
    with tf.variable_scope("decode") as decoding_scope:
        training_decoder_output = decoding_layer_train(encoder_state, 
                                                       dec_cell, 
                                                       dec_embed_input, 
                                                       target_sequence_length, 
                                                       max_target_sequence_length, 
                                                       output_layer, 
                                                       keep_prob)
        decoding_scope.reuse_variables()
    # Use your decoding_layer_infer
        inference_decoder_output = decoding_layer_infer(encoder_state,
                                                        dec_cell,
                                                        dec_embeddings,
                                                        target_vocab_to_int['<GO>'],
                                                        target_vocab_to_int['<EOS>'],
                                                        max_target_sequence_length,
                                                        target_vocab_size,
                                                        output_layer,
                                                        batch_size,
                                                        keep_prob)         
    return training_decoder_output, inference_decoder_output
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_decoding_layer(decoding_layer)
# In[13]:
def seq2seq_model(input_data, target_data, keep_prob, batch_size,
                  source_sequence_length, target_sequence_length,
                  max_target_sentence_length,
                  source_vocab_size, target_vocab_size,
                  enc_embedding_size, dec_embedding_size,
                  rnn_size, num_layers, target_vocab_to_int):
    """
    Build the Sequence-to-Sequence part of the neural network
    :param input_data: Input placeholder
    :param target_data: Target placeholder
    :param keep_prob: Dropout keep probability placeholder
    :param batch_size: Batch Size
    :param source_sequence_length: Sequence Lengths of source sequences in the batch
    :param target_sequence_length: Sequence Lengths of target sequences in the batch
    :param source_vocab_size: Source vocabulary size
    :param target_vocab_size: Target vocabulary size
    :param enc_embedding_size: Decoder embedding size
    :param dec_embedding_size: Encoder embedding size
    :param rnn_size: RNN Size
    :param num_layers: Number of layers
    :param target_vocab_to_int: Dictionary to go from the target words to an id
    :return: Tuple of (Training BasicDecoderOutput, Inference BasicDecoderOutput)
    """
    # Implement Function
    # Based in part on Sequence to Sequence exercise
    # Pass the input data through the encoder. We'll ignore the encoder output, but use the state
    _, enc_state = encoding_layer(input_data, 
                                  rnn_size, 
                                  num_layers,
                                  keep_prob,
                                  source_sequence_length,
                                  source_vocab_size, 
                                  enc_embedding_size)
    
    
    # Prepare the target sequences we'll feed to the decoder in training mode
    dec_input = process_decoder_input(target_data, target_vocab_to_int, batch_size)
    
    # Pass encoder state and decoder inputs to the decoders
    training_decoder_output, inference_decoder_output = decoding_layer(dec_input, 
                                                                       enc_state,
                                                                       target_sequence_length,
                                                                       max_target_sentence_length,
                                                                       rnn_size, 
                                                                       num_layers, 
                                                                       target_vocab_to_int, 
                                                                       target_vocab_size,
                                                                       batch_size, 
                                                                       keep_prob,
                                                                       dec_embedding_size)
    
    return training_decoder_output, inference_decoder_output
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_seq2seq_model(seq2seq_model)
# In[14]:
# Number of Epochs
epochs = 5  #10
# Batch Size
batch_size = 512  # 256
# RNN Size
rnn_size = 256  # 1024, 512
# Number of Layers
num_layers = 2
# Embedding Size
encoding_embedding_size = 220  # 200, 128, 256
decoding_embedding_size = 220  # 128, 256
# Learning Rate
learning_rate = 0.01  # 0.001
# Dropout Keep Probability
keep_probability = 0.5  # 0.7, 0.9
display_step = 67 # 100
# In[15]:
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
save_path = 'checkpoints/dev'
(source_int_text, target_int_text), (source_vocab_to_int, target_vocab_to_int), _ = helper.load_preprocess()
max_target_sentence_length = max([len(sentence) for sentence in source_int_text])
train_graph = tf.Graph()
with train_graph.as_default():
    input_data, targets, lr, keep_prob, target_sequence_length, max_target_sequence_length, source_sequence_length = model_inputs()
    #sequence_length = tf.placeholder_with_default(max_target_sentence_length, None, name='sequence_length')
    input_shape = tf.shape(input_data)
    train_logits, inference_logits = seq2seq_model(tf.reverse(input_data, [-1]),
                                                   targets,
                                                   keep_prob,
                                                   batch_size,
                                                   source_sequence_length,
                                                   target_sequence_length,
                                                   max_target_sequence_length,
                                                   len(source_vocab_to_int),
                                                   len(target_vocab_to_int),
                                                   encoding_embedding_size,
                                                   decoding_embedding_size,
                                                   rnn_size,
                                                   num_layers,
                                                   target_vocab_to_int)
    training_logits = tf.identity(train_logits.rnn_output, name='logits')
    inference_logits = tf.identity(inference_logits.sample_id, name='predictions')
    masks = tf.sequence_mask(target_sequence_length, max_target_sequence_length, dtype=tf.float32, name='masks')
    with tf.name_scope("optimization"):
        # Loss function
        cost = tf.contrib.seq2seq.sequence_loss(
            training_logits,
            targets,
            masks)
        # Optimizer
        optimizer = tf.train.AdamOptimizer(lr)
        # Gradient Clipping
        gradients = optimizer.compute_gradients(cost)
        capped_gradients = [(tf.clip_by_value(grad, -1., 1.), var) for grad, var in gradients if grad is not None]
        train_op = optimizer.apply_gradients(capped_gradients)
# In[16]:
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
def pad_sentence_batch(sentence_batch, pad_int):
    """Pad sentences with <PAD> so that each sentence of a batch has the same length"""
    max_sentence = max([len(sentence) for sentence in sentence_batch])
    return [sentence + [pad_int] * (max_sentence - len(sentence)) for sentence in sentence_batch]
def get_batches(sources, targets, batch_size, source_pad_int, target_pad_int):
    """Batch targets, sources, and the lengths of their sentences together"""
    for batch_i in range(0, len(sources)//batch_size):
        start_i = batch_i * batch_size
        # Slice the right amount for the batch
        sources_batch = sources[start_i:start_i + batch_size]
        targets_batch = targets[start_i:start_i + batch_size]
        # Pad
        pad_sources_batch = np.array(pad_sentence_batch(sources_batch, source_pad_int))
        pad_targets_batch = np.array(pad_sentence_batch(targets_batch, target_pad_int))
        # Need the lengths for the _lengths parameters
        pad_targets_lengths = []
        for target in pad_targets_batch:
            pad_targets_lengths.append(len(target))
        pad_source_lengths = []
        for source in pad_sources_batch:
            pad_source_lengths.append(len(source))
        yield pad_sources_batch, pad_targets_batch, pad_source_lengths, pad_targets_lengths
# In[17]:
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
def get_accuracy(target, logits):
    """
    Calculate accuracy
    """
    max_seq = max(target.shape[1], logits.shape[1])
    if max_seq - target.shape[1]:
        target = np.pad(
            target,
            [(0,0),(0,max_seq - target.shape[1])],
            'constant')
    if max_seq - logits.shape[1]:
        logits = np.pad(
            logits,
            [(0,0),(0,max_seq - logits.shape[1])],
            'constant')
    return np.mean(np.equal(target, logits))
# Split data to training and validation sets
train_source = source_int_text[batch_size:]
train_target = target_int_text[batch_size:]
valid_source = source_int_text[:batch_size]
valid_target = target_int_text[:batch_size]
(valid_sources_batch, valid_targets_batch, valid_sources_lengths, valid_targets_lengths ) = next(get_batches(valid_source,
                                                                                                             valid_target,
                                                                                                             batch_size,
                                                                                                             source_vocab_to_int['<PAD>'],
                                                                                                             target_vocab_to_int['<PAD>']))                                                                                                  
with tf.Session(graph=train_graph) as sess:
    sess.run(tf.global_variables_initializer())
    for epoch_i in range(epochs):
        for batch_i, (source_batch, target_batch, sources_lengths, targets_lengths) in enumerate(
                get_batches(train_source, train_target, batch_size,
                            source_vocab_to_int['<PAD>'],
                            target_vocab_to_int['<PAD>'])):
            _, loss = sess.run(
                [train_op, cost],
                {input_data: source_batch,
                 targets: target_batch,
                 lr: learning_rate,
                 target_sequence_length: targets_lengths,
                 source_sequence_length: sources_lengths,
                 keep_prob: keep_probability})
            if batch_i % display_step == 0 and batch_i > 0:
                batch_train_logits = sess.run(
                    inference_logits,
                    {input_data: source_batch,
                     source_sequence_length: sources_lengths,
                     target_sequence_length: targets_lengths,
                     keep_prob: 1.0})
                batch_valid_logits = sess.run(
                    inference_logits,
                    {input_data: valid_sources_batch,
                     source_sequence_length: valid_sources_lengths,
                     target_sequence_length: valid_targets_lengths,
                     keep_prob: 1.0})
                train_acc = get_accuracy(target_batch, batch_train_logits)
                valid_acc = get_accuracy(valid_targets_batch, batch_valid_logits)
                print('Epoch {:>3} Batch {:>4}/{} - Train Accuracy: {:>6.4f}, Validation Accuracy: {:>6.4f}, Loss: {:>6.4f}'
                      .format(epoch_i, batch_i, len(source_int_text) // batch_size, train_acc, valid_acc, loss))
    # Save Model
    saver = tf.train.Saver()
    saver.save(sess, save_path)
    print('Model Trained and Saved')
# In[18]:
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
# Save parameters for checkpoint
helper.save_params(save_path)
# In[19]:
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
import tensorflow as tf
import numpy as np
import helper
import problem_unittests as tests
_, (source_vocab_to_int, target_vocab_to_int), (source_int_to_vocab, target_int_to_vocab) = helper.load_preprocess()
load_path = helper.load_params()
# In[20]:
def sentence_to_seq(sentence, vocab_to_int):
    """
    Convert a sentence to a sequence of ids
    :param sentence: String
    :param vocab_to_int: Dictionary to go from the words to an id
    :return: List of word ids
    """
    # Implement Function
    # Convert the sentence to lowercase
    sentence_to_lowercase = sentence.lower()
    # Convert words not in the vocabulary, to the <UNK> word id
    words_not_in_vocab = vocab_to_int['<UNK>']
    # Convert words into ids using vocab_to_int
    return [vocab_to_int.get(word, words_not_in_vocab) for word in sentence_to_lowercase.split()]
"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_sentence_to_seq(sentence_to_seq)
# In[21]:
translate_sentence = 'he saw a old yellow truck .'
"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
translate_sentence = sentence_to_seq(translate_sentence, source_vocab_to_int)
loaded_graph = tf.Graph()
with tf.Session(graph=loaded_graph) as sess:
    # Load saved model
    loader = tf.train.import_meta_graph(load_path + '.meta')
    loader.restore(sess, load_path)
    input_data = loaded_graph.get_tensor_by_name('input:0')
    logits = loaded_graph.get_tensor_by_name('predictions:0')
    target_sequence_length = loaded_graph.get_tensor_by_name('target_sequence_length:0')
    source_sequence_length = loaded_graph.get_tensor_by_name('source_sequence_length:0')
    keep_prob = loaded_graph.get_tensor_by_name('keep_prob:0')
    translate_logits = sess.run(logits, {input_data: [translate_sentence]*batch_size,
                                         target_sequence_length: [len(translate_sentence)*2]*batch_size,
                                         source_sequence_length: [len(translate_sentence)]*batch_size,
                                         keep_prob: 1.0})[0]
print('Input')
print('  Word Ids:      {}'.format([i for i in translate_sentence]))
print('  English Words: {}'.format([source_int_to_vocab[i] for i in translate_sentence]))
print('\nPrediction')
print('  Word Ids:      {}'.format([i for i in translate_logits]))
print('  French Words: {}'.format(" ".join([target_int_to_vocab[i] for i in translate_logits])))