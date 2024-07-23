import math
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import matplotlib.pyplot as plt


global imgOriginal
global imgGris
global imgBinaria
global imgGrisRuido
global imgSuavizada
imgOriginal = None
imgGris = None
imgBinaria = None
imgGrisRuido = None
imgSuavizada = None

def cargar_mascaras():
    mascaras = {
        "Robert": (np.array([[1, 0], [0, -1]]), np.array([[0, 1], [-1, 0]])),
        "Prewit": (np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]), np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])),
        "Sobel": (np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]), np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])),
        "Laplaciano": (np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])),
        "Laplaciano Gaussiano": (np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]])),
        "Kirsch": (
            np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]), # 0
            np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]]), # 45
            np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]), # 90
            np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]]) # 135
        ),
        "Frei-Chen Orillas": (
            np.array([[1, math.sqrt(2), 1], [0, 0, 0], [-1, math.sqrt(2), -1]]),
            np.array([[1, 0, -1], [math.sqrt(2), 0, -math.sqrt(2)], [1, 0, -1]]), 
            np.array([[0, -1, math.sqrt(2)], [1, 0, -1], [-math.sqrt(2), 1, 0]]),
            np.array([[math.sqrt(2), -1, 0], [-1, 0, 1], [0, 1, -math.sqrt(2)]])
        ),
        "Frei-Chen Lineas": (
            np.array([[0, 1, 0], [-1, 0, -1], [0, 1, 0]]),
            np.array([[-1, 0, 1], [0, 0, 0], [1, 0, -1]]),
            np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]]),
            np.array([[-2, 1, -2], [1, 4, 1], [-2, 1, -2]])
        )
    }
    return mascaras

def cargar_foto():
    global imgOriginal
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
    )
    if file_path:
        try:
            # Abre la imagen y la muestra en la ventana
            imgOriginal = Image.open(file_path)
            img = imgOriginal.copy()
            img.thumbnail((250, 250))  # Redimensiona la imagen si es necesario
            img = ImageTk.PhotoImage(img)
            lbl_imagen.config(image=img)
            lbl_imagen.image = img  # Necesario para evitar que Python elimine la referencia a la imagen
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

def boton_pulsado(num):
    def handler():
        if num == 1:
            botonRobert()
        elif num == 2:
            botonPrewit()
        elif num == 3:
            botonSobel()
        elif num == 4:
            bototonLaplaciano()
        elif num == 5:
            bototonLaplacianoGaussiano()
        elif num == 6:
            botonKirsch()
        elif num == 7:
            botonFreiChenOrillas()
        elif num == 8:
            botonFreiChenLineas()
    return handler

def imagenGris():
    global imgOriginal, imgGris, imgGrisRuido
    if imgOriginal:
        # Convertir la imagen PIL a un arreglo numpy
        imagen_np = np.array(imgOriginal.convert("RGB"))
        image_rgb = cv2.cvtColor(imagen_np, cv2.COLOR_BGR2RGB)
        # Convertir la imagen a escala de grises usando cv2
        imgGris = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        # Aplicar ruido a la imagen en escala de grises
        imgGrisRuido = agregar_ruido_sal_pimienta(imgGris)
        return imgGris
    else:
        return []

def agregar_ruido_sal_pimienta(imagen, probabilidad_sal=0.1, probabilidad_pimienta=0.1):
    h, w = imagen.shape
    sal = np.random.rand(h, w) < probabilidad_sal
    pimienta = np.random.rand(h, w) < probabilidad_pimienta
    imagen_con_ruido = imagen.copy()
    imagen_con_ruido[sal] = 255
    imagen_con_ruido[pimienta] = 0
    return imagen_con_ruido


def imagenBinaria(img):
    global imgBinaria
    if img.any():
        # Aplicar umbralización a la imagen en escala de grises
        _, imgBinaria = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY_INV)
        return imgBinaria
    else:
        return []

def aplicar_padding(imagen, tamano_padding=1):
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

def filtro_suavizado_mediana(img, tamano_mascara=3, pasos=1):
    global imgSuavizada
    imgPadding = aplicar_padding(img, tamano_mascara // 2)
    # Convertir la imagen a escala de grises si es necesario
    if len(imgPadding.shape) == 3:
        imgPadding = cv2.cvtColor(imgPadding, cv2.COLOR_BGR2GRAY)

    # Obtener dimensiones de la imagen y tamaño de la máscara
    filas, columnas = imgPadding.shape
    mitad_mascara = tamano_mascara // 2

    # Crear imagen suavizada
    img_suavizada = np.zeros_like(imgPadding)

    # Aplicar el filtro de suavizado de mediana
    for _ in range(pasos):
        for i in range(filas):
            for j in range(columnas):
                # Obtener los valores de los píxeles en la vecindad de la máscara
                vecindad = imgPadding[max(0, i - mitad_mascara): min(filas, i + mitad_mascara + 1),
                               max(0, j - mitad_mascara): min(columnas, j + mitad_mascara + 1)]
                # Calcular el valor de la mediana y asignarlo al píxel correspondiente en la imagen suavizada
                img_suavizada[i, j] = np.median(vecindad)

        # Actualizar la imagen original con la imagen suavizada para el siguiente paso (si hay más pasos)
        imgSuavizada = img_suavizada.copy()

    return imgSuavizada

def botonRobert():
    global imgOriginal, imgGris, imgGrisRuido, imgBinaria, imgSuavizada
    imgGris = imagenGris()
    imgGrisRuido = agregar_ruido_sal_pimienta(imagen=imgGris)
    imgSuavizada = filtro_suavizado_mediana(imgGrisRuido, 3, 1)
    imgBinaria = imagenBinaria(imgSuavizada)
    if imgSuavizada.any():

        # Aplicar el filtro de Robert a la imagen en escala de grises
        mascara_x, mascara_y = mascaras["Robert"]
        convolucionX=cv2.filter2D(imgBinaria, -1, mascara_x)
        convolucionY=cv2.filter2D(imgBinaria, -1, mascara_y)
        imgAcentuada = np.sqrt(convolucionX**2 + convolucionY**2)

        plt.clf()

        # Mostrar la imagen original
        plt.subplot(2, 4, 1)
        plt.imshow(imgOriginal)
        plt.title('Imagen Original - Robert')
        plt.axis('off')

        # Mostrar la imagen gris
        plt.subplot(2, 4, 2)
        plt.imshow(imgGris, cmap='gray')
        plt.title('Imagen Gris')
        plt.axis('off')

        # Mostrar la imagen con ruido
        plt.subplot(2, 4, 3)
        plt.imshow(imgGrisRuido, cmap='gray')
        plt.title('Imagen Ruido')
        plt.axis('off')

        # Mostrar la imagen Suavizada
        plt.subplot(2, 4, 4)
        plt.imshow(imgSuavizada, cmap='gray')
        plt.title('Imagen Suavizada')
        plt.axis('off')

        # Mostrar la imagen binaria
        plt.subplot(2, 4, 5)
        plt.imshow(imgBinaria, cmap='binary')
        plt.title('Imagen Binaria')
        plt.axis('off')

        # Mostrar la imagen convolucionada en x
        plt.subplot(2, 4, 6)
        plt.imshow(convolucionX, cmap='binary')
        plt.title('Convolución Horizontal')
        plt.axis('off')

        # Mostrar la imagen convolucionada en y
        plt.subplot(2, 4, 7)
        plt.imshow(convolucionY, cmap='binary')
        plt.title('Imagen Vertical')
        plt.axis('off')

        # Mostrar la imagen resultante
        plt.subplot(2, 4, 8)
        plt.imshow(imgAcentuada, cmap='binary')
        plt.title('Imagen Resultante')
        plt.axis('off')

        plt.tight_layout()
        plt.show()

    else:
        return []

def botonPrewit():
    global imgOriginal, imgGris, imgGrisRuido, imgBinaria, imgSuavizada
    imgGris = imagenGris()
    imgGrisRuido = agregar_ruido_sal_pimienta(imagen=imgGris)
    imgSuavizada = filtro_suavizado_mediana(imgGrisRuido, 3, 1)
    imgBinaria = imagenBinaria(imgSuavizada)
    if imgSuavizada.any():

        # Aplicar el filtro de Robert a la imagen en escala de grises
        mascara_x, mascara_y = mascaras["Prewit"]
        convolucionX=cv2.filter2D(imgBinaria, -1, mascara_x)
        convolucionY=cv2.filter2D(imgBinaria, -1, mascara_y)
        imgAcentuada = np.sqrt(convolucionX**2 + convolucionY**2)

        plt.clf()

        # Mostrar la imagen original
        plt.subplot(2, 4, 1)
        plt.imshow(imgOriginal)
        plt.title('Imagen Original - Prewit')
        plt.axis('off')

        # Mostrar la imagen Gris
        plt.subplot(2, 4, 2)
        plt.imshow(imgGris, cmap='gray')
        plt.title('Imagen Gris')
        plt.axis('off')

        # Mostrar la imagen con ruido
        plt.subplot(2, 4, 3)
        plt.imshow(imgGrisRuido, cmap='gray')
        plt.title('Imagen Ruido')
        plt.axis('off')

        # Mostrar la imagen suavizada
        plt.subplot(2, 4, 4)
        plt.imshow(imgSuavizada, cmap='gray')
        plt.title('Imagen Suavizada')
        plt.axis('off')

        # Mostrar la imagen binaria
        plt.subplot(2, 4, 5)
        plt.imshow(imgBinaria, cmap='binary')
        plt.title('Imagen Binaria')
        plt.axis('off')

        # Mostrar la imagen convolucionada en X
        plt.subplot(2, 4, 6)
        plt.imshow(convolucionX, cmap='binary')
        plt.title('Convolución Horizontal')
        plt.axis('off')

        # Mostrar la imagen convolucionada en Y
        plt.subplot(2, 4, 7)
        plt.imshow(convolucionY, cmap='binary')
        plt.title('Imagen Vertical')
        plt.axis('off')

        # Mostrar la imagen resultante
        plt.subplot(2, 4, 8)
        plt.imshow(imgAcentuada, cmap='binary')
        plt.title('Imagen Resultante')
        plt.axis('off')

        plt.tight_layout()
        plt.show()

    else:
        return []

def botonSobel():
    global imgOriginal, imgGris, imgGrisRuido, imgBinaria
    imgGris = imagenGris()
    imgGrisRuido = agregar_ruido_sal_pimienta(imagen=imgGris)
    imgBinaria = imagenBinaria(imgGrisRuido)
    if imgBinaria.any():
        # Aplicar el filtro de Robert a la imagen en escala de grises
        mascara_x, mascara_y = mascaras["Sobel"]
        convolucionX=cv2.filter2D(imgBinaria, -1, mascara_x)
        convolucionY=cv2.filter2D(imgBinaria, -1, mascara_y)
        imgAcentuada = np.sqrt(convolucionX**2 + convolucionY**2)

        plt.clf()

        # Mostrar la imagen original
        plt.subplot(2, 4, 1)
        plt.imshow(imgOriginal)
        plt.title('Imagen Original - Sobel')
        plt.axis('off')

        # Mostrar la imagen Gris
        plt.subplot(2, 4, 2)
        plt.imshow(imgGris, cmap='gray')
        plt.title('Imagen Gris')
        plt.axis('off')

        # Mostrar la imagen con ruido
        plt.subplot(2, 4, 3)
        plt.imshow(imgGrisRuido, cmap='gray')
        plt.title('Imagen Ruido')
        plt.axis('off')

        # Mostrar la imagen binaria
        plt.subplot(2, 4, 4)
        plt.imshow(imgBinaria, cmap='binary')
        plt.title('Imagen Binaria')
        plt.axis('off')

        # Mostrar la imagen convolucionada en X
        plt.subplot(2, 4, 5)
        plt.imshow(convolucionX, cmap='binary')
        plt.title('Convolución Horizontal')
        plt.axis('off')

        # Mostrar la imagen convolucionada en Y
        plt.subplot(2, 4, 6)
        plt.imshow(convolucionY, cmap='binary')
        plt.title('Imagen Vertical')
        plt.axis('off')

        # Mostrar la imagen resultante
        plt.subplot(2, 4, 7)
        plt.imshow(imgAcentuada, cmap='binary')
        plt.title('Imagen Resultante')
        plt.axis('off')

        plt.tight_layout()
        plt.show()

def bototonLaplaciano():
    global imgOriginal, imgGris, imgGrisRuido, imgBinaria, imgSuavizada
    imgGris = imagenGris()
    imgGrisRuido = agregar_ruido_sal_pimienta(imagen=imgGris)
    imgSuavizada = filtro_suavizado_mediana(imgGrisRuido, 3, 1)
    imgBinaria = imagenBinaria(imgSuavizada)

    if imgBinaria.any():

        # Aplicar el filtro de Robert a la imagen en escala de grises
        mascara = mascaras["Laplaciano"]
        convolucion=cv2.filter2D(imgBinaria, -1, mascara)

        plt.clf()

        # Mostrar la imagen original
        plt.subplot(2, 3, 1)
        plt.imshow(imgOriginal)
        plt.title('Imagen Original - Laplaciano')
        plt.axis('off')

        # Mostrar la imagen Gris
        plt.subplot(2, 3, 2)
        plt.imshow(imgGris, cmap='gray')
        plt.title('Imagen Gris')
        plt.axis('off')

        # Mostrar la imagen con ruido
        plt.subplot(2, 3, 3)
        plt.imshow(imgGrisRuido, cmap='gray')
        plt.title('Imagen Ruido')
        plt.axis('off')

        # Mostrar la imagen suavizada
        plt.subplot(2, 3, 4)
        plt.imshow(imgSuavizada, cmap='gray')
        plt.title('Imagen Suavizada')
        plt.axis('off')

        # Mostrar la imagen binaria
        plt.subplot(2, 3, 5)
        plt.imshow(imgBinaria, cmap='binary')
        plt.title('Imagen Binaria')
        plt.axis('off')

        # Mostrar la imagen convolucionada
        plt.subplot(2, 3, 6)
        plt.imshow(convolucion, cmap='binary')
        plt.title('Convolución')
        plt.axis('off')

        plt.tight_layout()
        plt.show()

def bototonLaplacianoGaussiano():
    global imgOriginal, imgGris, imgGrisRuido, imgBinaria, imgSuavizada
    imgGris = imagenGris()
    imgGrisRuido = agregar_ruido_sal_pimienta(imagen=imgGris)
    imgSuavizada = filtro_suavizado_mediana(imgGrisRuido, 3, 1)
    imgBinaria = imagenBinaria(imgSuavizada)

    if imgBinaria.any():

        # Aplicar el filtro de Robert a la imagen en escala de grises
        mascara = mascaras["Laplaciano Gaussiano"]
        convolucion=cv2.filter2D(imgBinaria, -1, mascara)

        plt.clf()

        # Mostrar la imagen original
        plt.subplot(2, 3, 1)
        plt.imshow(imgOriginal)
        plt.title('Imagen Original - Laplaciano Gaussiano')
        plt.axis('off')

        # Mostrar la imagen Gris
        plt.subplot(2, 3, 2)
        plt.imshow(imgGris, cmap='gray')
        plt.title('Imagen Gris')
        plt.axis('off')

        # Mostrar la imagen con ruido
        plt.subplot(2, 3, 3)
        plt.imshow(imgGrisRuido, cmap='gray')
        plt.title('Imagen Ruido')
        plt.axis('off')

        # Mostrar la imagen suavizada
        plt.subplot(2, 3, 4)
        plt.imshow(imgSuavizada, cmap='gray')
        plt.title('Imagen Suavizada')
        plt.axis('off')

        # Mostrar la imagen binaria
        plt.subplot(2, 3, 5)
        plt.imshow(imgBinaria, cmap='binary')
        plt.title('Imagen Binaria')
        plt.axis('off')

        # Mostrar la imagen convolucionada
        plt.subplot(2, 3, 6)
        plt.imshow(convolucion, cmap='binary')
        plt.title('Convolución')
        plt.axis('off')

        plt.tight_layout()
        plt.show()

def botonKirsch():
    global imgOriginal, imgGris, imgGrisRuido, imgBinaria, imgSuavizada
    imgGris = imagenGris()
    imgGrisRuido = agregar_ruido_sal_pimienta(imagen=imgGris)
    imgSuavizada = filtro_suavizado_mediana(imgGrisRuido, 3, 1)
    imgBinaria = imagenBinaria(imgSuavizada)

    if imgBinaria.any():
        mascara_0, mascara_45, mascara_90, mascara_135 = mascaras["Kirsch"]
        convolucion0=cv2.filter2D(imgBinaria, -1, mascara_0)
        convolucion45=cv2.filter2D(imgBinaria, -1, mascara_45)
        convolucion90=cv2.filter2D(imgBinaria, -1, mascara_90)
        convolucion135=cv2.filter2D(imgBinaria, -1, mascara_135)
        imgAcentuada = np.sqrt(convolucion0**2 + convolucion45**2 + convolucion90**2 + convolucion135**2)

        plt.clf()

        # Mostrar la imagen original
        plt.subplot(2, 5, 1)
        plt.imshow(imgOriginal)
        plt.title('Imagen Original - Kirsch')
        plt.axis('off')

        # Mostrar la imagen Gris
        plt.subplot(2, 5, 2)
        plt.imshow(imgGris, cmap='gray')
        plt.title('Imagen Gris')
        plt.axis('off')

        # Mostrar la imagen con ruido
        plt.subplot(2, 5, 3)
        plt.imshow(imgGrisRuido, cmap='gray')
        plt.title('Imagen Ruido')
        plt.axis('off')

        # Mostrar la imagen suavizada
        plt.subplot(2, 5, 4)
        plt.imshow(imgSuavizada, cmap='gray')
        plt.title('Imagen Suavizada')
        plt.axis('off')

        # Mostrar la imagen binaria
        plt.subplot(2, 5, 5)
        plt.imshow(imgBinaria, cmap='binary')
        plt.title('Imagen Binaria')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 0
        plt.subplot(2, 5, 6)
        plt.imshow(convolucion0, cmap='binary')
        plt.title('Convolución 0°')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 45
        plt.subplot(2, 5, 7)
        plt.imshow(convolucion45, cmap='binary')
        plt.title('Convolución 45°')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 90
        plt.subplot(2, 5, 8)
        plt.imshow(convolucion90, cmap='binary')
        plt.title('Convolución 90°')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 135
        plt.subplot(2, 5, 9)
        plt.imshow(convolucion135, cmap='binary')
        plt.title('Convolución 135°')
        plt.axis('off')

        # Mostrar la imagen resultante
        plt.subplot(2, 5, 10)
        plt.imshow(imgAcentuada, cmap='binary')
        plt.title('Imagen Resultante')
        plt.axis('off')

        plt.tight_layout()
        plt.show()

def botonFreiChenOrillas():
    global imgOriginal, imgGris, imgGrisRuido, imgBinaria, imgSuavizada
    imgGris = imagenGris()
    imgGrisRuido = agregar_ruido_sal_pimienta(imagen=imgGris)
    imgSuavizada = filtro_suavizado_mediana(imgGrisRuido, 3, 1)
    imgBinaria = imagenBinaria(imgSuavizada)

    if imgBinaria.any():
        mascara_0, mascara_45, mascara_90, mascara_135 = mascaras["Frei-Chen Orillas"]
        convolucion0=cv2.filter2D(imgBinaria, -1, mascara_0)
        convolucion45=cv2.filter2D(imgBinaria, -1, mascara_45)
        convolucion90=cv2.filter2D(imgBinaria, -1, mascara_90)
        convolucion135=cv2.filter2D(imgBinaria, -1, mascara_135)
        imgAcentuada = np.sqrt(convolucion0**2 + convolucion45**2 + convolucion90**2 + convolucion135**2)

        plt.clf()

        # Mostrar la imagen original
        plt.subplot(2, 5, 1)
        plt.imshow(imgOriginal)
        plt.title('Imagen Original - Frei-Chen Orillas')
        plt.axis('off')

        # Mostrar la imagen Gris
        plt.subplot(2, 5, 2)
        plt.imshow(imgGris, cmap='gray')
        plt.title('Imagen Gris')
        plt.axis('off')

        # Mostrar la imagen con ruido
        plt.subplot(2, 5, 3)
        plt.imshow(imgGrisRuido, cmap='gray')
        plt.title('Imagen Ruido')
        plt.axis('off')

        # Mostrar la imagen suavizada
        plt.subplot(2, 5, 4)
        plt.imshow(imgSuavizada, cmap='gray')
        plt.title('Imagen Suavizada')
        plt.axis('off')

        # Mostrar la imagen binaria
        plt.subplot(2, 5, 5)
        plt.imshow(imgBinaria, cmap='binary')
        plt.title('Imagen Binaria')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 0
        plt.subplot(2, 5, 6)
        plt.imshow(convolucion0, cmap='binary')
        plt.title('Convolución 0°')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 45
        plt.subplot(2, 5, 7)
        plt.imshow(convolucion45, cmap='binary')
        plt.title('Convolución 45°')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 90
        plt.subplot(2, 5, 8)
        plt.imshow(convolucion90, cmap='binary')
        plt.title('Convolución 90°')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 135
        plt.subplot(2, 5, 9)
        plt.imshow(convolucion135, cmap='binary')
        plt.title('Convolución 135°')
        plt.axis('off')

        # Mostrar la imagen resultante
        plt.subplot(2, 5, 10)
        plt.imshow(imgAcentuada, cmap='binary')
        plt.title('Imagen Resultante')
        plt.axis('off')

        plt.tight_layout()
        plt.show()
        
def botonFreiChenLineas():
    global imgOriginal, imgGris, imgGrisRuido, imgBinaria, imgSuavizada
    imgGris = imagenGris()
    imgGrisRuido = agregar_ruido_sal_pimienta(imagen=imgGris)
    imgSuavizada = filtro_suavizado_mediana(imgGrisRuido, 3, 1)
    imgBinaria = imagenBinaria(imgSuavizada)

    if imgBinaria.any():
        mascara_0, mascara_45, mascara_90, mascara_135 = mascaras["Frei-Chen Lineas"]
        convolucion0=cv2.filter2D(imgBinaria, -1, mascara_0)
        convolucion45=cv2.filter2D(imgBinaria, -1, mascara_45)
        convolucion90=cv2.filter2D(imgBinaria, -1, mascara_90)
        convolucion135=cv2.filter2D(imgBinaria, -1, mascara_135)
        imgAcentuada = np.sqrt(convolucion0**2 + convolucion45**2 + convolucion90**2 + convolucion135**2)

        plt.clf()

        # Mostrar la imagen original
        plt.subplot(2, 5, 1)
        plt.imshow(imgOriginal)
        plt.title('Imagen Original - Frei-Chen Lineas')
        plt.axis('off')

        # Mostrar la imagen Gris
        plt.subplot(2, 5, 2)
        plt.imshow(imgGris, cmap='gray')
        plt.title('Imagen Gris')
        plt.axis('off')

        # Mostrar la imagen con ruido
        plt.subplot(2, 5, 3)
        plt.imshow(imgGrisRuido, cmap='gray')
        plt.title('Imagen Ruido')
        plt.axis('off')

        # Mostrar la imagen suavizada
        plt.subplot(2, 5, 4)
        plt.imshow(imgSuavizada, cmap='gray')
        plt.title('Imagen Suavizada')
        plt.axis('off')

        # Mostrar la imagen binaria
        plt.subplot(2, 5, 5)
        plt.imshow(imgBinaria, cmap='binary')
        plt.title('Imagen Binaria')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 0
        plt.subplot(2, 5, 6)
        plt.imshow(convolucion0, cmap='binary')
        plt.title('Convolución 0°')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 45
        plt.subplot(2, 5, 7)
        plt.imshow(convolucion45, cmap='binary')
        plt.title('Convolución 45°')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 90
        plt.subplot(2, 5, 8)
        plt.imshow(convolucion90, cmap='binary')
        plt.title('Convolución 90°')
        plt.axis('off')

        # Mostrar la imagen convolucionada en 135
        plt.subplot(2, 5, 9)
        plt.imshow(convolucion135, cmap='binary')
        plt.title('Convolución 135°')
        plt.axis('off')

        # Mostrar la imagen resultante
        plt.subplot(2, 5, 10)
        plt.imshow(imgAcentuada, cmap='binary')
        plt.title('Imagen Resultante')
        plt.axis('off')

        plt.tight_layout()
        plt.show()

def crear_botones(ventana, mascaras):
    botones = [
        ("Robert", 1),
        ("Prewit", 2),
        ("Sobel", 3),
        ("Laplaciano", 4),
        ("Laplaciano Gaussiano", 5),
        ("Kirsch", 6),
        ("Frei-Chen Orillas", 7),
        ("Frei-Chen Lineas", 8)
    ]

    for nombre, num in botones:
        btn = tk.Button(ventana, text=nombre, command=boton_pulsado(num))
        btn.pack(pady=5)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Filtros de Acentuado")
ventana.geometry("300x500")

# Cargar mascaras
mascaras = cargar_mascaras()

# Crear el botón para cargar la foto
btn_cargar_foto = tk.Button(ventana, text="Cargar Foto", command=cargar_foto)
btn_cargar_foto.pack(pady=10)

# Crear una etiqueta para mostrar la imagen cargada
lbl_imagen = tk.Label(ventana)
lbl_imagen.pack(pady=10)

# Crear botones de filtros
crear_botones(ventana, mascaras)

# Ejecutar la ventana
ventana.mainloop()
