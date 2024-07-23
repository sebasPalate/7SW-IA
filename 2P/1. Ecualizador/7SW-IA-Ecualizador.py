import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


def leer_imagen(ruta):
    try:
        imagen_bgr = cv2.imread(ruta, cv2.IMREAD_COLOR)
        if imagen_bgr is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen en {ruta}")
        return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f"Error al leer la imagen: {e}")
        return None


def mostrar_histograma(imagen, axes, canal, titulo=None):
    axes.cla()

    if canal == "rgb":
        canales = cv2.split(imagen)
        colores = ('red', 'green', 'blue')
        for canal, color in zip(canales, colores):
            axes.hist(canal.ravel(), bins=256, color=color,
                      alpha=0.7, label=f'{color.capitalize()}')
        axes.set_title(titulo)
    else:
        axes.hist(
            imagen.ravel(), bins=256, color=canal, alpha=0.7, label=titulo)
        axes.set_title(titulo)


def actualizar_imagen_mostrar_histograma(val):
    # Obtener el ajuste del slider
    ajuste_rojo = int(slider_rojo.val)
    ajuste_verde = int(slider_verde.val)
    ajuste_azul = int(slider_azul.val)

    # Sumar el ajuste al canal rojo y recortar los valores en el rango [0, 255]
    canal_rojo_modificado = cv2.add(canal_rojo, ajuste_rojo)
    canal_verde_modificado = cv2.add(canal_verde, ajuste_verde)
    canal_azul_modificado = cv2.add(canal_azul, ajuste_azul)

    # Modificar la imagen resultante
    imagen_resultante = cv2.merge(
        [canal_rojo_modificado, canal_verde_modificado, canal_azul_modificado])

    # Actualizar la imagen en el gráfico
    axs[4, 0].images[0].set_data(imagen_resultante)
    axs[4, 1].images[0].set_data(canal_rojo_modificado)
    axs[4, 2].images[0].set_data(canal_verde_modificado)
    axs[4, 3].images[0].set_data(canal_azul_modificado)

    # Actualizar los mostrar_histogramas
    mostrar_histograma(imagen_resultante, axs[3, 0], "rgb")
    mostrar_histograma(canal_rojo_modificado, axs[3, 1], "r")
    mostrar_histograma(canal_verde_modificado, axs[3, 2], "g")
    mostrar_histograma(canal_azul_modificado, axs[3, 3], "b")

    # Actualizar la figura
    fig.canvas.draw_idle()


try:
    imagen_rgb = leer_imagen('imagenes/dualipa.jpg')

    if imagen_rgb is not None:
        # Separar los canales RGB
        canal_rojo, canal_verde, canal_azul = cv2.split(imagen_rgb)

        # Crear una figura y ejes
        fig, axs = plt.subplots(5, 4, figsize=(10, 8))

        # Ocultar ejes para la imagen y el mostrar_histograma
        for ax in axs.flat:
            ax.label_outer()

        # Mostrar la imagenes y su mostrar_histograma sin modificar
        axs[0, 0].imshow(imagen_rgb)
        axs[0, 0].axis('off')
        mostrar_histograma(imagen_rgb, axs[1, 0], "rgb")

        axs[0, 1].imshow(canal_rojo, cmap='gray')
        axs[0, 1].axis('off')
        mostrar_histograma(canal_rojo, axs[1, 1], "r")

        axs[0, 2].imshow(canal_verde, cmap='gray')
        axs[0, 2].axis('off')
        mostrar_histograma(canal_verde, axs[1, 2], "g")

        axs[0, 3].imshow(canal_azul, cmap='gray')
        axs[0, 3].axis('off')
        mostrar_histograma(canal_azul, axs[1, 3], "b")

        # Eliminar los axs vacíos
        for ax in axs[2]:
            ax.remove()

        # Mostrar la imagen resultantes con su mostrar_histograma (modificados)
        axs[4, 0].imshow(imagen_rgb)
        axs[4, 0].axis('off')
        mostrar_histograma(imagen_rgb, axs[3, 0], "rgb")

        axs[4, 1].imshow(canal_rojo, cmap='gray')
        axs[4, 1].axis('off')
        mostrar_histograma(canal_rojo, axs[3, 1], "r")

        axs[4, 2].imshow(canal_verde, cmap='gray')
        axs[4, 2].axis('off')
        mostrar_histograma(canal_verde, axs[3, 2], "g")

        axs[4, 3].imshow(canal_azul, cmap='gray')
        axs[4, 3].axis('off')
        mostrar_histograma(canal_azul, axs[3, 3], "b")

        # Definir los límites de los sliders
        slider_min = -255
        slider_max = 255
        slider_step = 1

        # Definir la posición y el tamaño de los sliders para que estén centrados vertical y horizontalmente
        slider_width = 0.2
        slider_height = 0.03
        slider_padding = 0.05
        slider_start_y = 0.5
        slider_start_x = (1 - (slider_width * 3 + slider_padding * 2)) / 2

        slider_ax_rojo = fig.add_axes(
            [slider_start_x, slider_start_y, slider_width, slider_height])
        slider_ax_verde = fig.add_axes(
            [slider_start_x + slider_width + slider_padding, slider_start_y, slider_width, slider_height])
        slider_ax_azul = fig.add_axes(
            [slider_start_x + 2 * (slider_width + slider_padding), slider_start_y, slider_width, slider_height])

        # Crear los sliders en las posiciones especificadas
        slider_rojo = Slider(slider_ax_rojo, '', slider_min,
                             slider_max, valinit=0, valstep=slider_step)
        slider_verde = Slider(slider_ax_verde, '', slider_min,
                              slider_max, valinit=0, valstep=slider_step)
        slider_azul = Slider(slider_ax_azul, '', slider_min,
                             slider_max, valinit=0, valstep=slider_step)

        # Conectar el slider con la función de actualización
        slider_rojo.on_changed(actualizar_imagen_mostrar_histograma)
        slider_verde.on_changed(actualizar_imagen_mostrar_histograma)
        slider_azul.on_changed(actualizar_imagen_mostrar_histograma)

        # Mostrar la ventana interactiva
        plt.show()

except Exception as e:
    print(f"Error: {e}")
