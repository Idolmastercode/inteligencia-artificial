import cv2 as cv
import numpy as np
import sys

# --- FUNCIÓN PARA REDIMENSIONAR IMÁGENES MUY GRANDES ---
def redimensionar_para_mostrar(imagen, max_ancho=1000):
    """
    Redimensiona una imagen para mostrarla en pantalla si su ancho supera
    un máximo, manteniendo la proporción original.
    """
    alto, ancho = imagen.shape[:2]
    if ancho > max_ancho:
        proporcion = max_ancho / float(ancho)
        nuevo_alto = int(alto * proporcion)
        imagen_redimensionada = cv.resize(imagen, (max_ancho, nuevo_alto), interpolation=cv.INTER_AREA)
        return imagen_redimensionada
    else:
        return imagen
# ---------------------------------------------------------

img = cv.imread('figura.png')

img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

print("Selecciona el color que deseas segmentar:")
print("1: Rojo")
print("2: Verde")
print("3: Azul")
print("4: Amarillo")

opcion = input("Escribe el número: ")

mascara = np.zeros(img.shape[:2], dtype=np.uint8)

if opcion == '1':
    umbralBajo1 = (0, 100, 80)
    umbralAlto1 = (10, 255, 255)
    umbralBajo2 = (170, 100, 80)
    umbralAlto2 = (180, 255, 255)
    
    mascara1 = cv.inRange(img_hsv, umbralBajo1, umbralAlto1)
    mascara2 = cv.inRange(img_hsv, umbralBajo2, umbralAlto2)
    mascara = mascara1 + mascara2
    
elif opcion == '2':
    umbralBajo = (35, 80, 80)
    umbralAlto = (85, 255, 255)
    mascara = cv.inRange(img_hsv, umbralBajo, umbralAlto)

elif opcion == '3':
    umbralBajo = (100, 80, 80)
    umbralAlto = (130, 255, 255)
    mascara = cv.inRange(img_hsv, umbralBajo, umbralAlto)

elif opcion == '4':
    umbralBajo = (20, 100, 80)
    umbralAlto = (32, 255, 255)
    mascara = cv.inRange(img_hsv, umbralBajo, umbralAlto)

else:
    print("ERROR. Opción no válida.")
    sys.exit()

kernel = np.ones((5,5), np.uint8)
mascara_procesada = cv.morphologyEx(mascara, cv.MORPH_CLOSE, kernel)

resultado = cv.bitwise_and(img, img, mask=mascara_procesada) 
resultado_con_centros = resultado.copy()

contornos, _ = cv.findContours(mascara_procesada, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for i, contorno in enumerate(contornos):
    area = cv.contourArea(contorno)
    if area > 100:
        M = cv.moments(contorno)
        
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            continue
        cv.drawContours(resultado_con_centros, [contorno], -1, (0, 255, 0), 2)
        
        cv.circle(resultado_con_centros, (cX, cY), 5, (0, 0, 255), -1)
        
        cv.putText(resultado_con_centros, f"({cX},{cY})", (cX + 10, cY - 10), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

cv.namedWindow('Imagen Original', cv.WINDOW_NORMAL)
cv.namedWindow('Imagen HSV', cv.WINDOW_NORMAL)
cv.namedWindow('Mascara (sin procesar)', cv.WINDOW_NORMAL)
cv.namedWindow('Mascara Procesada', cv.WINDOW_NORMAL)
cv.namedWindow('Resultado (Color Aislado)', cv.WINDOW_NORMAL)
cv.namedWindow('Figuras con Centros', cv.WINDOW_NORMAL)

cv.imshow('Imagen Original', redimensionar_para_mostrar(img))
cv.imshow('Imagen HSV', redimensionar_para_mostrar(img_hsv))
cv.imshow('Mascara (sin procesar)', redimensionar_para_mostrar(mascara))
cv.imshow('Mascara Procesada', redimensionar_para_mostrar(mascara_procesada))
cv.imshow('Resultado (Color Aislado)', redimensionar_para_mostrar(resultado))
cv.imshow('Figuras con Centros', redimensionar_para_mostrar(resultado_con_centros))

cv.waitKey(0)
cv.destroyAllWindows()