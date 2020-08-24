import sys
from laberinto import Laberinto
from arbol_solucion import lista_solucion

class Nodo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.costo = 0
        self.padres = None
        self.derecha = None
        self.abajo = None
        self.izquierda = None
        self.arriba = None
        self.heuristica = 0

    def igualdad(self, x, y):
        return x == self.x and y == self.y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"
    
    def get_posicion(self):
        return [self.x, self.y]
    
class GrafoEnemigo:

    nodos = []  #Se crea una lista de nodos para evitar nodos iguales
    laberinto = None

    lista_nodos_padres = []
    lista_nodos_hijos = []

    def __init__(self):
        
        #Se crea el grafo
        self.laberinto = Laberinto()

        #La raiz del grafo es la posición inicial del Pacman 
        self.raiz = self.crear_nodo(self.laberinto.inicio_enemigo[0], self.laberinto.inicio_enemigo[1])

        #Se crea la heuristica

        #Se le asigna un costo de 0 al nodo raiz 
        self.raiz.costo = 0

    def crear_nodo(self, x, y):
        
        #Se intancia la clase nodo
        nodo = Nodo()
        
        #Se inicializan las coordenadas del nodo
        nodo.x = x
        nodo.y = y

        #Se agrega el nodo a la lista nodos
        self.nodos.append(nodo)

        #Se establece el costo del nodo si el Pacman llega a pasar por ahi
        if self.laberinto.trampas[nodo.x][nodo.y] == 1:
            #Costo de pasar por un enemigo
            nodo.costo = 4
        else:
            if self.laberinto.beneficio[nodo.x][nodo.y] == 1:
                #Le permite al pacman coger el beneficio (espinaca) para tener un menor costo
                nodo.costo = -1
            else:
                nodo.costo = 1

        #Verifica si el nodo tiene algun obstaculo al rededor

        if self.laberinto.puede_pasar(nodo.x, nodo.y, "derecha"): #Pregunta en la clase Laberinto si puede pasar (ir derecha)
            #Si el nodo existe, este no se vuelve a crear
            nodo.derecha = self.nodo_existente(nodo.x, nodo.y + 1)
            #Si el nodo derecha es vacio, lo crea si lo tiene
            if nodo.derecha is None:
                #Se llama de nuevo al metodo CREAR_NODO() con el nodo derecha
                nodo.derecha = self.crear_nodo(nodo.x, nodo.y + 1)
                self.lista_nodos_hijos.append([nodo.derecha.x,nodo.derecha.y])
                #El nodo puede convertirse en padre, de modo que se agrega a la lista PADRES ***
                nodo.derecha.padres = nodo
                self.lista_nodos_padres.append([nodo.derecha.padres.x,nodo.derecha.padres.y])
  
        if self.laberinto.puede_pasar(nodo.x, nodo.y, "izquierda"):

            nodo.izquierda = self.nodo_existente(nodo.x, nodo.y - 1)

            if nodo.izquierda is None:

                nodo.izquierda = self.crear_nodo(nodo.x, nodo.y - 1)
                self.lista_nodos_hijos.append([nodo.izquierda.x,nodo.izquierda.y])

                nodo.izquierda.padres = nodo
                self.lista_nodos_padres.append([nodo.izquierda.padres.x,nodo.izquierda.padres.y])
                
        if self.laberinto.puede_pasar(nodo.x, nodo.y, "abajo"):
            nodo.abajo = self.nodo_existente(nodo.x + 1, nodo.y)

            if nodo.abajo is None:

                nodo.abajo = self.crear_nodo(nodo.x + 1, nodo.y)
                self.lista_nodos_hijos.append([nodo.abajo.x,nodo.abajo.y])

                nodo.abajo.padres = nodo
                self.lista_nodos_padres.append([nodo.abajo.padres.x,nodo.abajo.padres.y])
                

        if self.laberinto.puede_pasar(nodo.x, nodo.y, "arriba"):
            nodo.arriba = self.nodo_existente(nodo.x - 1, nodo.y)

            if nodo.arriba is None:
                
                nodo.arriba = self.crear_nodo(nodo.x - 1, nodo.y)
                self.lista_nodos_hijos.append([nodo.arriba.x,nodo.arriba.y])

                nodo.arriba.padres = nodo
                self.lista_nodos_padres.append([nodo.arriba.padres.x,nodo.arriba.padres.y])

        if (len(self.lista_nodos_hijos) == len(self.nodos)-1):#****
            lista_solucion(self.lista_nodos_padres,self.lista_nodos_hijos)

        return nodo
        
    #Verifica si el nodo ya ha sido creado (No volverlo a explorar)
    def nodo_existente(self, x, y):
        for nodo in self.nodos:
            if nodo.igualdad(x, y):
                return nodo
        return None
    #Obtine el costo del nodo donde esta situado
    def get_nodo_costo(self, x, y):
        for nodo in self.nodos:
            if nodo.igualdad(x, y):
                return nodo.costo
        return 0

    #Se vacia la lista padres cuando se llama el algoritmo que se va a ejecutar
    def limpiar_padres(self):
        for nodo in self.nodos:
            nodo.padres = None

    #Se crea la heuristica para los algoritmos de busqueda Avara y A*
    
