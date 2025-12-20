# Reporte de Análisis de Datos: Realidad vs. Ficción (Nov 2025)

## Resumen Ejecutivo
Este análisis examina la coincidencia temporal entre dos fenómenos masivos en México durante noviembre de 2025: el estreno de **Frankenstein** (Guillermo del Toro) y las **Protestas de la Generación Z**. El objetivo fue identificar correlaciones de sentimiento y volumen mediático utilizando Python para procesar el dataset `datasetTexto.csv`.

---

## 1. Hallazgos Clave del Dataset

### La "Bipolaridad Emocional" de México
Los datos revelan una fractura emocional clara en el discurso público:
* **El Refugio Cultural:** Mientras el país celebra un logro artístico (Oscar, Venecia, Estética), el sentimiento es abrumadoramente positivo (**+1.0** promedio). La película funciona como un escape colectivo.
* **La Furia Social:** Simultáneamente, la narrativa de las protestas alcanza niveles críticos de negatividad (**-1.5**), impulsada por palabras clave como "represión", "miedo" y "robo de futuro".

### El Punto de Quiebre: 16 de Noviembre
El análisis temporal muestra que la atención mediática no fue constante:
* **Frankenstein:** Mantiene un crecimiento orgánico y constante desde inicios de mes.
* **Gen Z:** Muestra un **pico explosivo el 16 de noviembre**. Los datos validan que este fue el día crítico de confrontación (detenciones en el Ángel), rompiendo la barrera mediática tradicional.

### Control de Narrativa
Los medios internacionales (Reuters, El País) y plataformas digitales mostraron mayor volumen de cobertura sobre la protesta que los medios nacionales tradicionales. Esto sugiere que la validación del movimiento vino desde el exterior y las redes sociales, superando el cerco informativo local.

**Conclusión Sintética:** El dataset cuenta la historia de un país que se conmueve por un monstruo ficticio (que busca amor paterno) mientras protesta contra un sistema real (percibido como un padre ausente e indiferente).

---

## 2. Explicación Técnica del Código

El script de Python utiliza un enfoque de Ciencia de Datos ágil para transformar texto no estructurado en insights visuales. A continuación se detalla la lógica implementada:

### Ingesta y Limpieza (Pandas)
* **Robustez:** Se implementó manejo de errores (`try/except`) y el parámetro `on_bad_lines='skip'` para asegurar que el script no falle si el CSV presenta inconsistencias de formato.
* **Normalización Temporal:** Se forzó la conversión de la columna `Fecha` a objetos `datetime`, eliminando registros sin fecha válida para garantizar la precisión de la línea de tiempo.

### Motor de Sentimiento (Heurística)
En lugar de utilizar modelos de IA pesados, se diseñó una función algorítmica eficiente:
* **Diccionarios de Peso:** Se definieron listas de palabras clave positivas (ej. "orgullo", "maestra") y negativas (ej. "represión", "miedo").
* **Ponderación Asimétrica:** Se asignó un valor de **-1.5** a las palabras negativas frente a **+1.0** a las positivas.
    * *Justificación Técnica:* En análisis de crisis social, la indignación tiende a tener mayor peso y viralidad que la celebración. Este ajuste calibra el modelo a la realidad del comportamiento en redes sociales.

### Visualización (Matplotlib & Seaborn)
Se eligió un estilo `dark_background` para maximizar el contraste visual.
* **Gráfica de Línea:** Permite visualizar la tendencia y la velocidad de escalada de los eventos.
* **Boxplot (Caja y Bigotes):** Utilizado para medir la dispersión de opiniones. Permite identificar si existe consenso o polarización dentro de cada categoría.
* **Optimización de Código:** Se ajustaron los parámetros `hue` y `legend` para cumplir con los estándares actuales de la librería Seaborn, garantizando un código limpio y sin advertencias de depreciación.