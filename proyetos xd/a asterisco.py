import pygame
import sys
import os

### Setup: Entrada de Usuario por Consola ###
def obtener_tamano_consola():
    """ Valida la entrada de (Ancho, Alto) desde la consola. Soporta "X Y" o "X,Y". """
    print("--- Configuración del Tablero ---")
    print("Introduce el tamaño (ej. 25 20  o  25,20)")
    print("O introduce solo el Ancho, presiona Enter, y luego el Alto.")
    
    while True:
        try:
            linea = input("Tamaño (Ancho Alto): ").strip()
            partes = linea.replace(',', ' ').split()
            
            if len(partes) == 2:
                cols = int(partes[0]) 
                filas = int(partes[1]) 
                if cols > 1 and filas > 1:
                    return cols, filas
            elif len(partes) == 1:
                cols = int(partes[0])
                filas_str = input(f"Ancho {cols}. Introduce Alto (Filas): ").strip()
                filas = int(filas_str)
                if cols > 1 and filas > 1:
                    return cols, filas
            
            print("Entrada inválida. Inténtalo de nuevo (ej. 25 20).")
            
        except ValueError:
            print("Entrada inválida (deben ser números). Inténtalo de nuevo.")
        except EOFError:
            print("Entrada cancelada. Usando 25x25 por defecto.")
            return 25, 25

### NUEVA FUNCIÓN: Selección de Modo ###
def obtener_modo_juego():
    """ Pide al usuario que elija entre A* y Pixel Art. """
    print("\n--- Modo de Operación ---")
    while True:
        modo = input("Elige modo: [1] A* Pathfinding  [0] Pixel Art: ").strip()
        if modo == '1':
            print("Modo A* seleccionado.")
            return 1
        if modo == '0':
            print("Modo Pixel Art seleccionado.")
            return 0
        print("Entrada inválida. Escribe 1 o 0.")


# --- Punto de entrada principal ---
if __name__ == "__main__":
    COLS, FILAS = obtener_tamano_consola()
    MODO_JUEGO = obtener_modo_juego()
    
    ### Inicialización de Pygame y Ventana ###
    pygame.init()
    pygame.font.init()

    ANCHO_VENTANA = 600
    ALTO_VENTANA = 600
    VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    
    if MODO_JUEGO == 1:
        pygame.display.set_caption("Visualizador A* Temática Chivas")
    else:
        pygame.display.set_caption("Pixel Art Board")
    
    # Imprimir instrucciones de Pixel Art si es el caso
    if MODO_JUEGO == 0:
        print("\n--- Controles Pixel Art ---")
        print("Click Izq: Pintar")
        print("Click Der: Borrar (Blanco)")
        print("Teclas 1-6: Seleccionar color")
        print("  [1] Negro")
        print("  [2] Rojo (Chivas)")
        print("  [3] Azul (Chivas)")
        print("  [4] Amarillo")
        print("  [5] Verde")
        print("  [6] Gris (Pared)")
        print("[C]: Limpiar todo")

else:
    print("Este script debe ejecutarse directamente.")
    sys.exit()


### Constantes de Color (Temática y Pixel Art) ###
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0) # Nuevo
GRIS = (128, 128, 128)
GRIS_OSCURO = (100, 100, 100) # Paredes
CHIVAS_ROJO = (205, 16, 34)
CHIVAS_AZUL = (0, 75, 135)
CHIVAS_AZUL_OSCURO = (0, 33, 71)
AZUL_CLARO = (173, 216, 230) # Lista Cerrada (LC)
ROJO_CLARO = (240, 128, 128) # Lista Abierta (LA)
AMARILLO_PIXEL = (255, 235, 59)
VERDE_PIXEL = (76, 175, 80)

# Paleta A*
COLOR_INICIO = CHIVAS_AZUL
COLOR_FIN = CHIVAS_AZUL_OSCURO
COLOR_PARED = GRIS_OSCURO
COLOR_CAMINO = CHIVAS_ROJO
COLOR_LA = ROJO_CLARO
COLOR_LC = AZUL_CLARO

### Clase: Nodo (Visual) ###
class Nodo:
    def __init__(self, fila, col, ancho_nodo_x, ancho_nodo_y, total_filas, total_cols):
        self.fila = fila
        self.col = col
        self.x = col * ancho_nodo_x
        self.y = fila * ancho_nodo_y
        self.color = BLANCO
        self.ancho_x = ancho_nodo_x
        self.ancho_y = ancho_nodo_y
        self.total_filas = total_filas
        self.total_cols = total_cols

    def get_pos(self):
        return self.fila, self.col
    def es_pared(self):
        return self.color == COLOR_PARED
    def es_inicio(self):
        return self.color == COLOR_INICIO
    def es_fin(self):
        return self.color == COLOR_FIN
    def restablecer(self):
        self.color = BLANCO
    def hacer_inicio(self):
        self.color = COLOR_INICIO
    def hacer_pared(self):
        self.color = COLOR_PARED
    def hacer_fin(self):
        self.color = COLOR_FIN
    def hacer_la(self):
        self.color = COLOR_LA
    def hacer_lc(self):
        self.color = COLOR_LC
    def hacer_camino(self):
        self.color = COLOR_CAMINO

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho_x, self.ancho_y))

### Clase: NodoAStar (Lógica Algoritmo) ###
class NodoAStar(Nodo):
    def __init__(self, fila, col, ancho_nodo_x, ancho_nodo_y, total_filas, total_cols, padre=None, distancia=None, h=None):
        super().__init__(fila, col, ancho_nodo_x, ancho_nodo_y, total_filas, total_cols)
        if distancia is not None and h is not None:
            self.distancia = distancia
            self.h = h
            self.total = distancia + h
            self.padre = padre
        else:
            self.distancia = float("inf")
            self.h = float("inf")
            self.total = float("inf")
            self.padre = None
        self.vecinos = []

    # Lógica de Vecinos (incl. diagonales y anti-corte de esquinas)
    def actualizar_vecinos(self, grid, fin):
        self.vecinos = []
        
        # --- Movimientos Cardinales ---
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_pared():
            self.vecinos.append(NodoAStar(grid[self.fila + 1][self.col].fila, grid[self.fila + 1][self.col].col, 
                                          self.ancho_x, self.ancho_y, self.total_filas, self.total_cols, 
                                          self, self.distancia + 10, 
                                          abs(fin.fila - (self.fila + 1)) * 10 + abs(fin.col - self.col) * 10))
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_pared():
            self.vecinos.append(NodoAStar(grid[self.fila - 1][self.col].fila, grid[self.fila - 1][self.col].col, 
                                          self.ancho_x, self.ancho_y, self.total_filas, self.total_cols, 
                                          self, self.distancia + 10, 
                                          abs(fin.fila - (self.fila - 1)) * 10 + abs(fin.col - self.col) * 10))
        if self.col < self.total_cols - 1 and not grid[self.fila][self.col + 1].es_pared():
            self.vecinos.append(NodoAStar(grid[self.fila][self.col + 1].fila, grid[self.fila][self.col + 1].col, 
                                          self.ancho_x, self.ancho_y, self.total_filas, self.total_cols, 
                                          self, self.distancia + 10, 
                                          abs(fin.fila - self.fila) * 10 + abs(fin.col - (self.col + 1)) * 10))
        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared():
            self.vecinos.append(NodoAStar(grid[self.fila][self.col - 1].fila, grid[self.fila][self.col - 1].col, 
                                          self.ancho_x, self.ancho_y, self.total_filas, self.total_cols, 
                                          self, self.distancia + 10, 
                                          abs(fin.fila - self.fila) * 10 + abs(fin.col - (self.col - 1)) * 10))
                                          
        # --- Movimientos Diagonales ---
        if self.fila < self.total_filas - 1 and self.col < self.total_cols - 1 and \
           not grid[self.fila + 1][self.col + 1].es_pared():
            if not grid[self.fila + 1][self.col].es_pared() or not grid[self.fila][self.col + 1].es_pared():
                self.vecinos.append(NodoAStar(grid[self.fila + 1][self.col + 1].fila, grid[self.fila + 1][self.col + 1].col, 
                                              self.ancho_x, self.ancho_y, self.total_filas, self.total_cols, 
                                              self, self.distancia + 15, 
                                              abs(fin.fila - (self.fila + 1)) * 10 + abs(fin.col - (self.col + 1)) * 10))
        if self.fila < self.total_filas - 1 and self.col > 0 and \
           not grid[self.fila + 1][self.col - 1].es_pared():
            if not grid[self.fila + 1][self.col].es_pared() or not grid[self.fila][self.col - 1].es_pared():
                self.vecinos.append(NodoAStar(grid[self.fila + 1][self.col - 1].fila, grid[self.fila + 1][self.col - 1].col, 
                                              self.ancho_x, self.ancho_y, self.total_filas, self.total_cols, 
                                              self, self.distancia + 15, 
                                              abs(fin.fila - (self.fila + 1)) * 10 + abs(fin.col - (self.col - 1)) * 10))
        if self.fila > 0 and self.col < self.total_cols - 1 and \
           not grid[self.fila - 1][self.col + 1].es_pared():
            if not grid[self.fila - 1][self.col].es_pared() or not grid[self.fila][self.col + 1].es_pared():
                self.vecinos.append(NodoAStar(grid[self.fila - 1][self.col + 1].fila, grid[self.fila - 1][self.col + 1].col, 
                                              self.ancho_x, self.ancho_y, self.total_filas, self.total_cols, 
                                              self, self.distancia + 15, 
                                              abs(fin.fila - (self.fila - 1)) * 10 + abs(fin.col - (self.col + 1)) * 10))
        if self.fila > 0 and self.col > 0 and \
           not grid[self.fila - 1][self.col - 1].es_pared():
            if not grid[self.fila - 1][self.col].es_pared() or not grid[self.fila][self.col - 1].es_pared():
                self.vecinos.append(NodoAStar(grid[self.fila - 1][self.col - 1].fila, grid[self.fila - 1][self.col - 1].col, 
                                              self.ancho_x, self.ancho_y, self.total_filas, self.total_cols, 
                                              self, self.distancia + 15, 
                                              abs(fin.fila - (self.fila - 1)) * 10 + abs(fin.col - (self.col - 1)) * 10))

### Funciones Auxiliares (Grid y UI) ###
def crear_grid(filas, cols):
    grid = []
    ancho_nodo_x = ANCHO_VENTANA // cols
    ancho_nodo_y = ALTO_VENTANA // filas
    
    for i in range(filas):
        grid.append([])
        for j in range(cols):
            nodo = Nodo(i, j, ancho_nodo_x, ancho_nodo_y, filas, cols)
            grid[i].append(nodo)
    return grid

def dibujar_grid_lines(ventana, filas, cols):
    ancho_nodo_x = ANCHO_VENTANA // cols
    ancho_nodo_y = ALTO_VENTANA // filas
    
    for i in range(filas + 1):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo_y), (ANCHO_VENTANA, i * ancho_nodo_y))
    for j in range(cols + 1):
        pygame.draw.line(ventana, GRIS, (j * ancho_nodo_x, 0), (j * ancho_nodo_x, ALTO_VENTANA))

def dibujar(ventana, grid, filas, cols):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

def obtener_click_pos(pos, filas, cols):
    ancho_nodo_x = ANCHO_VENTANA // cols
    ancho_nodo_y = ALTO_VENTANA // filas
    x_mouse, y_mouse = pos
    
    fila = int(y_mouse // ancho_nodo_y)
    col = int(x_mouse // ancho_nodo_x)

    if fila >= filas: fila = filas - 1
    if col >= cols: col = cols - 1
        
    return fila, col

### Bucle Principal (main) ###
def main(ventana, filas, cols, modo_juego):
    grid = crear_grid(filas, cols)
    corriendo = True
    clock = pygame.time.Clock()

    # --- Variables de estado A* ---
    inicio = None
    fin = None
    algoritmo_iniciado = False
    dibujando_camino = False
    actual = None
    la = {} # Lista Abierta
    lc = {} # Lista Cerrada
    camino_final = []
    indice_camino = 0
    
    # --- Variables de estado Pixel Art ---
    color_actual_pixelart = NEGRO

    ### CARGA DE IMÁGENES ###
    IMAGENES_CARGADAS = False
    chiva_img = None
    trofeo_img = None
    
    if modo_juego == 1:
        ancho_nodo_x = ANCHO_VENTANA // cols
        ancho_nodo_y = ALTO_VENTANA // filas
        
        ruta_chiva = "chiva.png"
        ruta_trofeo = "trofeo.png"
        
        if not os.path.exists(ruta_chiva):
            print(f"Advertencia: No se encontró '{ruta_chiva}'. La chiva no se mostrará.")
        if not os.path.exists(ruta_trofeo):
            print(f"Advertencia: No se encontró '{ruta_trofeo}'. El trofeo no se mostrará.")

        try:
            if os.path.exists(ruta_chiva):
                chiva_img_orig = pygame.image.load(ruta_chiva).convert_alpha()
                chiva_img = pygame.transform.scale(chiva_img_orig, (ancho_nodo_x, ancho_nodo_y))
            
            if os.path.exists(ruta_trofeo):
                trofeo_img_orig = pygame.image.load(ruta_trofeo).convert_alpha()
                trofeo_img = pygame.transform.scale(trofeo_img_orig, (ancho_nodo_y, ancho_nodo_y))
            
            if chiva_img or trofeo_img:
                IMAGENES_CARGADAS = True
                
        except pygame.error as e:
            print(f"Error al cargar imágenes: {e}")
            IMAGENES_CARGADAS = False

    while corriendo:
        # --- MANEJO DE EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            # ==================================
            # --- LÓGICA MODO A* (PATHFINDING) ---
            # ==================================
            if modo_juego == 1:
                if algoritmo_iniciado:
                    continue

                # Click izquierdo (A*)
                if pygame.mouse.get_pressed()[0]:  
                    pos = pygame.mouse.get_pos()
                    fila, col = obtener_click_pos(pos, filas, cols)
                    if fila < 0 or col < 0: continue 
                    nodo = grid[fila][col]
                    
                    if not inicio and nodo != fin:
                        inicio = nodo
                        inicio.hacer_inicio()
                    elif not fin and nodo != inicio:
                        fin = nodo
                        fin.hacer_fin()
                    elif nodo != fin and nodo != inicio:
                        nodo.hacer_pared()

                # Click derecho (A*)
                elif pygame.mouse.get_pressed()[2]: 
                    pos = pygame.mouse.get_pos()
                    fila, col = obtener_click_pos(pos, filas, cols)
                    if fila < 0 or col < 0: continue
                    nodo = grid[fila][col]
                    nodo.restablecer()
                    if nodo == inicio:
                        inicio = None
                    elif nodo == fin:
                        fin = None

            # ============================
            # --- LÓGICA MODO PIXEL ART ---
            # ============================
            elif modo_juego == 0:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    fila, col = obtener_click_pos(pos, filas, cols)
                    if fila < 0 or col < 0: continue
                    nodo = grid[fila][col]
                    nodo.color = color_actual_pixelart
                
                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    fila, col = obtener_click_pos(pos, filas, cols)
                    if fila < 0 or col < 0: continue
                    nodo = grid[fila][col]
                    nodo.restablecer()
            
            # --- CONTROLES DE TECLADO (Compartidos y Específicos) ---
            if event.type == pygame.KEYDOWN:
                
                # Teclas específicas de A*
                if modo_juego == 1:
                    if event.key == pygame.K_SPACE and inicio and fin:
                        la = {}
                        lc = {}
                        camino_final = []
                        indice_camino = 0
                        
                        actual = NodoAStar(inicio.fila, inicio.col, inicio.ancho_x, inicio.ancho_y, inicio.total_filas, inicio.total_cols, None, 0, 0)
                        la[(actual.fila, actual.col)] = actual 
                        algoritmo_iniciado = True
                        dibujando_camino = False
                
                # Teclas específicas de Pixel Art (Paleta)
                elif modo_juego == 0:
                    if event.key == pygame.K_1:
                        color_actual_pixelart = NEGRO
                    elif event.key == pygame.K_2:
                        color_actual_pixelart = CHIVAS_ROJO
                    elif event.key == pygame.K_3:
                        color_actual_pixelart = CHIVAS_AZUL
                    elif event.key == pygame.K_4:
                        color_actual_pixelart = AMARILLO_PIXEL
                    elif event.key == pygame.K_5:
                        color_actual_pixelart = VERDE_PIXEL
                    elif event.key == pygame.K_6:
                        color_actual_pixelart = GRIS_OSCURO
                
                # Tecla 'C' (Universal para limpiar)
                if event.key == pygame.K_c:
                    inicio = None
                    fin = None
                    grid = crear_grid(filas, cols)
                    algoritmo_iniciado = False
                    dibujando_camino = False
                    actual = None
                    la = {}
                    lc = {}
                    camino_final = []
                    indice_camino = 0
                    color_actual_pixelart = NEGRO # Resetear color
                
        ### Lógica Central A* (Step-by-Step) - SOLO MODO 1 ###
        if modo_juego == 1 and algoritmo_iniciado:
            if not la:
                print("No hay camino posible")
                algoritmo_iniciado = False
                continue 

            minValue = min(la.values(), key=lambda x: x.total).total
            actual = None
            for key in list(la.keys()): 
                if la[key].total == minValue:
                    actual = la.pop(key) 
                    break
            
            lc[(actual.fila, actual.col)] = actual
            
            if (actual.fila, actual.col) != (inicio.fila, inicio.col) and \
               (actual.fila, actual.col) != (fin.fila, fin.col):
                grid[actual.fila][actual.col].hacer_lc()
            
            # --- CAMINO ENCONTRADO ---
            if actual.fila == fin.fila and actual.col == fin.col:
                print("Camino encontrado")
                algoritmo_iniciado = False
                
                temp = actual
                while temp:
                    camino_final.append(temp)
                    temp = temp.padre
                camino_final.reverse() 
                
                indice_camino = 0
                dibujando_camino = True 
                continue 

            actual.actualizar_vecinos(grid, fin)

            for vecino in actual.vecinos:
                if lc.get((vecino.fila, vecino.col)) is not None:
                    continue
                
                nodo_en_la = la.get((vecino.fila, vecino.col))
                
                if nodo_en_la is None or vecino.total < nodo_en_la.total:
                    la[(vecino.fila, vecino.col)] = vecino
                    if (vecino.fila, vecino.col) != (fin.fila, fin.col):
                        grid[vecino.fila][vecino.col].hacer_la()

        ### LÓGICA DE ANIMACIÓN (SOLO MODO 1) ###
        elif modo_juego == 1 and dibujando_camino:
            if indice_camino < len(camino_final):
                nodo_actual_camino = camino_final[indice_camino]
                if not (nodo_actual_camino.es_inicio() or nodo_actual_camino.es_fin()):
                    grid[nodo_actual_camino.fila][nodo_actual_camino.col].hacer_camino()
                indice_camino += 1

        
        ### Ciclo de Renderizado (Universal) ###
        
        # 1. Fondo y nodos (colores)
        dibujar(ventana, grid, filas, cols)
        
        # 2. Rejilla
        dibujar_grid_lines(ventana, filas, cols)

        # 3. Sprites (Solo A*)
        if modo_juego == 1 and IMAGENES_CARGADAS:
            
            if fin and trofeo_img:
                ventana.blit(trofeo_img, (fin.x, fin.y))
            
            if chiva_img:
                if dibujando_camino:
                    idx_actual = max(0, indice_camino - 1) 
                    if idx_actual < len(camino_final):
                        nodo_chiva = camino_final[idx_actual]
                        ventana.blit(chiva_img, (nodo_chiva.x, nodo_chiva.y))
                
                elif len(camino_final) > 0 and fin:
                    ventana.blit(chiva_img, (fin.x, fin.y))
                
                elif inicio:
                    ventana.blit(chiva_img, (inicio.x, inicio.y))

        # 4. Flip del buffer
        pygame.display.update()

        # 5. Control de FPS (Tick)
        if modo_juego == 1 and dibujando_camino and indice_camino < len(camino_final):
            clock.tick(10) # Tick lento durante la animación del path
        else:
            clock.tick(60) # Tick normal en modo edición o pixel art
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(VENTANA, FILAS, COLS, MODO_JUEGO)