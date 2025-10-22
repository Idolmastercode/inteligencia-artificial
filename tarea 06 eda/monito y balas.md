# 💥 Juego de Balas Rebote — Esquiva del Monito

## 🎯 Objetivo
El jugador controla a un **monito** que debe **esquivar una pelota** que rebota dentro de un área cerrada.  
La pelota cambia de dirección al chocar con los bordes, y el monito puede **moverse**, **saltar** o **quedarse quieto** según la situación.

---

## 🧠 Lógica de la Solución
Para que el monito decida qué hacer (moverse, saltar o no hacer nada), el sistema evalúa:

### 🔹 Parámetros de la pelota
- **Posición:** (X, Y)  
- **Velocidad:** (Vx, Vy)  
- **Hitbox:** ancho, altura  

### 🔹 Parámetros del monito
- **Posición:** (X, Y)  
- **Velocidad:** (Vx, Vy)  
- **Hitbox:** ancho, altura  

### 🔹 Parámetros del mapa
- **Dimensiones del área:** ancho, altura  

### 🔹 Cálculo clave
- **Distancia entre monito y pelota:**  
  `dist = sqrt((X_pelota - X_monito)² + (Y_pelota - Y_monito)²)`

---

## 🧩 Lógica de decisión
| Situación | Acción del monito |
|------------|------------------|
| Pelota cerca en trayectoria directa | Moverse horizontal o verticalmente |
| Pelota a distancia segura | Mantener posición |
| Rebote inesperado cercano | Movimiento evasivo rápido |