# 📊 Práctica de IA: Análisis de Rendimiento de Modelos Pequeños

## Introducción

El objetivo de esta práctica fue evaluar la capacidad de 5 modelos de IA pequeños (phi3:mini, gemma:2b, tinydolphin, tinyllama, qwen:0.5b) para comprender y responder a preguntas específicas basadas en un temario de nivel universitario (Asignatura: Inteligencia Artificial, Clave: SCC-1012).

La evaluación se centró en la **precisión**, el **seguimiento de instrucciones** y la **coherencia** de las respuestas.

---

## Tabla Comparativa de Rendimiento

Se utilizó un sistema de semáforos para una evaluación visual rápida del desempeño en cada pregunta.

| Modelo | Q1 (Objetivo) | Q2 (Algoritmo A*) | Q3 (Razonamiento) | Q4 (SBR) | Q5 (Aplicaciones) | Veredicto |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **phi3:mini** | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | **Éxito Sobresaliente** |
| **gemma:2b** | 🟡 | 🟡 | 🔴 | 🔴 | 🟢 | **Rendimiento Mixto** |
| **tinyllama** | 🟡 | 🔴 | 🔴 | 🔴 | 🔴 | **Fallo Crítico (Alucinación)** |
| **tinydolphin** | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | **Fallo Crítico (Formato)** |
| **qwen:0.5b** | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | **Fallo Crítico (No-Respuesta)** |

**Leyenda:**
* 🟢 **Verde:** Respuesta precisa y contextualizada al temario.
* 🟡 **Amarillo:** Respuesta parcialmente correcta, genérica o vaga.
* 🔴 **Rojo:** Respuesta incorrecta, alucinada, o no se proporcionó respuesta a la pregunta.

---

## Análisis Detallado por Modelo

### 🥇 Ganador Indiscutible: phi3:mini

Este modelo demostró una capacidad superior para asimilar el contexto del temario y responder con precisión.

* **Q1 (Objetivo):** Capturó perfectamente la esencia del temario ("capacitar al ingeniero", "modelos matemáticos", "problemas complejos").
* **Q2 (A\*):** Dio la mejor definición, mencionando "búsqueda", "navegación por camino", "heurística" y "minimización del costo".
* **Q3 (Razonamiento):** Definió correctamente la diferencia clave: el razonamiento no-monótono permite que las conclusiones cambien con nueva información.
* **Q4 (SBR):** Identificó los componentes clave ("base de conocimiento" y "reglas"), aunque omitió el "mecanismo de control" explícito.
* **Q5 (Aplicaciones):** Listó las 6 aplicaciones correctamente y añadió descripciones (aunque con algunos errores tipográficos).

**Conclusión:** `phi3:mini` fue el único modelo que no solo *recuperó* información, sino que pareció *entender* los conceptos de IA sobre los que se le preguntaba.

---

### 🥈 Rendimiento Mixto: gemma:2b

Este modelo logró completar algunas tareas simples de recuperación, pero falló en las explicaciones conceptuales.

* **Q1 (Objetivo):** Dio una respuesta genérica. Correcta, pero no tan adaptada al temario como `phi3`.
* **Q2 (A\*):** Respuesta demasiado simple ("encontrar los caminos más cortos"). Es correcta, pero le falta la profundidad de una respuesta de nivel universitario.
* **Q3 y Q4 (Razonamiento y SBR):** Sus respuestas fueron vagas y conceptualmente incorrectas. ("múltiples lógicas" no es la definición de razonamiento no-monótono).
* **Q5 (Aplicaciones):** **Éxito total**. Listó las 6 aplicaciones de forma limpia y precisa.

**Conclusión:** `gemma:2b` es eficaz para tareas de extracción o listado de datos simples, pero no se le debe confiar la explicación de conceptos complejos.

---

### ❌ Fallo Crítico (Alucinación): tinyllama

Este modelo no solo falló en responder correctamente, sino que **inventó activamente información** (alucinó) que no estaba en el temario.

* **Q2 (A\*):** Fallo garrafal. Describió A\* como un algoritmo para "ajuste de ventanillas" y lo confundió con el conocimiento no-monótono.
* **Q3 (Razonamiento):** Omitió la pregunta por completo.
* **Q4 (SBR):** Alucinación severa. Inventó un concepto de "siete símbolos" y lo relacionó con "HTML" y "páginas web".
* **Q5 (Aplicaciones):** Listó 6 elementos, pero *ninguno* correspondía a la lista del Tema 4. Inventó su propia lista.

**Conclusión:** `tinyllama` es un ejemplo claro de los peligros de la alucinación en modelos pequeños. No es fiable para tareas basadas en contexto.

---

### ❌ Fallo Crítico (Formato y Coherencia): tinydolphin y qwen:0.5b

Estos dos modelos fallaron en el nivel más básico de la tarea: no pudieron seguir la instrucción de "responder las 5 preguntas".

* **tinydolphin:** No respondió las preguntas. En su lugar, generó un resumen del temario, pero lo hizo de forma incorrecta, mezclando los contenidos de los temas (ej. puso "reglas y búsqueda" en el Tema 2, cuando está en el Tema 3).
* **qwen:0.5b:** No generó ninguna respuesta. Simplemente repitió las preguntas y, en el proceso, asignó incorrectamente los números de los temas (ej. dijo que A\* estaba en el Tema 2).

**Conclusión:** Estos modelos no fueron capaces de procesar la instrucción (Preguntas + Contexto) y fallaron la prueba por completo.

---

## 💡 Conclusiones Generales de la Práctica

1.  **La Brecha de Capacidad es Enorme:** No todos los modelos "pequeños" son iguales. `phi3:mini` demostró capacidades de razonamiento contextual que lo colocan en una categoría muy superior a los demás.
2.  **Riesgo de Alucinación vs. Vaguedad:** Es más fácil detectar un modelo "malo" (como `tinyllama`) que alucina respuestas absurdas, que un modelo "mediocre" (como `gemma:2b`) que da respuestas vagas pero plausibles.
3.  **La Comprensión del Contexto es Clave:** La mayoría de los modelos (excepto `phi3`) ignoraron el temario. `tinyllama` y `tinydolphin` lo usaron incorrectamente, y `gemma` pareció ignorarlo en favor de respuestas genéricas. `phi3` fue el único que lo usó como la "fuente de verdad".
4.  **El Seguimiento de Instrucciones no está Garantizado:** Dos de los cinco modelos (`tinydolphin` y `qwen`) fallaron la tarea más simple: el formato de Pregunta y Respuesta.