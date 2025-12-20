import json
import os

# Nombre del archivo Notebook que vamos a generar
notebook_filename = "CNN_Final_Pro.ipynb"

# ==============================================================================
# CONTENIDO DE LAS CELDAS (EL CÓDIGO BLINDADO ADAPTADO A TU FORMATO)
# ==============================================================================

# 1. IMPORTS Y CONFIGURACIÓN GPU
cell_imports = """import os
import gc
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import (
    Input, Dense, Dropout, Flatten, BatchNormalization,
    MaxPooling2D, Conv2D, LeakyReLU, Rescaling,
    RandomFlip, RandomRotation, RandomZoom
)
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import Callback, EarlyStopping
from tensorflow.keras.preprocessing import image

# Limpieza preventiva de memoria
tf.keras.backend.clear_session()
gc.collect()

# Configuración de GPU para evitar errores de memoria
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✅ GPU Detectada y Configurada: {gpus[0].name}")
    except RuntimeError as e:
        print(e)
else:
    print("⚠️ No se detectó GPU. Se usará CPU (puede ser lento).")"""

# 2. CARGA DE DATOS (REEMPLAZA AL OS.WALK VIEJO)
cell_load_data = """# Parámetros del Proyecto
IMG_SIZE = 224
BATCH_SIZE = 32  # Tamaño seguro para no saturar VRAM
EPOCHS = 100
INIT_LR = 1e-3

# Ruta del Dataset (Ajusta si es necesario)
dirname = os.path.join(os.getcwd(), 'Dataset')

if not os.path.exists(dirname):
    print(f"❌ ERROR: No encuentro la carpeta {dirname}")
else:
    print(f"📂 Cargando imágenes desde: {dirname}")

# --- AQUÍ ESTÁ EL TRUCO ---
# Usamos image_dataset_from_directory en lugar de cargar listas manuales.
# Esto evita que la RAM explote.
full_ds = tf.keras.utils.image_dataset_from_directory(
    dirname,
    label_mode='categorical',
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=13
)

class_names = full_ds.class_names
print(f"✅ Clases encontradas: {class_names}")"""

# 3. SPLITS Y PREPROCESAMIENTO (REEMPLAZA AL TRAIN_TEST_SPLIT)
cell_splits = """# División de Datos (70% Train, 15% Val, 15% Test)
# Se hace sobre el dataset dinámico, no sobre arrays en memoria.

total_batches = tf.data.experimental.cardinality(full_ds).numpy()
train_size = int(0.7 * total_batches)
val_size = int(0.15 * total_batches)
test_size = int(0.15 * total_batches)

train_ds = full_ds.take(train_size)
remaining = full_ds.skip(train_size)
val_ds = remaining.take(val_size)
test_ds = remaining.skip(val_size)

# Optimización de Flujo (AUTOTUNE)
# Permite cargar datos del disco mientras la GPU entrena.
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)

print(f"Estructura lista: Train({train_size} batches) | Val({val_size} batches) | Test({test_size} batches)")"""

# 4. MODELO CNN (ARQUITECTURA PROFUNDA + DATA AUGMENTATION)
cell_model = """# Definición del Modelo "Tanque" (Robusto contra basura y overfitting)
sport_model = Sequential()
sport_model.add(Input(shape=(IMG_SIZE, IMG_SIZE, 3)))

# --- BLOQUE 1: Data Augmentation ---
# Esto genera variaciones (rotación, zoom) en tiempo real para aprender mejor.
sport_model.add(RandomFlip("horizontal"))
sport_model.add(RandomRotation(0.1))
sport_model.add(RandomZoom(0.1))

# Normalización (Dentro del modelo para usar GPU)
sport_model.add(Rescaling(1./255)) 

# --- BLOQUE 2: Extracción de Características (Convoluciones) ---
# Capa 1 (32 filtros)
sport_model.add(Conv2D(32, kernel_size=(3, 3), activation='linear', padding='same'))
sport_model.add(LeakyReLU(negative_slope=0.1))
sport_model.add(BatchNormalization())
sport_model.add(MaxPooling2D((2, 2), padding='same'))
sport_model.add(Dropout(0.2))

# Capa 2 (64 filtros)
sport_model.add(Conv2D(64, kernel_size=(3, 3), activation='linear', padding='same'))
sport_model.add(LeakyReLU(negative_slope=0.1))
sport_model.add(BatchNormalization())
sport_model.add(MaxPooling2D(pool_size=(2, 2)))
sport_model.add(Dropout(0.3))

# Capa 3 (128 filtros)
sport_model.add(Conv2D(128, kernel_size=(3, 3), activation='linear', padding='same'))
sport_model.add(LeakyReLU(negative_slope=0.1))
sport_model.add(BatchNormalization())
sport_model.add(MaxPooling2D(pool_size=(2, 2)))
sport_model.add(Dropout(0.4))

# Capa 4 (256 filtros - Detalles finos)
sport_model.add(Conv2D(256, kernel_size=(3, 3), activation='linear', padding='same'))
sport_model.add(LeakyReLU(negative_slope=0.1))
sport_model.add(BatchNormalization())
sport_model.add(MaxPooling2D(pool_size=(2, 2)))
sport_model.add(Dropout(0.4))

# --- BLOQUE 3: Clasificación ---
sport_model.add(Flatten())
sport_model.add(Dense(128, activation='linear'))
sport_model.add(LeakyReLU(negative_slope=0.1))
sport_model.add(Dropout(0.5))
sport_model.add(Dense(len(class_names), activation='softmax'))

sport_model.summary()"""

# 5. COMPILACIÓN
cell_compile = """# Compilación con SGD + Momentum (Para estabilidad)
sport_model.compile(
    loss='categorical_crossentropy',
    optimizer=SGD(learning_rate=INIT_LR, momentum=0.9),
    metrics=['accuracy']
)"""

# 6. ENTRENAMIENTO
cell_train = """# Configuración de Callbacks
# 1. ClearMemory: Limpia RAM al final de cada época.
# 2. EarlyStopping: Detiene si no mejora en 12 épocas.

class ClearMemory(Callback):
    def on_epoch_end(self, epoch, logs=None):
        gc.collect()
        tf.keras.backend.clear_session()

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=12,
    restore_best_weights=True,
    verbose=1
)

print("🚀 Iniciando entrenamiento...")
history = sport_model.fit(
    train_ds, 
    epochs=EPOCHS,
    verbose=1,
    validation_data=val_ds,
    callbacks=[ClearMemory(), early_stop]
)

# Guardar el modelo entrenado
sport_model.save("modelo_final_cnn.h5")
print("💾 Modelo guardado exitosamente.")"""

# 7. EVALUACIÓN Y GRÁFICAS
cell_evaluate = """# Evaluación Final en Test Set
test_eval = sport_model.evaluate(test_ds, verbose=0)
print(f'📊 Accuracy Final (Test): {test_eval[1]:.2%}')
print(f'📉 Loss Final (Test): {test_eval[0]:.4f}')

# Gráficas de Rendimiento
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs_range = range(len(acc))

plt.figure(figsize=(16, 6))

plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, 'bo-', label='Training Accuracy')
plt.plot(epochs_range, val_acc, 'b-', linewidth=2, label='Validation Accuracy')
plt.title('Precisión (Accuracy)')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, 'ro-', label='Training Loss')
plt.plot(epochs_range, val_loss, 'r-', linewidth=2, label='Validation Loss')
plt.title('Pérdida (Loss)')
plt.legend()
plt.grid(True)
plt.show()"""

# 8. REPORTE DE CLASIFICACIÓN
cell_report = """# Generación de Reporte Detallado
print("Calculando predicciones detalladas...")
y_pred = []
y_true = []

# Iteramos sobre el dataset de test para obtener etiquetas reales vs predichas
for images, labels in test_ds:
    preds = sport_model.predict(images, verbose=0)
    y_pred.extend(np.argmax(preds, axis=1))
    y_true.extend(np.argmax(labels.numpy(), axis=1))

print("\\n--- CLASSIFICATION REPORT ---")
print(classification_report(y_true, y_pred, target_names=class_names))

# Matriz de Confusión (Opcional)
# cm = confusion_matrix(y_true, y_pred)
# print(cm)"""

# 9. ZONA DE PRUEBAS (DEMO)
cell_demo = """# =========================================
# 🧪 ZONA DE PRUEBA INDIVIDUAL (DEMO)
# =========================================
# Coloca una imagen en la carpeta y pon su nombre abajo para probarla.

def probar_imagen(nombre_archivo):
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    
    if not os.path.exists(ruta):
        print(f"⚠️ No encuentro el archivo: {nombre_archivo}")
        return

    # Cargar y preprocesar
    img = image.load_img(ruta, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) # Batch de 1

    # Predicción
    prediccion = sport_model.predict(img_array, verbose=0)
    score = tf.nn.softmax(prediccion[0])
    
    clase_detectada = class_names[np.argmax(score)]
    confianza = 100 * np.max(score)
    
    # Mostrar
    plt.figure(figsize=(5, 5))
    plt.imshow(img)
    color_txt = 'green' if confianza > 70 else 'red'
    plt.title(f"{clase_detectada.upper()}\\n({confianza:.2f}%)", color=color_txt, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.show()
    print(f"Resultado: {clase_detectada} con {confianza:.2f}% de seguridad.")

# --- ¡CAMBIA ESTO POR TU FOTO! ---
# Ejemplo: probar_imagen("mi_perro.jpg")
print("Usa la función probar_imagen('nombre.jpg') para testear.")"""

# ==============================================================================
# CONSTRUCCIÓN DEL JSON DEL NOTEBOOK
# ==============================================================================

notebook_structure = {
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": ["# CNN Final Pro: Clasificación de Imágenes"]},
  {"cell_type": "markdown", "metadata": {}, "source": ["## 1. Importación de Librerías y Configuración GPU"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell_imports]},
  
  {"cell_type": "markdown", "metadata": {}, "source": ["## 2. Carga del Dataset (Optimizado con Generadores)"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell_load_data]},
  
  {"cell_type": "markdown", "metadata": {}, "source": ["## 3. Preprocesamiento y Splits"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell_splits]},
  
  {"cell_type": "markdown", "metadata": {}, "source": ["## 4. Definición del Modelo (Data Augmentation + 4 Bloques)"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell_model]},
  
  {"cell_type": "markdown", "metadata": {}, "source": ["## 5. Compilación"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell_compile]},
  
  {"cell_type": "markdown", "metadata": {}, "source": ["## 6. Entrenamiento"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell_train]},
  
  {"cell_type": "markdown", "metadata": {}, "source": ["## 7. Evaluación y Gráficas de Resultados"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell_evaluate]},
  
  {"cell_type": "markdown", "metadata": {}, "source": ["## 8. Reporte de Clasificación (Precision/Recall)"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell_report]},
  
  {"cell_type": "markdown", "metadata": {}, "source": ["## 9. Prueba / Demo en Vivo"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell_demo]}
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {"name": "ipython", "version": 3},
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

# ESCRIBIR EL ARCHIVO
try:
    with open(notebook_filename, 'w', encoding='utf-8') as f:
        json.dump(notebook_structure, f, indent=1)
    print(f"✅ ¡ÉXITO! Se generó el archivo '{notebook_filename}'.")
    print(f"👉 Ahora abre Jupyter y ejecuta este archivo.")
except Exception as e:
    print(f"❌ Error al escribir el archivo: {e}")