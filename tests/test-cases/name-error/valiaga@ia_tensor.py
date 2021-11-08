#!/usr/bin/env python
# coding: utf-8
# In[11]:
import numpy as np
import pandas as pd
# pd.set_option('html', True)
# In[12]:
from IPython.core.display import Image
# In[17]:
Image('https://pbs.twimg.com/media/C2U2-UHWIAADYQK.jpg')
# In[16]:
Image('https://img.elcomercio.pe/files/article_content_ec_fotos/uploads/2017/03/22/58d2059f5e1c1.jpeg')
# In[18]:
import tensorflow as tf
# In[19]:
genero = tf.feature_column.categorical_column_with_vocabulary_list(
"genero", ["Masculino", "Femenino"]
)
# In[20]:
educacion = tf.feature_column.categorical_column_with_vocabulary_list(
"educacion", [
    "Bachiller", "Maestria", "doctorado"
]
)
# In[22]:
estado_marital = tf.feature_column.categorical_column_with_vocabulary_list(
"estado_marital", [
    "Casado", "Soltero", "Divorciado"
]
)
# In[25]:
relaciones = tf.feature_column.categorical_column_with_vocabulary_list(
"relaciones", [
    "Esposo", "Primo", "Tio", "Hermano"
]
)
# In[26]:
trabajos= tf.feature_column.categorical_column_with_vocabulary_list(
"trabajos", [
    "Ingeniero", "Doctor", "Obrero"
]
)
# In[27]:
ocupacion = tf.feature_column.categorical_column_with_hash_bucket(
"ocupacion", hash_bucket_size=1000
)
# In[28]:
native_country = tf.feature_column.categorical_column_with_hash_bucket(
    "native_country", hash_bucket_size=1000)
# In[29]:
# Continuous base columns.
edad = tf.feature_column.numeric_column("edad")
num_education = tf.feature_column.numeric_column("num_educacion")
# In[31]:
#tranforaciones
cubos_edad = tf.feature_column.bucketized_column(
edad, boundaries = [18, 25, 30]
)
# In[32]:
base_columns = [
    genero, educacion, ocupacion, trabajos, relaciones,
    cu,
]