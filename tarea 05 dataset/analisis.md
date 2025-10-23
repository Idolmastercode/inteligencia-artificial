# 📈 Análisis Simple en Excel — Dataset con 3 Columnas

## 🧾 Formato del dataset
El archivo contiene tres columnas

> La **columna C** representa una **variable binaria (0 o 1)**, que puede indicar *sí/no*, *activo/inactivo*, *aprobado/reprobado*, etc.

---

## ⚙️ Pasos del análisis

1. **Importar los datos:**  
   Abre Excel → pestaña **Datos** → “Desde texto/CSV” o “Desde archivo”.

2. **Limpiar o revisar datos:**  
   - Asegúrate de que no haya celdas vacías.  
   - Verifica el tipo de dato en cada columna (número o texto).

3. **Resumen estadístico rápido:**  
   - Usa funciones como:  
     - `=PROMEDIO(A:A)`  
     - `=DESVEST.P(A:A)`  
     - `=CONTAR.SI(C:C;1)` → cuenta los valores “1”.

4. **Gráfica básica:**  
   - Inserta → **Gráfica de dispersión (XY)** para comparar las columnas A y B.  
   - Usa el color o tamaño del punto según el valor en la columna C (0 o 1).  

---

## 🔍 Interpretación genérica

- Los puntos pueden mostrar **tendencias o agrupaciones** según la variable binaria.  
- Si las clases 0 y 1 se separan visualmente, hay una posible **relación entre A, B y C**.  
- Si están mezcladas, no hay correlación clara.

---

⚠️ **Nota:**  
Este análisis es únicamente exploratorio.  
**No se presentan conclusiones**, ya que **se desconoce el contexto y significado real del dataset**.

✅ **Resumen:**  
El análisis permite observar patrones básicos y verificar la distribución de datos, pero sin interpretación específica debido a la falta de información contextual.
