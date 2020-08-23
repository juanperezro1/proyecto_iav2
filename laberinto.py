import mapa
import busquedas
import numpy as np

class Laberinto:
    matriz_muros = [[]]
    tamano = []
    trampas = [[]]
    beneficio = [[]]
    matriz_beneficio = [[]]
    inicio = []
    meta = []
    matrizAyuda1 = []
    lista_solucion = [[]]

    
    
# Caminos libres 0, Obstaculos 1,  Enemigo (Fantasma) 2, Inicio (MrPacman) 3, Meta (Sra Pacman) 4

    def __init__(self):
        self.read_laberinto()

    def read_laberinto(self):
        
        self.matrizAyuda1 = mapa.leer_archivo()

        self.tamano.append(len(self.matrizAyuda1)+1)

        self.set_tamano()

        for i in range(len(self.matrizAyuda1)):
            for j in range(len(self.matrizAyuda1)):
                
                if(self.matrizAyuda1[i][j] == 2):   #Enemigo
                    self.trampas[i][j] = 1

                if(self.matrizAyuda1[i][j] == 3):  #Inicio
                    self.inicio.append(i)
                    self.inicio.append(j)
            
                if(self.matrizAyuda1[i][j] == 4):   #Meta
                    self.meta.append([i,j])

                if(self.matrizAyuda1[i][j] == 1):    #Bloques
                    self.matriz_muros[i][j] = 1

                    self.matriz_muros = np.array(self.matriz_muros)
                    matriz_unos = np.ones(len(self.matriz_muros))

                    self.matriz_muros[len(self.matriz_muros)-1] = matriz_unos
                    self.matriz_muros[:,len(self.matriz_muros)-1] = matriz_unos

                if(self.matrizAyuda1[i][j] == 5):   #Enemigo
                    self.beneficio[i][j] = 1

    #Espinaca power: a partir de la posición de la espinaca setea el camino hasta la meta con unos (1)

    def poder_espinaca(self,lista_solucion,costo_solucion):

        pos_espinaca_lista_solucion = None

        #Se obtiene la posición de la espinaca
        posicion_espinaca = []
        for i in range(len(self.matrizAyuda1)):
            for j in range(len(self.matrizAyuda1)):
                    if(self.matrizAyuda1[i][j] == 5):
                        posicion_espinaca.append([i,j])

        #Se verifica que el Pacman pasará por la espinaca. Se evalua si la posición de la espinaca coincide con la posible
        #posición solución del Pacman y se obtiene la posición
                
        for solucion in lista_solucion:
            for indice in posicion_espinaca:
                if (solucion[0],solucion[1]) == (indice[0],indice[1]):
                    pos_espinaca_lista_solucion = lista_solucion.index(posicion_espinaca[0])
                    pos_espinaca_lista_solucion = pos_espinaca_lista_solucion + 1
                    
        #Con la posición se realiza un recorte a la lista solución y se le agrega 1 despues de la espinaca

        if pos_espinaca_lista_solucion != None:
            camino_espinaca = lista_solucion[pos_espinaca_lista_solucion:]
            
            for i in range(len(self.beneficio)):
                for j in range(len(self.beneficio)): 
                    for indice in camino_espinaca:
                        if([i,j] == [indice[0],indice[1]]):
                            self.beneficio[i][j] = 1
            
            matriz_power_espinaca = self.beneficio

            contador_poder = 0
            
            #Realiza la reducción del costo al pasar por un bloque (si ha tomado la espinaca)
            for i in range(len(matriz_power_espinaca)):
                for j in range(len(matriz_power_espinaca)):
                    if(matriz_power_espinaca[i][j] == 1):
                        contador_poder += 0.5
                    
            costo_con_poder = abs(-costo_solucion + contador_poder)
            print("El costo con el poder de la espinaca es: ",costo_con_poder)

        else:
            print("El costo de la solución es: ",costo_solucion)

    #Se inicializan en 0 las matrices que se usaran 
    def set_tamano(self):
        self.trampas = [[0 for i in range(self.tamano[0])] for i in range(self.tamano[0])]
        self.beneficio = [[0 for i in range(self.tamano[0])] for i in range(self.tamano[0])]
        self.matriz_muros = [[0 for i in range(self.tamano[0])] for i in range(self.tamano[0])]

    #Verifica si el jugador puede pasar, es decir, no tiene un obstaculo al rededor   
    def puede_pasar(self, fila, columna, direccion):

        if direccion == "derecha":
            #Si existe un muro a la derecha del Pacman retornara que este no podra pasar (existe bloque)
            if self.matriz_muros[fila][columna + 1] == 1:
                return False
            #De lo contrario retornara True si puede pasar (no existe bloque)
            return self.matriz_muros[fila][columna + 1] == 0

        elif direccion == "abajo":
            if self.matriz_muros[fila + 1][columna] == 1:
                return False
            return self.matriz_muros[fila + 1][columna] == 0

        elif direccion == "izquierda":
            if self.matriz_muros[fila][columna - 1] == 1:
                return False
            return self.matriz_muros[fila][columna - 1] == 0

        elif direccion == "arriba":
            if self.matriz_muros[fila - 1][columna] == 1:
                return False
            return self.matriz_muros[fila - 1][columna] == 0


