# 🎨 Práctica: Detección de Color en una Imagen

## 🧾 Descripción general
En esta práctica se trabajó con una imagen para **detectar y resaltar un color específico** (rojo, verde, azul o amarillo).  
El programa permite elegir el color que se desea analizar y luego muestra las áreas donde aparece ese color.

---

## ⚙️ ¿Qué se hizo?

1. **Se cargó una imagen** llamada `figura.png`.
2. **Se convirtió la imagen** a un formato que facilita identificar colores (HSV).
3. El usuario **elige un color** a detectar desde un menú.
4. El programa **crea una máscara**, es decir, una capa que marca las zonas donde aparece ese color.
5. Luego **se limpian los bordes** de esa máscara para que los resultados sean más precisos.
6. Se **resalta la parte de la imagen** que tiene el color elegido.
7. Se **encuentran las figuras** de ese color y se dibuja su contorno junto con el **centro (coordenadas X, Y)**.
8. Finalmente, se muestran varias ventanas con los resultados:
   - Imagen original  
   - Imagen convertida a HSV  
   - Máscara sin procesar  
   - Máscara procesada  
   - Resultado con el color aislado  
   - Figuras con sus centros marcados

---

## 👁️ Resultados esperados
El usuario puede **visualizar el color seleccionado destacado** sobre el resto de la imagen.  
Cada figura detectada muestra su **contorno y su punto central**, ayudando a entender **dónde está** y **cuánto ocupa**.

---

⚠️ **Nota:**  
Esta práctica solo busca **probar la detección de color**, no se realizan mediciones o análisis más avanzados.