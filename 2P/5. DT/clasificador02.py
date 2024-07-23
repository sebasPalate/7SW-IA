import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
import joblib

# Cargar los datos desde el archivo .csv
datos = pd.read_csv('datasetImg64x64.csv')

# Separar las etiquetas de las características
etiquetas = datos.iloc[:, 0].values
caracteristicas = datos.iloc[:, 1:].values

# Convertir las etiquetas a 1 si es 7, 0 si no lo es
etiquetas = np.where(etiquetas == 7, 1, 0)

# Dividir los datos en conjunto de entrenamiento y prueba
caracteristicas_entrenamiento, caracteristicas_prueba, etiquetas_entrenamiento, etiquetas_pruebas = train_test_split(
    caracteristicas, etiquetas, test_size=0.2, random_state=42)  # random_state para reproducibilidad

# Inicializar y entrenar el modelo de árbol de decisión
arbol_decision = DecisionTreeClassifier(
    criterion="entropy", max_depth=150, random_state=42)

# Entrenar el modelo
arbol = arbol_decision.fit(
    caracteristicas_entrenamiento, etiquetas_entrenamiento)

# Evaluar la precisión del modelo
accuracy = arbol.score(caracteristicas_prueba, etiquetas_pruebas)
print('Accuracy:', round(accuracy, 4)*100, "%")

# Calcular la tasa de error de clasificación
etiqueta_predicha = arbol.predict(caracteristicas_prueba)
num_errores = (etiquetas_pruebas != etiqueta_predicha).sum()
tasa_error = num_errores / len(etiquetas_pruebas)
print('Tasa de error de prueba:', tasa_error)

# Guardar el modelo
joblib.dump(arbol, 'modelos/modelo_arbol_decision.pkl')

# Exportar el árbol a un archivo .dot
dot_data = export_graphviz(arbol, out_file=None,
                           feature_names=datos.columns[1:],
                           class_names=['Not 7', '7'],
                           filled=True, rounded=True,
                           special_characters=True)

# Visualizar el árbol usando graphviz
graph = graphviz.Source(dot_data)

# Esto guardará el árbol como arbol_decision.pdf
graph.render("arbol_decision")

# Obtener la información del árbol entrenado
nodos = arbol.tree_

# Calcular la ganancia de información del nodo raíz
def calcular_entropia(p):
    return -p * np.log2(p) if p != 0 else 0

# Entropía del nodo padre (nodo raíz)
proba_padre = nodos.value[0][0] / np.sum(nodos.value[0][0])
print("\nProbabilidad del Padre: ", proba_padre)
entropia_padre = sum([calcular_entropia(p) for p in proba_padre])
print(f'Entropía del nodo padre: {entropia_padre:.4f}')

# Ganancia de información del nodo padre
nodo_izq = nodos.children_left[0]
nodo_der = nodos.children_right[0]

# Entropía del nodo izquierdo
proba_izq = nodos.value[nodo_izq][0] / np.sum(nodos.value[nodo_izq][0])
print("\nProbabilidad del Nodo Izquierdo: ", proba_izq)
entropia_izq = sum([calcular_entropia(p) for p in proba_izq])
print(f'Entropía del nodo izquierdo: {entropia_izq:.4f}')

# Entropía del nodo derecho
proba_der = nodos.value[nodo_der][0] / np.sum(nodos.value[nodo_der][0])
print("\nProbabilidad del Nodo Derecho: ", proba_der)
entropia_der = sum([calcular_entropia(p) for p in proba_der])
print(f'Entropía del nodo derecho: {entropia_der:.4f}')

# Ganancia de información
p_izq = np.sum(nodos.value[nodo_izq][0]) / np.sum(nodos.value[0][0])
p_der = np.sum(nodos.value[nodo_der][0]) / np.sum(nodos.value[0][0])
ganancia_informacion = entropia_padre - (p_izq * entropia_izq + p_der * entropia_der)

print(f'\nGanancia de información del nodo padre: {ganancia_informacion:.4f}')
