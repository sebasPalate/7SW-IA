import cv2
import numpy as np
import matplotlib.pyplot as plt


def verificar_tamano(tamano):
    if tamano <= 1:
        raise ValueError("El tamaño de la máscara debe ser mayor a 1.")
    if tamano % 2 == 0 and tamano != 2:
        raise ValueError(
            "El tamaño de la máscara debe ser un número impar o 2.")


def crear_mascara_promedio(tamano):
    # Verificar el tamaño de la máscara
    verificar_tamano(tamano)

    # Calcular el valor de la máscara
    # valor_mascara = 1 / (tamano * tamano)
    valor_mascara = 1

    # Crear la máscara
    mascara = np.full((tamano, tamano), valor_mascara)
    return mascara


def crear_mascara_gaussiana(tamano, sigma, normalizar=True):
    # Verificar el tamaño de la máscara
    verificar_tamano(tamano)

    # Calcular el centro de la máscara
    centro = tamano // 2

    # Crear la máscara
    mascara = np.zeros((tamano, tamano))

    # Crear la máscara gaussiana
    for i in range(tamano):
        for j in range(tamano):
            distancia = np.sqrt((i - centro) ** 2 + (j - centro) ** 2)
            mascara[i, j] = np.exp(-(distancia ** 2) / (2 * sigma ** 2))

    # Normalizar la máscara para que la suma de todos los valores sea 1
    if normalizar:
        mascara /= np.sum(mascara)

    return mascara


def aplicar_padding(imagen, tamano_padding):
    if tamano_padding < 0:
        raise ValueError("El tamaño del padding debe ser no negativo.")

    # Obtener las dimensiones de la imagen
    alto, ancho = imagen.shape

    # Crear una nueva imagen con el relleno
    image_padding = np.zeros(
        (alto + 2*tamano_padding, ancho + 2*tamano_padding), dtype=imagen.dtype)

    # Copiar la imagen original en el centro de la nueva imagen
    image_padding[tamano_padding:alto+tamano_padding,
                  tamano_padding:ancho+tamano_padding] = imagen

    return image_padding


def agregar_ruido_sal_pimienta(imagen, probabilidad=0.05):
    # Copiar la imagen original
    salida = np.copy(imagen)

    # Calcular la cantidad de ruido
    cantidad_de_ruido = int(np.ceil(probabilidad * imagen.size))

    # Añadir "sal" (blanco)
    coords_sal = [np.random.randint(0, i, cantidad_de_ruido)
                  for i in imagen.shape]
    salida[coords_sal[0], coords_sal[1]] = 255

    # Añadir "pimienta" (negro)
    coords_pimienta = [np.random.randint(
        0, i, cantidad_de_ruido) for i in imagen.shape]
    salida[coords_pimienta[0], coords_pimienta[1]] = 0

    return salida


def convolucion_promedio(imagen, mascara, step=1):
    # Obtener el alto/ancho de la imagen y el tamaño de la mascara
    alto, ancho = imagen.shape
    tam_mascara = mascara.shape[0]

    # Crear una imagen de salida
    imagen_salida = np.zeros((alto - tam_mascara + 1, ancho - tam_mascara + 1))

    # Aplicar la convolución
    for i in range(0, alto - tam_mascara + 1, step):
        for j in range(0, ancho - tam_mascara + 1, step):
            region = imagen[i:i + tam_mascara, j:j + tam_mascara]
            valor = np.sum(region * mascara) / (tam_mascara * tam_mascara)
            imagen_salida[i, j] = round(valor)

    # Asegurarse que los valores estén en el rango correcto
    imagen_salida = np.clip(imagen_salida, 0, 255)

    return imagen_salida.astype(np.uint8)


def convolucion_mediana(imagen, tam_mascara, step=1):
    alto, ancho = imagen.shape

    # Crear una imagen de salida
    imagen_salida = np.zeros(
        (alto - tam_mascara + 1, ancho - tam_mascara + 1))

    # Aplicar la convolución
    for i in range(0, alto - tam_mascara + 1, step):
        for j in range(0, ancho - tam_mascara + 1, step):
            region = imagen[i:i + tam_mascara, j:j + tam_mascara]
            valor = np.median(region)
            imagen_salida[i, j] = valor

    # Asegurarse de que los valores estén en el rango correcto
    imagen_salida = np.clip(imagen_salida, 0, 255)

    return imagen_salida.astype(np.uint8)


def convolucion_gaussiana(imagen, mascara, step=1):
    alto, ancho = imagen.shape
    tam_mascara = mascara.shape[0]

    # Crear una imagen de salida
    imagen_salida = np.zeros((alto - tam_mascara + 1, ancho - tam_mascara + 1))

    # Aplicar la convolución
    for i in range(0, alto - tam_mascara + 1, step):
        for j in range(0, ancho - tam_mascara + 1, step):
            # Seleccionar la región de la imagen que coincida con el tamaño de la máscara gaussiana
            region = imagen[i:i + tam_mascara, j:j + tam_mascara]
            # Aplicar la convolución multiplicando la región por la máscara gaussiana y sumando los resultados
            valor = np.sum(region * mascara)
            # Asignar el valor resultante al píxel correspondiente en la imagen de salida
            imagen_salida[i, j] = round(valor)

    # Asegurarse de que los valores estén en el rango correcto
    imagen_salida = np.clip(imagen_salida, 0, 255)

    return imagen_salida.astype(np.uint8)


def calcular_moda(region):
    valores, cuentas = np.unique(region, return_counts=True)
    indice_moda = np.argmax(cuentas)
    return valores[indice_moda]


def convolucion_moda(imagen, tam_mascara, step=1):
    alto, ancho = imagen.shape

    # Crear una imagen de salida
    imagen_salida = np.zeros((alto - tam_mascara + 1, ancho - tam_mascara + 1))

    # Aplicar la convolución
    for i in range(0, alto - tam_mascara + 1, step):
        for j in range(0, ancho - tam_mascara + 1, step):
            region = imagen[i:i + tam_mascara, j:j + tam_mascara]
            valor = calcular_moda(region)
            imagen_salida[i, j] = valor

    # Asegurarse de que los valores estén en el rango correcto
    imagen_salida = np.clip(imagen_salida, 0, 255)
    return imagen_salida.astype(np.uint8)


# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Cargar una imagen
        image_bgr = cv2.imread('imagenes/iguaDua.jpg', cv2.IMREAD_COLOR)

        if image_bgr is None:
            raise FileNotFoundError(
                "No se pudo cargar la imagen. Verifica la ruta.")

        percent = 0.09  # Porcentaje de ruido
        padding = 1  # Tamaño del padding
        size = 3  # Tamaño de la máscara (normal y gaussiana)
        sigma = 1.0  # Sigma de la máscara gaussiana
        step = 1  # Paso de la convolución

        """1. Preprocesamiento de la Imagen"""
        # Convertir la imagen de BGR (OpenCV) a RGB
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        # Convertir la imagen en escala de grises
        image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

        # Agregar ruido a la imagen (sal y pimienta)
        image_nse = agregar_ruido_sal_pimienta(image_gray, percent)

        # Aplicar padding a la imagen
        image_padding = aplicar_padding(image_nse, padding)

        """2. Creación de las Mascaras"""
        # Crear una máscara de convolución
        mask_average = crear_mascara_promedio(size)

        # Crear una máscara gaussiana
        gaussian_mask = crear_mascara_gaussiana(size, sigma)

        """3. Aplicar las Convoluciones"""
        # Aplicar la convolución de promedio
        imagen_convolucionada_promedio = convolucion_promedio(
            image_padding, mask_average, step)

        # Aplicar la convolución de mediana
        imagen_convolucionada_mediana = convolucion_mediana(
            image_padding, size, step)

        # Aplicar la convolución de moda
        imagen_convolucionada_moda = convolucion_moda(
            image_padding, size, step)

        # Aplicar la convolución de promedio con la máscara gaussiana
        imagen_convolucionada_gaussiana = convolucion_gaussiana(
            image_padding, gaussian_mask, step)

        """4. Mostrar las Imágenes"""
        # Mostrar las imágenes
        plt.figure(figsize=(18, 6))

        # Mostrar la imagen original
        plt.subplot(2, 4, 1)
        plt.imshow(image_rgb)
        plt.title('Imagen Original')
        plt.axis('off')

        # Mostrar la imagen en escala de grises
        plt.subplot(2, 4, 2)
        plt.imshow(image_gray, cmap='gray')
        plt.title('Imagen Gris')
        plt.axis('off')

        # Mostrar imagen con sal y pimienta
        plt.subplot(2, 4, 3)
        plt.imshow(image_nse, cmap='gray')
        plt.title('Imagen con Ruido')
        plt.axis('off')

        # Mostrar la imagen con padding y ruido
        plt.subplot(2, 4, 4)
        plt.imshow(image_padding, cmap='gray')
        plt.title('Imagen con Padding/Ruido')
        plt.axis('off')

        # Mostrar resultando media/promedio
        plt.subplot(2, 4, 5)
        plt.imshow(imagen_convolucionada_promedio, cmap='gray')
        plt.title('Imagen Media/Promedio')
        plt.axis('off')

        # Mostrar resultando mediana
        plt.subplot(2, 4, 6)
        plt.imshow(imagen_convolucionada_mediana, cmap='gray')
        plt.title('Imagen Mediana')
        plt.axis('off')

        # Mostrar resultando moda
        plt.subplot(2, 4, 7)
        plt.imshow(imagen_convolucionada_moda, cmap='gray')
        plt.title('Imagen Moda')
        plt.axis('off')

        # Mostrar resultando gaussiana media/promedio
        plt.subplot(2, 4, 8)
        plt.imshow(imagen_convolucionada_gaussiana, cmap='gray')
        plt.title('Imagen Gaussiana')
        plt.axis('off')

        # Mostrar las figuras
        plt.tight_layout()
        plt.show()

    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
