import numpy as np
import pandas as pd
# pd.set_option('html', True)
from IPython.core.display import Image
Image('https://pbs.twimg.com/media/C2U2-UHWIAADYQK.jpg')
Image('https://img.elcomercio.pe/files/article_content_ec_fotos/uploads/2017/03/22/58d2059f5e1c1.jpeg')
import tensorflow as tf
genero = tf.feature_column.categorical_column_with_vocabulary_list(
"genero", ["Masculino", "Femenino"]
)
educacion = tf.feature_column.categorical_column_with_vocabulary_list(
"educacion", [
    "Bachiller", "Maestria", "doctorado"
]
)
estado_marital = tf.feature_column.categorical_column_with_vocabulary_list(
"estado_marital", [
    "Casado", "Soltero", "Divorciado"
]
)
relaciones = tf.feature_column.categorical_column_with_vocabulary_list(
"relaciones", [
    "Esposo", "Primo", "Tio", "Hermano"
]
)
trabajos= tf.feature_column.categorical_column_with_vocabulary_list(
"trabajos", [
    "Ingeniero", "Doctor", "Obrero"
]
)
ocupacion = tf.feature_column.categorical_column_with_hash_bucket(
"ocupacion", hash_bucket_size=1000
)
native_country = tf.feature_column.categorical_column_with_hash_bucket(
    "native_country", hash_bucket_size=1000)
# Continuous base columns.
edad = tf.feature_column.numeric_column("edad")
num_education = tf.feature_column.numeric_column("num_educacion")
#tranforaciones
cubos_edad = tf.feature_column.bucketized_column(
edad, boundaries = [18, 25, 30]
)
base_columns = [
    genero, educacion, ocupacion, trabajos, relaciones,
    cu,
]