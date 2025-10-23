# 🧭 Algoritmo A* con Distancia Manhattan

El **algoritmo A\*** (A estrella) es un método de **búsqueda de caminos óptimos** usado en mapas o planos, como en videojuegos o robots, para ir desde un punto inicial hasta un destino evitando obstáculos.

---

## ⚙️ Funcionamiento básico

Cada casilla o nodo tiene tres valores:
- **g:** costo desde el inicio hasta el nodo actual.  
- **h:** estimación del costo hasta el objetivo (heurística).  
- **f = g + h:** costo total estimado (se elige el nodo con menor *f*).

---

## 📏 Distancia Manhattan

Para planos en cuadrícula (movimiento en 4 direcciones), la heurística más común es la **distancia Manhattan**:

\[
h = |x₁ - x₂| + |y₁ - y₂|
\]

Es decir, la suma de los pasos horizontales y verticales necesarios para llegar.

---

## 🧩 Proceso general

1. Inicia desde el nodo inicial y calcula su `f`.
2. Expande el nodo con menor `f` (prioridad).
3. Calcula `g`, `h` y `f` para sus vecinos.
4. Repite hasta alcanzar el destino o agotar los nodos.