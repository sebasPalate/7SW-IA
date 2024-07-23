import pandas as pd
import numpy as np
from math import log
from sklearn.model_selection import train_test_split
import joblib

# Carga los datos desde el archivo .csv
datos = pd.read_csv('datasetImg64x64.csv')

# Separa las etiquetas de las imágenes
y = datos.iloc[:, 0].values
X = datos.iloc[:, 1:].values

# Convierte las etiquetas a 1 si es 7, 0 si no lo es
y = np.where(y == 7, 1, 0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def calcular_entropia(y):
    clases = set(y)
    entropia = 0
    for clase in clases:
        p = sum([1 for valor in y if valor == clase]) / len(y)
        entropia -= p * log2(p)
    return entropia

def calcular_ganancia_informacion(X, y, atributo):
    entropia_inicial = calcular_entropia(y)
    valores = set(X[:, atributo])
    entropia_final = 0
    for valor in valores:
        y_subconjunto = y[X[:, atributo] == valor]
        entropia_final += len(y_subconjunto) / len(y) * calcular_entropia(y_subconjunto)
    ganancia_informacion = entropia_inicial - entropia_final
    return ganancia_informacion

def encontrar_mejor_atributo(X, y):
    mejor_ganancia_informacion = -1
    mejor_atributo = -1
    for atributo in range(X.shape[1]):
        ganancia_informacion = calcular_ganancia_informacion(X, y, atributo)
        if ganancia_informacion > mejor_ganancia_informacion:
            mejor_ganancia_informacion = ganancia_informacion
            mejor_atributo = atributo
    return mejor_atributo

def construir_arbol(X, y, profundidad_maxima, profundidad_actual=0):
    if profundidad_actual == profundidad_maxima or calcular_entropia(y) == 0:
        return y[0]
    mejor_atributo = encontrar_mejor_atributo(X, y)
    arbol = {mejor_atributo: {}}
    valores = set(X[:, mejor_atributo])
    for valor in valores:
        X_subconjunto = X[X[:, mejor_atributo] == valor]
        y_subconjunto = y[X[:, mejor_atributo] == valor]
        arbol[mejor_atributo][valor] = construir_arbol(X_subconjunto, y_subconjunto, profundidad_maxima, profundidad_actual + 1)
    return arbol

def predecir(arbol, x):
    for atributo in arbol.keys():
        valor = x[atributo]
        if valor in arbol[atributo].keys():
            subarbol = arbol[atributo][valor]
            if type(subarbol) is dict:
                return predecir(subarbol, x)
            else:
                return subarbol
    return 0 # Si no se puede predecir, regresa 0

def log2(x):
    if x == 0:
        return 0
    return x * log(x) / log(2)

# Construye el árbol de decisión
arbol = construir_arbol(X_train, y_train, 100)

# Haz predicciones en el conjunto de prueba
y_pred = [predecir(arbol, x) for x in X_test]

# Calcula el número de errores
num_errores = (y_test != y_pred).sum()

# Calcula la tasa de error de clasificación
tasa_error = num_errores / len(y_test)

print('Tasa de error de prueba:', tasa_error)

print('Precisión:', 1 - tasa_error)
# Guarda el modelo
joblib.dump(arbol, 'modelos/modelo_arbol_decision_manual.pkl')