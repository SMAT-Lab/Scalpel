#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# In[2]:
data_path = 'bike-sharing-dataset/hour.csv'
rides = pd.read_csv(data_path)
rides.head()
# In[3]:
rides[:24*10].plot(x='dteday', y='cnt')
# In[4]:
dummy_fields = ['season', 'weathersit', 'mnth', 'hr', 'weekday']
for field in dummy_fields:
    dummies = pd.get_dummies(rides[field], prefix=field)
    rides = pd.concat([rides, dummies], axis=1)
fields_to_drop = ['instant', 'dteday', 'season', 'weathersit', 'mnth', 'hr', 'weekday', 'atemp', 'workingday']
data = rides.drop(fields_to_drop, axis=1)
data.head()
# In[5]:
quant_features = ['casual', 'registered', 'cnt', 'temp', 'hum', 'windspeed']
# Guardar los factores de escala en un diccionario para que podamos usarlas más tarde
scaled_features = {}
for quant in quant_features:
    mean, std = data[quant].mean(), data[quant].std()
    scaled_features[quant] = [mean, std]
    data.loc[:, quant] = (data[quant] - mean) / std
data.head()
# In[6]:
# Guardar datos de aproximadamente los últimos 21 días
test_data = data[-21*24:]
# Eliminar los datos de prueba del conjunto de datos
data = data[:-21*24]
# Separar los datos en features (X) y targets(y)
target_fields = ['cnt', 'casual', 'registered']
features, targets = data.drop(target_fields, axis=1), data[target_fields]
test_features, test_targets = test_data.drop(target_fields, axis=1), test_data[target_fields]
# In[7]:
# Hold out the last 60 days or so of the remaining data as a validation set
hold = 24 * 60
train_features, train_targets = features[:-hold], targets[:-hold]
val_features, val_targets = features[-hold:], targets[-hold:]
# In[8]:
train_features.shape
# In[9]:
train_features[:5]
# In[10]:
val_features.shape
# In[11]:
val_features[:5]
# In[12]:
test_features.shape
# In[13]:
test_features[:5]
# In[14]:
class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Usar la misma semilla para depurar con facilidad
        np.random.seed(21)
        
        # Guardar el número de nodos en las capas de entrada, oculta y salida
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        
        # Guardar la tasa de aprendizaje
        self.learning_rate = learning_rate
        
        # Inicializar los pesos
        self.weights_input_to_hidden = np.random.normal(0.0, self.input_nodes ** -0.5,
                                                        (self.input_nodes, self.hidden_nodes))
        self.weights_hidden_to_output = np.random.normal(0.0, self.hidden_nodes ** -0.5,
                                                        (self.hidden_nodes, self.output_nodes))
        
        # Configurar la función de activación
        self.activation_function = lambda x : 1 / (1 + np.exp(-x))
    
    def train(self, features, targets):
        ''' Entrenar la red en lotes de features y targets. 
        
            Argumentos
            ---------
            features: arreglo 2D, cada fila es un registro de los datos, cada columna es una característica (feature)
            targets: arreglo 1D de valores objetivos
        '''
        n_records = features.shape[0]
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)
        
        for X, y in zip(features, targets):
            hidden_outputs, final_outputs = self.feedforward(X)
            delta_weights_i_h, delta_weights_h_o = self.backpropagation(final_outputs, hidden_outputs, X, y, 
                                                                        delta_weights_i_h, delta_weights_h_o)
        
        self.update_weights(delta_weights_i_h, delta_weights_h_o, n_records)
    
    def feedforward(self, X):
        ''' Feedforward
         
            Argumentos
            ---------
            X: lote de features
        '''
        # Capa oculta
        hidden_inputs = np.dot(X, self.weights_input_to_hidden) # Señales que entran a la capa oculta
        hidden_outputs = self.activation_function(hidden_inputs) # Señales que salen de la capa oculta
        
        # Capa de salida
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) # Señales que entran a la capa de salida
        final_outputs = final_inputs # Señales que salen de la capa de salida
        
        return hidden_outputs, final_outputs
    
    def backpropagation(self, final_outputs, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):
        ''' Backpropagation
         
            Argumentos
            ---------
            final_outputs: salidas del proceso feedforward
            y: lote de targets (es decir, etiquetas)
            delta_weights_i_h: cambio en pesos de la capa de entrada a la oculta
            delta_weights_h_o: cambio en pesos de la capa oculta a la de salida
        '''
        # Error en la salida
        error = y - final_outputs
        
        # Contribución al error por la capa oculta
        hidden_error = np.dot(self.weights_hidden_to_output, error)
        
        # Términos de error usados en backpropagation
        output_error_term = error * 1
        hidden_error_term = hidden_error * hidden_outputs * (1 - hidden_outputs)
        
        # Cambios en pesos
        delta_weights_i_h += hidden_error_term * X[:, None]
        delta_weights_h_o += output_error_term * hidden_outputs[:, None]
        
        return delta_weights_i_h, delta_weights_h_o
    def update_weights(self, delta_weights_i_h, delta_weights_h_o, n_records):
        ''' Actualizar pesos en cada paso de descenso de gradiente
         
            Argumentos
            ---------
            delta_weights_i_h: cambio en pesos de la capa de entrada a la oculta
            delta_weights_h_o: cambio en pesos de la capa oculta a la de salida
            n_records: número de registros
        '''
        self.weights_input_to_hidden += self.learning_rate * delta_weights_i_h / n_records
        self.weights_hidden_to_output += self.learning_rate * delta_weights_h_o / n_records
    
    def run(self, features):
        ''' Ejecutar el proceso feedforward a través de la red con ciertos datos de entrada
        
            Argumentos
            ---------
            features: arreglo 1D de características
        '''
        # Capa oculta
        hidden_inputs = np.dot(features, self.weights_input_to_hidden) # Señales que entran a la capa oculta
        hidden_outputs = self.activation_function(hidden_inputs) # Señales que salen de la capa oculta
        
        # Capa de salida
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) # Señales que entran a la capa de salida
        final_outputs = final_inputs # Señales que salen de la capa de salida
        
        return final_outputs
# In[15]:
def MSE(y, Y):
    return np.mean((y-Y)**2)
# In[16]:
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
    # Pruebas unitarias para la carga de datos
    ##########
    
    def test_data_path(self):
        # Probar que la ruta del archivo al conjunto de datos no se ha alterado
        self.assertTrue(data_path.lower() == 'bike-sharing-dataset/hour.csv')
        
    def test_data_loaded(self):
        # Probar que se ha cargado el frame de datos
        self.assertTrue(isinstance(rides, pd.DataFrame))
    
    ##########
    # Pruebas unitarias para la funcionalidad de la red
    ##########
    def test_activation(self):
        network = NeuralNetwork(3, 2, 1, 0.5)
        # Probar que la función de activación es la función sigmoide
        self.assertTrue(np.all(network.activation_function(0.5) == 1 / (1 + np.exp(-0.5))))
    def test_train(self):
        # Probar que los pesos se actualizan de manera correcta al entrenar la red
        network = NeuralNetwork(3, 2, 1, 0.5)
        network.weights_input_to_hidden = test_w_i_h.copy()
        network.weights_hidden_to_output = test_w_h_o.copy()
        
        network.train(inputs, targets)
        
        self.assertTrue(np.allclose(network.weights_input_to_hidden,
                                    np.array([[ 0.10562014, -0.20185996], 
                                              [0.39775194, 0.50074398], 
                                              [-0.29887597, 0.19962801]])))
        self.assertTrue(np.allclose(network.weights_hidden_to_output, 
                                    np.array([[ 0.37275328], 
                                              [-0.03172939]])))
    def test_run(self):
        # Probar la correcta implementación del método run
        network = NeuralNetwork(3, 2, 1, 0.5)
        network.weights_input_to_hidden = test_w_i_h.copy()
        network.weights_hidden_to_output = test_w_h_o.copy()
        self.assertTrue(np.allclose(network.run(inputs), 0.09998924))
suite = unittest.TestLoader().loadTestsFromModule(TestMethods())
unittest.TextTestRunner().run(suite)
# In[17]:
# Ajustar hiperparámetros
iterations = 2000
learning_rate = 1
hidden_nodes = 8
output_nodes = 1
# In[18]:
import sys
input_nodes = train_features.shape[1]
network = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
losses = {'train':[], 'validation':[]}
# Usar la misma semilla para depurar con facilidad
np.random.seed(21)
for ii in range(iterations):
    # Escoger un lote de 128 registros de manera aleatoria del conjunto de entrenamiento
    batch = np.random.choice(train_features.index, size=128)
    X, y = train_features.iloc[batch].values, train_targets.iloc[batch]['cnt']
                             
    network.train(X, y)
    
    # Imprimir el progreso del proceso de entrenamiento
    train_loss = MSE(network.run(train_features).T, train_targets['cnt'].values)
    val_loss = MSE(network.run(val_features).T, val_targets['cnt'].values)
    
    sys.stdout.write("\rProgress: {:2.1f}".format(100 * ii/float(iterations))                      + "% ... Training loss: " + str(train_loss)[:5]                      + " ... Validation loss: " + str(val_loss)[:5])
    sys.stdout.flush()
    
    losses['train'].append(train_loss)
    losses['validation'].append(val_loss)
# In[19]:
plt.plot(losses['train'], label='Training loss')
plt.plot(losses['validation'], label='Validation loss')
plt.legend()
_ = plt.ylim()
# In[20]:
fig, ax = plt.subplots(figsize=(8,4))
# Realizar predicciones en los datos de prueba
mean, std = scaled_features['cnt']
predictions = network.run(test_features).T * std + mean
# Configurar gráfica
ax.plot(predictions[0], label='Prediction')
ax.plot((test_targets['cnt'] * std + mean).values, label='Data')
ax.set_xlim(right=len(predictions))
ax.legend()
# Configurar las fechas a mostrar en la gráfica
dates = pd.to_datetime(rides.iloc[test_data.index]['dteday'])
dates = dates.apply(lambda d: d.strftime('%b %d'))
ax.set_xticks(np.arange(len(dates))[12::24])
_ = ax.set_xticklabels(dates[12::24], rotation=45)