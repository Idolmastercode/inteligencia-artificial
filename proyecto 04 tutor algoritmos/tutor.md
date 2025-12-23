# Proyecto: Tutor de Algoritmos basado en Fine-Tuning de LLM

## Descripción General

Este proyecto consiste en la creación de un **tutor de algoritmos** basado en un **modelo de lenguaje fine-tuneado**, cuyo objetivo es **explicar algoritmos de forma didáctica**, clara y progresiva, simulando el comportamiento de un tutor humano.

A diferencia de un modelo genérico que responde de manera técnica o ambigua, este tutor está entrenado específicamente para **enseñar**, no solo para describir.

---

## Dataset de Algoritmos

### Origen y Características

- **Cantidad aproximada:** ~2,000 algoritmos
- **Formato original:** Lenguaje técnico y descriptivo
- **Contenido:**  
  - Algoritmos clásicos  
  - Estructuras de datos  
  - Procedimientos paso a paso  
  - Explicaciones formales

Este dataset original **no era adecuado directamente** para un tutor, ya que el lenguaje era excesivamente técnico y poco pedagógico.

---

## Reescritura del Dataset (Data Augmentation)

Para transformar el dataset en material útil para enseñanza, se realizó un proceso de **reescritura asistida por LLM**:

- Cada algoritmo fue pasado por un modelo LLaMA
- Se utilizó un **prompt específico tipo tutor**, por ejemplo:
  - “Explica este algoritmo como si fueras un tutor”
  - “Incluye pasos, intuición y ejemplos simples”

### Costo Computacional

- Proceso **extremadamente tardado**
- Aproximadamente **5 horas de ejecución**
- Uso intensivo de GPU para acelerar el procesamiento

El resultado fue un **nuevo dataset pedagógico**, específicamente diseñado para entrenar un tutor.

---

## Dataset Final

- **Formato:** `JSONL`
- **Estructura:** Conversaciones tipo chat
- **Rol principal:** Tutor de algoritmos
- **Uso:** Fine-tuning supervisado (SFT)

Este dataset final es el núcleo del comportamiento didáctico del modelo.

---

## Modelo Base

- **Modelo:** LLaMA (variante instruct)
- **Tamaño:** 1B parámetros
- **Cuantización:** 4-bit (bnb)
- **Framework:** Unsloth

La elección de un modelo pequeño se hizo para:
- Reducir costos computacionales
- Facilitar ejecución local
- Mantener tiempos de entrenamiento razonables

---

## Fine-Tuning del Modelo

### Técnica Utilizada

- **Fine-Tuning Supervisado (SFT)**
- **Adaptadores LoRA**
- Entrenamiento optimizado para GPU

### Configuración General

- Longitud máxima de secuencia: 2048 tokens
- Batch size reducido con acumulación de gradientes
- Entrenamiento de 1 época (suficiente dado el tamaño del dataset)
- Optimizador AdamW en 8-bit

El proceso fue **estable y directo**, sin necesidad de múltiples épocas debido a la calidad del dataset.

---

## Hardware y Rendimiento

- **GPU:** NVIDIA RTX 5070
- Entrenamiento fluido y sin cuellos de botella
- El mayor tiempo de cómputo ocurrió durante la **generación del dataset**, no durante el fine-tuning

Una vez preparado el dataset, el entrenamiento fue relativamente rápido.

---

## Exportación y Uso Final

El modelo entrenado fue exportado en formato:

- **GGUF**
- Cuantización `q8_0`

Esto permite:
- Uso directo en **Ollama**
- Ejecución local
- Integración sencilla como tutor interactivo

---

## Resultado

El modelo final:

- Explica algoritmos paso a paso
- Usa lenguaje claro y pedagógico
- Se comporta como un tutor, no como un manual técnico
- Responde de forma consistente y enfocada en enseñanza

El objetivo no fue crear un modelo “generalista”, sino un **tutor especializado y funcional**.

---

## Conclusión

Este proyecto demuestra que, con un dataset bien diseñado y un fine-tuning eficiente, es posible transformar un modelo pequeño en una herramienta educativa útil.  
La clave del éxito no estuvo en el tamaño del modelo, sino en:

- La **calidad del dataset**
- El **diseño del prompt**
- La **reescritura pedagógica del conocimiento**

En resumen:  
**dataset bueno + fine-tuning simple = tutor efectivo**.
