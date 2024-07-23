import pandas as pd
import numpy as np

# Cargar los datos de entrenamiento
datos_entrenamiento = pd.read_csv('train_one_hot.csv')

# Cargar los datos de testeo
datos_testeo = pd.read_csv('test_one_hot.csv')

# Definir la función de distancia de Hamming
def distancia_hamming(x, y):
    return np.sum(x != y)

# Excluir 'PassengerId' y 'Survived' del conjunto de datos de entrenamiento
X_entrenamiento = datos_entrenamiento.drop(columns=['PassengerId', 'Survived'])

# Inicializar contadores para calcular accuracy y tasa de error
correct_predictions = 0
total_observations = datos_testeo.shape[0]

# Iterar sobre cada observación en el dataset de testeo
for i in range(total_observations):
    # Guardar la clase real en una variable separada
    actual_class = datos_testeo.loc[i, 'Survived']

    # Eliminar 'PassengerId' y 'Survived' de la observación de prueba
    X_observacion_testeo = datos_testeo.drop(columns=['PassengerId', 'Survived']).iloc[i]

    # Calcular la distancia de Hamming
    distancias = X_entrenamiento.apply(
        lambda row: distancia_hamming(row.values, X_observacion_testeo.values), axis=1)

    # Crear el DataFrame con las distancias y las clases
    df_distancias = pd.DataFrame({
        'Distancia': distancias,
        'Sobrevivio': datos_entrenamiento['Survived']
    })

    # Ordenar el DataFrame por distancia
    df_distancias = df_distancias.sort_values(by='Distancia', ascending=True)

    # Calcular los vecinos usando el logaritmo
    k = int(np.log(total_observations))

    # Obtener los k vecinos más cercanos
    vecinos = df_distancias.head(k)

    # Calcula la probabilidad para cada clase
    class_probabilities = vecinos['Sobrevivio'].value_counts()

    # Predicción: la clase con mayor probabilidad
    predicted_class = class_probabilities.idxmax()

    # Comparar con la clase real y actualizar contadores
    if predicted_class == actual_class:
        correct_predictions += 1

# Calcular accuracy y tasa de error
accuracy = correct_predictions / total_observations
error_rate = 1 - accuracy

print(f"Accuracy: {accuracy:.4f}")
print(f"Tasa de error: {error_rate:.4f}")