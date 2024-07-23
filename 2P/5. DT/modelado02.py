import cv2
import numpy as np
import joblib
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename

# Función para cargar la imagen usando un cuadro de diálogo


def cargar_imagen():
    # Ocultar la ventana principal de Tkinter
    root = Tk()
    root.withdraw()
    # Abrir el cuadro de diálogo para seleccionar el archivo
    filename = askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png")]
    )
    return filename


# Cargar el modelo
clf = joblib.load('modelos/modelo_arbol_decision.pkl')

# Obtener la ruta de la imagen seleccionada por el usuario
ruta_imagen = cargar_imagen()

# Verificar si se seleccionó una imagen
if ruta_imagen:
    # Leer la imagen a color
    image_bgr = cv2.imread(ruta_imagen, cv2.IMREAD_COLOR)

    # Convertir la imagen de BGR (OpenCV) a RGB
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Convertir la imagen a escala de grises
    image_gry = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

    # Umbralización utilizando el método de Otsu
    _, image_bin = cv2.threshold(
        image_gry, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Redimensionar la imagen para que no sea demasiado grande (por ejemplo, a 400px de ancho máximo)
    max_width = 400
    height, width = image_bin.shape
    if width > max_width:
        scaling_factor = max_width / width
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        image_bin_resized = cv2.resize(image_bin, (new_width, new_height))
    else:
        image_bin_resized = image_bin

    # Mostrar la imagen binarizada redimensionada
    cv2.imshow('Imagen binarizada', image_bin_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Redimensionar la imagen a 64x64 para la predicción
    img_rz = cv2.resize(image_bin, (64, 64))

    # Convertir la imagen a un array de numpy y aplanarla
    img_data = np.array(img_rz).flatten()

    # Usar el modelo para predecir la clase de la imagen
    prediccion = clf.predict([img_data])

    # Crear una ventana emergente con la predicción
    root = Tk()
    root.withdraw()
    mensaje = 'Es un 7' if prediccion.item() == 1 else 'No es un 7'
    messagebox.showinfo("Predicción", mensaje)
else:
    print("No se seleccionó ninguna imagen.")
