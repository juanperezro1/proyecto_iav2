import re
import mapa
import search
import numpy as np

class Maze:

    matriz_muros = [[]]
    tamano = []
    trampas = [[]]
    beneficio = [[]]
    inicio = []
    meta = []
    matrizAyuda1 = []
    lista_solucion = [[]]
    matriz_beneficio =[[]]
    
# Caminos libres 0
# Enemigos(Fantasmas) 4 , Inicio(Mr Pacman) 5 , Meta(Sra Pacman) 6 

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
                    #print("tamanoooo",len(self.matriz_muros))
                    self.matriz_muros[:,len(self.matriz_muros)-1] = matriz_unos
                    #print(self.matriz_muros)
                    #print("sdasdas",self.matriz_muros)

    #Espinaca power
    def funcion(self,lista_solucion):
        pass
        """
        #print(self.matrizAyuda1)
        posicion_espinaca = []
        for i in range(len(self.matrizAyuda1)):
            for j in range(len(self.matrizAyuda1)):
                    if(self.matrizAyuda1[i][j] == 5):
                        posicion_espinaca.append([i,j])        
        #cont = 0
        for solucion in lista_solucion:
            for indice in posicion_espinaca:
                if (solucion[0],solucion[1]) == (indice[0],indice[1]):
                    pos_espinaca_lista_solucion = lista_solucion.index(posicion_espinaca[0])
                
        camino_espinaca = lista_solucion[pos_espinaca_lista_solucion:]
        #print(camino_espinaca)

        for i in range(len(self.beneficio)):
            for j in range(len(self.beneficio)): 
                for indice in camino_espinaca:
                    if([i,j] == [indice[0],indice[1]]):
                        
                        self.beneficio[i][j] = 1
        
        matriz_beneficio = self.beneficio
        print("holii",matriz_beneficio)
        """
    #Tamaño matrices 

    def set_tamano(self):
        # Lastly we will fill wall and trap arrays with zero.

        self.trampas = [[0 for i in range(self.tamano[0])] for i in range(self.tamano[0])]
        self.beneficio = [[0 for i in range(self.tamano[0]-1)] for i in range(self.tamano[0]-1)]
        self.matriz_muros = [[0 for i in range(self.tamano[0])] for i in range(self.tamano[0])]

        """
        self.beneficio = [[0,0,0,0,0,0,0,0],
                          [0,0,0,0,1,1,0,0],
                          [0,0,0,0,0,1,1,0],
                          [0,0,0,0,0,0,1,0],
                          [0,0,0,0,0,1,1,0],
                          [0,0,0,1,1,1,0,0],
                          [0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0]]
        """ 

    def puede_pasar(self, fila, columna, direccion):
        # Check if the player can pass
        if direccion == "derecha":
            if self.matriz_muros[fila][columna] == 1:
                return False
            # Return True if there is no blocking wall on derecha side. Otherwise, return False.
            return self.matriz_muros[fila][columna] == 0
        elif direccion == "abajo":
            if self.matriz_muros[fila][columna] == 1:
                return False
            return self.matriz_muros[fila][columna] == 0
        elif direccion == "izquierda":
            if self.matriz_muros[fila][columna] == 1:
                return False
            return self.matriz_muros[fila][columna - 1] == 0
        elif direccion == "arriba":
            if self.matriz_muros[fila][columna] == 1:
                return False
            return self.matriz_muros[fila - 1][columna] == 0


