import numpy as np
import cv2
from joblib import load
import matplotlib.pyplot as plt

# Función para preprocesar la imagen


def preprocess_image(image_path):
    # Leer la imagen con OpenCV
    # Convertir a escala de grises
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    img = cv2.resize(img, (28, 28))  # Redimensionar a 28x28 píxeles

    # Convertir la imagen a un array numpy y aplanarla
    img_flattened = img.flatten()

    return img_flattened


# Ruta a la nueva imagen que deseas clasificar
image_path = 'imagenes/camiseta01.jpg'

# Cargar el modelo entrenado
clf = load('modelo/onevsone.joblib')

# Preprocesar la imagen
img_preprocessed = preprocess_image(image_path)

# Realizar la predicción
prediction = clf.predict([img_preprocessed])

# Mapear la predicción a la etiqueta correspondiente
labels = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress',
          'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
predicted_label = labels[prediction[0]]

print(f'La imagen ha sido clasificada como: {predicted_label}')

# Mostrar la imagen
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
plt.title(f'Predicción: {predicted_label}')
plt.axis('off')
plt.show()
