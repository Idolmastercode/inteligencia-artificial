# Proyecto de Análisis Sociocultural de la Generación Z mediante NLP y RAG

## 1. Introducción

Este proyecto tiene como objetivo realizar un **análisis sociocultural profundo de la Generación Z**, combinando **testimonios empíricos extraídos de redes sociales** con **teoría filosófica y sociológica**, utilizando técnicas modernas de **Procesamiento de Lenguaje Natural (NLP)** y **Modelos de Lenguaje (LLM)** bajo un enfoque de **Retrieval-Augmented Generation (RAG)**.

Más que centrarse en un producto final, el proyecto prioriza el **proceso de construcción del corpus**, la **limpieza y curaduría de datos**, y la **metodología computacional** empleada para contrastar experiencia vivida y teoría académica.

---

## 2. Justificación del Uso de Reddit como Fuente Empírica

Originalmente se contempló el uso de la **API oficial de Reddit**. Sin embargo, durante la fase de investigación, esta fue **fuertemente restringida** debido al uso masivo de datos para el entrenamiento de inteligencias artificiales.

Ante este contexto, se optó por trabajar con **datasets históricos ya existentes**, en formato CSV, recolectados previamente a dichas restricciones. Reddit se eligió por las siguientes razones:

- Alta presencia de usuarios pertenecientes a la **Generación Z**
- Cultura de escritura extensa y testimonial
- Existencia de subforos especializados en salud mental y experiencias personales
- Lenguaje menos filtrado y más espontáneo que otras redes sociales

---

## 3. Recolección Inicial de Datos

### 3.1 Volumen Inicial

- Aproximadamente **200 archivos CSV**
- Decenas de miles de comentarios
- Múltiples subreddits relacionados directa o indirectamente con la Generación Z

Este volumen inicial resultó **excesivo y ruidoso** para un análisis cualitativo profundo, por lo que fue necesaria una **fase intensiva de depuración**.

---

## 4. Limpieza y Curaduría del Corpus Empírico

### 4.1 Filtrado Semántico por Palabras Clave

Se aplicó un proceso de selección utilizando palabras clave asociadas a problemáticas recurrentes en la Generación Z:

- `ansiedad`
- `depresión`
- `burnout`

El objetivo fue **reducir el corpus a testimonios con alta carga emocional y existencial**, descartando contenido superficial o irrelevante.

### 4.2 Resultado del Filtrado

- Corpus final: ~**6,000 comentarios**
- Selección basada en:
  - Longitud mínima del texto
  - Presencia semántica de malestar psicológico
  - Origen verificable dentro de subreddits relevantes

Este conjunto se consolidó en un único archivo:

corpus_tesis_final.csv


---

## 5. Construcción del Corpus Teórico

Para contrastar los testimonios empíricos, se incorporó un **corpus teórico en formato PDF**, compuesto por textos filosóficos y sociológicos, entre ellos:

- *El existencialismo es un humanismo* – Jean-Paul Sartre
- *La sociedad del cansancio* – Byung-Chul Han
- Obras y ensayos de Bauman y otros autores contemporáneos

Estos textos representan un **marco conceptual** para interpretar fenómenos como:

- Ansiedad estructural
- Autoexplotación
- Crisis de sentido
- Individualización del fracaso

---

## 6. Procesamiento de Documentos Teóricos (PDF)

Los PDFs fueron cargados y fragmentados utilizando `PyPDFLoader`, permitiendo:

- División en fragmentos semánticamente manejables
- Asociación de metadatos
- Integración homogénea con los testimonios de Reddit

Cada fragmento fue tratado como un documento independiente para el sistema RAG.

---

## 7. Representación Vectorial (Embeddings)

### 7.1 Modelo de Embeddings

Se utilizó el modelo:

all-MiniLM-L6-v2


Por las siguientes razones:

- Buen equilibrio entre precisión y rendimiento
- Dimensionalidad adecuada para corpus mixtos (empírico + teórico)
- Ampliamente probado en tareas de similitud semántica

### 7.2 Vectorización

Cada documento (comentario o fragmento teórico) fue transformado en un vector numérico que representa su significado semántico.

---

## 8. Almacenamiento Vectorial con ChromaDB

Los embeddings fueron almacenados en una base de datos vectorial local usando **ChromaDB**, lo que permitió:

- Persistencia del conocimiento
- Búsqueda semántica eficiente
- Recuperación contextual de información relevante

La base se generó desde cero para evitar contaminación de datos previos.

---

## 9. Arquitectura RAG (Retrieval-Augmented Generation)

### 9.1 Motivación

En lugar de generar respuestas basadas únicamente en el modelo de lenguaje, se implementó un sistema **RAG** para:

- Anclar las respuestas en datos reales
- Evitar alucinaciones
- Forzar el contraste entre experiencia empírica y teoría

---

## 10. Integración con Ollama y LLM Local

### 10.1 Modelo Utilizado

- **LLM:** `llama3.1`
- Ejecutado localmente mediante **Ollama**

Ventajas clave:
- Privacidad total de los datos
- Control del pipeline
- Reproducibilidad académica

---

## 11. Prompt Engineering y Rol del Modelo

El modelo fue instruido explícitamente para:

- Analizar testimonios como evidencia empírica
- Contrastar con teoría filosófica
- No inventar información fuera del corpus
- Mantener un tono analítico y académico

Se definió al modelo como un **filósofo y sociólogo digital**, no como un asistente genérico.

---

## 12. Pipeline Técnico (Resumen)

1. Carga de PDFs teóricos  
2. Carga y limpieza de CSV empíricos  
3. Conversión a documentos LangChain  
4. Generación de embeddings  
5. Almacenamiento en ChromaDB  
6. Recuperación semántica (`k=5`)  
7. Generación de respuestas con contexto controlado  