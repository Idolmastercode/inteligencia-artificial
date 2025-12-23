# Proyecto: Visualizador del Algoritmo A* y Tablero Pixel Art

## Descripción General

Este proyecto consiste en una **aplicación gráfica desarrollada con Pygame** que permite visualizar el funcionamiento del **algoritmo de búsqueda A\*** de forma interactiva.  
Adicionalmente, el programa incluye un **modo alternativo de Pixel Art**, reutilizando la misma lógica de tablero.

El objetivo principal del proyecto es **comprender y demostrar el funcionamiento del algoritmo A\***, así como practicar programación gráfica, manejo de eventos y estructuras de datos.

---

## Modos de Operación

Al iniciar el programa, el usuario puede elegir entre dos modos:

### 1. Modo A* (Pathfinding)

- Permite crear un tablero configurable
- Selección manual de:
  - Nodo inicio
  - Nodo final
  - Obstáculos (paredes)
- Visualización paso a paso del algoritmo
- Animación del camino final encontrado

### 2. Modo Pixel Art

- El tablero funciona como una cuadrícula para dibujo
- El usuario puede pintar y borrar celdas
- Paleta de colores seleccionable por teclado
- Uso libre sin algoritmo de búsqueda

---

## Configuración del Tablero

El tamaño del tablero se solicita por consola antes de iniciar la ventana gráfica:

- Entrada flexible (`X Y` o `X,Y`)
- Validación de valores mínimos
- Tamaño dinámico de celdas según la resolución de la ventana

Esto permite probar el algoritmo en distintos escenarios sin modificar el código.

---

## Implementación del Algoritmo A*

### Representación del Nodo

Cada celda del tablero se representa como un objeto `Nodo`, el cual contiene:

- Posición (fila, columna)
- Estado visual (inicio, fin, pared, camino, etc.)
- Dimensiones gráficas

Para la lógica del algoritmo, se utiliza una clase extendida `NodoAStar`, que añade:

- Costo acumulado (`g`)
- Heurística (`h`)
- Costo total (`f = g + h`)
- Referencia al nodo padre
- Lista de vecinos

---

## Heurística y Movimientos

- Heurística utilizada: **distancia Manhattan**
- Movimientos permitidos:
  - Cardinales (arriba, abajo, izquierda, derecha)
  - Diagonales
- Costo:
  - Movimiento recto: 10
  - Movimiento diagonal: 15
- Se evita el “corte de esquinas” cuando hay paredes adyacentes

---

## Estructuras de Datos

- **Lista Abierta (LA):** nodos pendientes por evaluar
- **Lista Cerrada (LC):** nodos ya evaluados
- Almacenadas como diccionarios para acceso rápido

En cada iteración se selecciona el nodo con menor costo total (`f`).

---

## Visualización y Animación

Durante la ejecución del algoritmo:

- LA y LC se muestran con colores distintos
- El camino final se dibuja progresivamente
- Se incluye una animación del recorrido
- Elementos gráficos opcionales (sprites) para inicio y meta

Esto permite observar claramente cómo A* explora el espacio.

---

## Controles Principales (Modo A*)

- **Click izquierdo:**  
  - Primer click: inicio  
  - Segundo click: fin  
  - Siguientes: paredes
- **Click derecho:** borrar nodo
- **Barra espaciadora:** iniciar algoritmo
- **Tecla C:** limpiar tablero completo

---

## Controles Principales (Modo Pixel Art)

- **Click izquierdo:** pintar
- **Click derecho:** borrar
- **Teclas 1–6:** selección de colores
- **Tecla C:** limpiar tablero

---

## Tecnologías Utilizadas

- Lenguaje: **Python**
- Librería gráfica: **Pygame**
- Paradigma: Programación orientada a objetos

No se utilizaron modelos de IA ni librerías externas adicionales.

---

## Conclusión

Este proyecto cumple como una **implementación clara y funcional del algoritmo A\***, permitiendo visualizar su comportamiento en tiempo real.  
El modo Pixel Art añade un componente práctico adicional y demuestra la reutilización del mismo tablero para diferentes propósitos.

El enfoque del proyecto es **didáctico y visual**, ideal para comprender algoritmos de búsqueda y lógica de navegación en grafos.
