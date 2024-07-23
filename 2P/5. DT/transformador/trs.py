import os
import cv2
import csv

# Especifica la carpeta principal que contiene las subcarpetas para cada número
carpeta_principal = 'DATA'

# Abre o crea el archivo CSV para escribir los datos
archivo_csv = open('datasetImg64x64.csv', 'w', newline='')

# Tamaño deseado para las imágenes redimensionadas
nuevo_tamano = (64, 64)

# Inicializa el escritor CSV
csv_writer = csv.writer(archivo_csv)

contador_imagenes_procesadas = 0

# Itera a través de las subcarpetas
for nombre_subcarpeta in os.listdir(carpeta_principal):
    # Ignora las carpetas especiales '.' y '..'
    if nombre_subcarpeta in ['.', '..']:
        continue

    # Lee todas las imágenes en la subcarpeta actual
    ruta_subcarpeta = os.path.join(carpeta_principal, nombre_subcarpeta)
    imagenes = [imagen for imagen in os.listdir(
        ruta_subcarpeta) if imagen.endswith('.png')]

    for nombre_imagen in imagenes:
        # Lee la imagen con OpenCV
        ruta_imagen = os.path.join(ruta_subcarpeta, nombre_imagen)
        imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

        # Redimensiona la imagen a un tamaño fijo
        imagen_redimensionada = cv2.resize(imagen, nuevo_tamano)

        # Binariza la imagen (ajusta según sea necesario)
        _, imagen_binarizada = cv2.threshold(
            imagen_redimensionada, 128, 1, cv2.THRESH_BINARY)

        # Convierte la matriz de la imagen en una fila
        fila_datos = imagen_binarizada.flatten()

        # Escribe la fila en el archivo CSV junto con la etiqueta
        etiqueta = nombre_subcarpeta
        csv_writer.writerow([etiqueta] + fila_datos.tolist())

        contador_imagenes_procesadas += 1

print(f'Total de imágenes procesadas: {contador_imagenes_procesadas}')


# Cierra el archivo CSV
archivo_csv.close()
