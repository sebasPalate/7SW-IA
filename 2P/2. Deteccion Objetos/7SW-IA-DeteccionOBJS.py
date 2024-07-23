import cv2
import matplotlib.pyplot as plt

# 1. Cargar la Imagen
# Leer la imagen a color
image_bgr = cv2.imread('imagenes/objs.jpg', cv2.IMREAD_COLOR)

# Convertir la imagen de BGR (OpenCV) a RGB
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

# 2. Preprocesamiento
# Convertir la imagen a escala de grises
image_gry = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

# 3. Definir Umbralización
_, image_bin = cv2.threshold(image_gry, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 4. Invertir la imagen binarizada (si es necesario)
# image_bin = cv2.bitwise_not(image_bin)

# 5. Identificacion de Contornos
contours, _ = cv2.findContours(image_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Convertir la imagen binarizada a color para dibujar contornos en color
image_bin_color = cv2.cvtColor(image_bin, cv2.COLOR_GRAY2BGR)
cv2.drawContours(image_bin_color, contours, -1, (255, 0, 0), 2)  # Dibujar contornos en azul

# Copiar la imagen RGB para dibujar los contornos
image_rgb_contours = image_rgb.copy()
# cv2.drawContours(image_rgb_contours, contours, -1, (255, 0, 0), 2)  # Dibujar contornos en azul

# 6. Filtrar los contornos por área, dibujar rectángulos y calcular centroides
min_area = 1000
for contour in contours:
    area = cv2.contourArea(contour)
    if area >= min_area:
        # Dibujar un rectángulo alrededor del contorno en la imagen binarizada a color y rgb
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image_bin_color, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Dibujar rectángulos en verde
        cv2.rectangle(image_rgb_contours, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Dibujar rectángulos en verde

        # Calcular el centroide
        M = cv2.moments(contour)
        if M["m00"] != 0:  # Evitar división por cero
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Dibujar el centroide en la imagen binarizada a color
            cv2.circle(image_bin_color, (cX, cY), 5, (0, 0, 255), -1)  
            cv2.putText(image_bin_color, f'Area: {int(area)}', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            # Dibujar círculo en rojo
            # cv2.circle(image_rgb_contours, (cX, cY), 5, (0, 0, 255), -1)

# 7. Mostrar las imágenes usando matplotlib
plt.figure(figsize=(18, 6))

# Mostrar la imagen original
plt.subplot(1, 3, 1)
plt.imshow(image_rgb)
plt.title('Imagen Original')
plt.axis('off')

# Mostrar la imagen binarizada con contornos y rectángulos
plt.subplot(1, 3, 2)
plt.imshow(image_bin_color)
plt.title('Imagen Binarizada con Contornos y Rectángulos')
plt.axis('off')

# Mostrar la imagen RGB con contornos
plt.subplot(1, 3, 3)
plt.imshow(image_rgb_contours)
plt.title('Imagen RGB con Contornos')
plt.axis('off')

# Mostrar el numero de objetos detectados al pie d ela figura
plt.figtext(0.5, 0.01, f'Número de objetos detectados: {len(contours)}', ha='center', fontsize=14)

# Mostrar las figuras
plt.tight_layout()
plt.show()
