# ♟️ Recorrido del Caballo — Tablero de Ajedrez

El **tablero de ajedrez** tiene **8 filas × 8 columnas**, es decir **64 casillas** alternadas entre blancas y negras.

El **caballo** se mueve en forma de **“L”**, lo que significa:
- 2 casillas en una dirección (vertical u horizontal)  
- y luego 1 casilla perpendicularmente.

Ejemplo de movimientos válidos desde una posición:
. . X . .
. X . X .
. . ♞ . .
. X . X .
. . X . .

---

## 🎯 Objetivo del juego

El reto consiste en mover el **caballo** de manera que **visite todas las casillas del tablero exactamente una vez** sin repetir ninguna posición.  
Este problema se conoce como el **“Paseo del Caballo”** (*Knight’s Tour*).

---

## 🧠 Lógica básica de solución

1. Elige una casilla inicial (por ejemplo, esquina A1).  
2. En cada paso, selecciona un movimiento válido no visitado.  
3. Si quedas sin movimientos disponibles antes de cubrir todas las casillas, retrocede (backtracking).  
4. Repite hasta recorrer las 64 posiciones.

---

## ⚙️ Heurística de Warnsdorff (versión eficiente)

En lugar de probar todo al azar, se sigue esta regla:
> “Siempre mueve el caballo a la casilla que tenga **menos movimientos disponibles a futuro**.”

Esto reduce los bloqueos y permite encontrar recorridos completos sin retrocesos.

---

✅ **Resumen:**
El **recorrido del caballo** combina geometría y algoritmos (búsqueda o heurística).  
Aunque parece simple, requiere **planificación inteligente** para lograr visitar las 64 casillas sin repetir ninguna.
