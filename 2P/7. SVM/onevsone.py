import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump
import time
import numpy as np
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import SVC
import os

def cargar_datos(ruta_train, ruta_test):
    try:
        df_train = pd.read_csv(ruta_train)
        df_test = pd.read_csv(ruta_test)
        return df_train, df_test
    except FileNotFoundError as e:
        print(f'Error al leer los archivos CSV: {e}')
        exit()

def separar_caracteristicas_etiquetas(df):
    y = df['label'].astype(int)
    X = df.drop('label', axis=1)
    return X, y

def entrenar_modelo(X_train, y_train, kernel='linear', C=1.0, random_state=42):
    clf = OneVsOneClassifier(SVC(kernel=kernel, C=C, random_state=random_state))
    start_time = time.time()
    clf.fit(X_train, y_train)
    end_time = time.time()
    training_time = end_time - start_time
    print(f'Tiempo de entrenamiento: {training_time:.2f} segundos')
    return clf, training_time

def evaluar_modelo(clf, X_test, y_test):
    start_time = time.time()
    predictions = clf.predict(X_test)
    end_time = time.time()
    prediction_time = end_time - start_time
    print(f'Tiempo de predicción: {prediction_time:.2f} segundos')
    
    accuracy = accuracy_score(y_test, predictions)
    print(f'Precisión del clasificador SVM: {accuracy:.4f}')
    
    print('Classification Report:')
    print(classification_report(y_test, predictions))
    
    return accuracy, prediction_time

def guardar_modelo(clf, ruta_modelo):
    os.makedirs(os.path.dirname(ruta_modelo), exist_ok=True)
    dump(clf, ruta_modelo)

# Ruta de los datasets
ruta_train = 'fashionDataset/fashion-mnist_train.csv'
ruta_test = 'fashionDataset/fashion-mnist_test.csv'

# Cargar los datos
df_train, df_test = cargar_datos(ruta_train, ruta_test)

# Separar las etiquetas de las características
X_train, y_train = separar_caracteristicas_etiquetas(df_train)
X_test, y_test = separar_caracteristicas_etiquetas(df_test)

# Entrenar el modelo
clf, training_time = entrenar_modelo(X_train, y_train)

# Evaluar el modelo
accuracy, prediction_time = evaluar_modelo(clf, X_test, y_test)

# Guardar el modelo
ruta_modelo = 'modelo/onevsone.joblib'
guardar_modelo(clf, ruta_modelo)
