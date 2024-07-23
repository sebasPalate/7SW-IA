import cv2
import numpy as np
import joblib


# Carga el modelo
clf = joblib.load('modelos/modelo_arbol_decision.pkl')

# Leer la imagen a color
image_bgr = cv2.imread('imagenes/numero7-02.jpg', cv2.IMREAD_COLOR)

# Convertir la imagen de BGR (OpenCV) a RGB
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

# Convertir la imagen a escala de grises
image_gry = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

# Umbralización utilizando el método de Otsu
""" _, image_bin = cv2.threshold(
    image_gry, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) """
_, image_bin = cv2.threshold(
    image_gry, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Mostrar la imagen binarizada
cv2.imshow('Imagen binarizada', image_bin)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Redimensiona la imagen a 64x64
img_rz = cv2.resize(image_bin, (64, 64))

# Convierte la imagen a un array de numpy y aplánala
img_data = np.array(img_rz).flatten()

# Usa el modelo para predecir la clase de la imagen
prediccion = clf.predict([img_data])

# Imprimir la predicción
print('Predicción:', 'Es un 7' if prediccion.item() == 1 else 'No es un 7')
