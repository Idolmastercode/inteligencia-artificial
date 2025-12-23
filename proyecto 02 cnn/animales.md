# Proyecto de Detección de Animales con CNN

## Descripción General

Este proyecto consiste en el desarrollo de un modelo de **detección y clasificación de animales** utilizando una **Red Neuronal Convolucional (CNN)**. El sistema es capaz de identificar las siguientes clases:

- Perros 🐶  
- Gatos 🐱  
- Tortugas 🐢  
- Hormigas 🐜  
- Mariquitas 🐞  

El objetivo principal fue evaluar el desempeño de una CNN entrenada con múltiples clases animales, considerando variaciones reales como ruido visual, fondos complejos y similitudes entre especies.

---

## Conjunto de Datos

- **Clases:** 5  
- **Imágenes por clase:** ~10,000  
- **Total de imágenes:** ~50,000  

Las imágenes presentan variaciones de:
- Iluminación
- Ángulos
- Fondos
- Tamaños y posturas

En particular, las clases de **perros y gatos** introdujeron mayor ruido visual debido a:
- Fondos domésticos similares
- Colores de pelaje parecidos
- Posturas poco consistentes

Esto afectó parcialmente la precisión del modelo.

---

## Preprocesamiento

- **Resolución de entrada:** `100x100` píxeles  
- Normalización de valores de píxeles  
- Redimensionamiento uniforme  
- Etiquetado por clase  

---

## Modelo

- **Tipo:** Red Neuronal Convolucional (CNN)  
- **Épocas de entrenamiento:** 100  
- **Entrada:** Imágenes RGB 100x100  
- **Salida:** Clasificación multiclase (5 clases)

El entrenamiento logró resultados **aceptables**, aunque con confusiones ocasionales entre perros y gatos debido al ruido mencionado.

---

## Entorno de Desarrollo

- **Sistema operativo:** Ubuntu ejecutado en **WSL (Windows Subsystem for Linux)**  
- **Framework:** TensorFlow (versión *Nightly*, experimental)  
- **Motivo del uso de Nightly:**  
  Permitir el uso eficiente de la **GPU directamente desde WSL**, lo cual no era posible con versiones estables en el momento del desarrollo.

---

## Aceleración por GPU

- **GPU:** NVIDIA RTX 5070  

El uso de TensorFlow Nightly con soporte experimental de GPU permitió:

- Reducción drástica del tiempo de entrenamiento  
- Ahorro literal de **horas de trabajo** comparado con ejecución en CPU  
- Mayor facilidad para experimentar con hiperparámetros  

Sin esta configuración, el entrenamiento completo habría sido considerablemente más lento.

---

## Resultados

- El modelo logró distinguir correctamente la mayoría de las clases.
- Las clases de **tortugas, hormigas y mariquitas** mostraron mejor separación.
- **Perros y gatos** presentaron mayor confusión debido al ruido visual.
- El desempeño general puede considerarse **funcional y aceptable**, aunque no perfecto.

---

## Conclusiones

Este proyecto demuestra la viabilidad de entrenar una CNN multiclase con un conjunto de datos relativamente grande, aprovechando herramientas experimentales para acelerar el desarrollo. A pesar de las dificultades introducidas por el ruido en ciertas clases, el modelo logró resultados razonables y sirvió como una experiencia práctica sólida en visión por computadora y uso de GPU con TensorFlow en WSL.
