import pandas as pd
import numpy as np

# Cargar los datos de entrenamiento
datos_entrenamiento = pd.read_csv('train_one_hot.csv')

# Cargar los datos de testeo
datos_testeo = pd.read_csv('test_one_hot.csv')

# Definir la función de distancia de Hamming
def distancia_hamming(x, y):
    return np.sum(x != y)

# Obtener una observacion del dataset de testeo
observacion_testeo = datos_testeo.iloc[0]

# Excluir 'PassengerId' y 'Survived' del conjunto de datos de entrenamiento
X_entrenamiento = datos_entrenamiento.drop(columns=['PassengerId', 'Survived'])

# Excluir 'PassengerId' de la observacion de testeo (asumiendo que 'Survived' no está en testeo)
X_observacion_testeo = observacion_testeo.drop(labels=['PassengerId'])

# Calcular la distancia de Hamming
distancias = X_entrenamiento.apply(
    lambda row: distancia_hamming(row.values, X_observacion_testeo.values), axis=1)

# Crear el DataFrame con las distancias y las clases
df_distancias = pd.DataFrame({
    'Distancia': distancias,
    'Sobrevivio': datos_entrenamiento['Survived']
})
print("Distancias: \n")
print(df_distancias)


# Ordenar el DataFrame por distancia
df_distancias = df_distancias.sort_values(by='Distancia', ascending=True)
print("Distancias Ordenadas: \n")
print(df_distancias)


# Obtener el total de observaciones del dataset de entrenamiento
total_observaciones = df_distancias.shape[0]

# Calcular los vecinos usando el logaritmo
k = int(np.log(total_observaciones))

# Obtener los k vecinos más cercanos
vecinos = df_distancias.head(k)

print("Vecinos: \n")
print(vecinos)

# Calcula la probabilidad para cada clase
class_probabilities = vecinos['Sobrevivio'].value_counts()

# Calcular las probabilidades
vector_clase = []
vector_probabilidad = []
print("Probabilidades por clase:")
for clase, conteo in class_probabilities.items():
    vector_clase.append(clase)
    vector_probabilidad.append(conteo / k)

df_probabilidad = pd.DataFrame({
    'Clase': vector_clase,
    'Probabilidad': vector_probabilidad
})
print(df_probabilidad)

print("Clase con mayor probabilidad:", df_probabilidad.loc[df_probabilidad['Probabilidad'].idxmax(), 'Clase'])
