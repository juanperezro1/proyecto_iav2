from collections import OrderedDict
#from mapa import Pacman
from mapa import Mapa
#from mapa import Fantasma
from mapa import leer_archivo
from laberinto import Laberinto
from mapa import modificar_file

import main
import numpy as np
import random

grafo_enemigo = None
frontera = []
visitado = OrderedDict()  #Se previene que el nodo se repita, usando diccionarios

def busqueda_por_profundidad():
    grafo_enemigo.limpiar_padres()
    solucion = busqueda_profundidad("Busqueda por profundidad(DFS):")
    return solucion

def busqueda_profundidad(algoritmo):

    #Variables
    pop_index = 0
    estado_meta = None
    costo_solucion = 0
    solucion = []
    nodos_expandidos = []

    #Se establece la condición si el Pacman no ha llegado a la meta
    while estado_meta is None: 

        frontera.clear()
        visitado.clear()
        frontera.append(grafo_enemigo.raiz)

        while len(frontera) > 0: 

            if "DFS" in algoritmo:
                pop_index = len(frontera) - 1

            #Se remueve el nodo correcto de la frontera y se agrega a visitado
            nodo_actual = frontera.pop(pop_index)
            visitado[nodo_actual] = None

            #Detener el metodo si se ha llegado a la meta
            if es_meta(nodo_actual):
                estado_meta = nodo_actual
                break

            #Agregar los nodos fronteras segun donde se encuentre el jugador
            agregar_a_frontera(nodo_actual, algoritmo)

        #Se guardan todos los nodos visitado en la lista NODOS_EXPANDIDOS
        for nodo in visitado:
            nodos_expandidos.append(nodo)

    #Verifica si el algoritmo DFS fue exitoso
    if estado_meta is None:
        print("No se encontro la meta.")
        return

    # We need to calculate the costo of the solucion AND get the solucion itself...
    actual = estado_meta

    while actual is not None:
        costo_solucion += actual.costo
        solucion.insert(0, actual)
        #Obtener el nodo padre
        actual = actual.padres
    
    #Imprimir los resultados
    lista_solucion = imprimir_resultados(algoritmo, costo_solucion, solucion, nodos_expandidos)
    return lista_solucion

def agregar_a_frontera(nodo_actual, algoritmo):
    #Si el nodo hijo no es None y no ha sido visitado, se agrega a la frontera.
    agregar_nodos = []
    
    if nodo_actual.derecha is not None and not es_visitado(nodo_actual.derecha):
        agregar_nodos.append(set_padres(nodo_actual, nodo_actual.derecha, algoritmo))
    if nodo_actual.abajo is not None and not es_visitado(nodo_actual.abajo):
        agregar_nodos.append(set_padres(nodo_actual, nodo_actual.abajo, algoritmo))
    if nodo_actual.izquierda is not None and not es_visitado(nodo_actual.izquierda):
        agregar_nodos.append(set_padres(nodo_actual, nodo_actual.izquierda, algoritmo))
    if nodo_actual.arriba is not None and not es_visitado(nodo_actual.arriba):
        agregar_nodos.append(set_padres(nodo_actual, nodo_actual.arriba, algoritmo))

    #Se realizar reverse para acomodar los nodos 
    if "DFS" in algoritmo:
        agregar_nodos.reverse()

    #Se agregan los nodos a la frontera
    for nodo in agregar_nodos:
        frontera.append(nodo)

def set_padres(nodo_padre, nodo_hijo, algoritmo):
    #Se le asigna el nodo donde esta actualmente los posibles hijos que puede tener 
    if "DFS" in algoritmo or nodo_hijo.padres is None:
        nodo_hijo.padres = nodo_padre
    return nodo_hijo

def es_visitado(nodo):
    if nodo in visitado:
        return True
    return False

#Evalua si el nodo en donde se encuentra es meta
def es_meta(nodo):
    for goal in grafo_enemigo.laberinto.meta_enemigo:
        if goal[0] == nodo.x and goal[1] == nodo.y:
            return True
    return False

lista_solucion = []
lista_expandidos = []
pos_gritona = []

index_validacion = 0
def imprimir_resultados(algoritmo, costo_solucion, solucion, nodos_expandidos):

    for nodo in solucion:
        lista_solucion.append([nodo.x,nodo.y])

    return lista_solucion
    


 

    
