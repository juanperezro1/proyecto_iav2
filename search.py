from collections import OrderedDict
from mapa import Pacman
from mapa import leer_archivo
from maze import Maze
import main

graph = None
frontera = []
visitado = OrderedDict()  #Se previene que el nodo se repita, usando diccionarios

def busqueda_por_profundidad():
    graph.limpiar_padres()
    busqueda_profundidad("Busqueda por profundidad(DFS):")

def busqueda_avara():
    graph.limpiar_padres()
    heuristica("Busqueda avara(GBFS):", return_heuristic)

def busqueda_a_estrella():
    graph.limpiar_padres()
    heuristica("Busqueda A estrella(A*):", return_cost_and_heuristic)
    
def heuristica(algoritmo, ordenar_heuristica):

    # Variables
    estado_meta = None
    costo_solucion = 0
    solucion = []

    #Se limpian la frontera y los nodos visitado
    frontera.clear()
    visitado.clear()

    #Se agrega a la lista de FRONTERA el nodo raiz
    frontera.append(graph.raiz)

    while len(frontera) > 0:

        #Se organiza la frontera de acuerdo a la heuristica
        ordenar_frontera(ordenar_heuristica)
        
        #Remueve el nodo correcto de la frontera y se agrega a visitado
        nodo_actual = frontera.pop(0)
        visitado[nodo_actual] = None

        #Sale del metodo si encuentra la meta
        if es_meta(nodo_actual):
            estado_meta = nodo_actual
            break

        #Criterio de desempate DFS
        print("criterio desempa",nodo_actual)
        agregar_a_frontera(nodo_actual, "DFS")
        

    #Verifica si la busqueda AVARA fue exitosa
    if estado_meta is not None:

        #Se calcula el costo de la solución y la ruta 
        actual = estado_meta
        while actual is not None:
            costo_solucion += actual.costo
            solucion.insert(0, actual)
            #Obtener los nodos padres del nodo actual
            actual = actual.padres

        #Imprimir resultados
        imprimir_resultados(algoritmo, costo_solucion, solucion, visitado)
    else:
        print("No se encontro una meta")

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
        frontera.append(graph.raiz)

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
        # Get the padres nodo and continue...
        actual = actual.padres
    
    #Imprimir los resultados
    imprimir_resultados(algoritmo, costo_solucion, solucion, nodos_expandidos)

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
        print("nodo padre:",nodo_padre,"nodo_hijo:",nodo_hijo,algoritmo)
    print("nodooooooo jijo",nodo_hijo)
    return nodo_hijo


def es_visitado(nodo):
    if nodo in visitado:
        return True
    return False

#Evalua si el nodo en donde se encuentra es meta
def es_meta(nodo):
    for goal in graph.laberinto.meta:
        if goal[0] == nodo.x and goal[1] == nodo.y:
            return True
    return False

lista_solucion = []
lista_expandidos = []

def imprimir_resultados(algoritmo, costo_solucion, solucion, nodos_expandidos):

    print(algoritmo)
    print("El camino solución es (" + str(len(solucion)) + " nodos):", end=" ")
    
    ##Imprime el camino para llegar a la meta
    for nodo in solucion:
        print(nodo, end=" ")
        lista_solucion.append([nodo.x,nodo.y])

    print("\nNodos expandidos (" + str(len(nodos_expandidos)) + " nodos):", end=" ")

    for nodo in nodos_expandidos:
        print(nodo, end=" ")
        lista_expandidos.append([nodo.x,nodo.y])
    print("\n")

    maze = Maze()
    #Se envia la LISTA_SOLUCION para determinar el poder espinaca
    maze.poder_espinaca(lista_solucion,costo_solucion)
    Pacman(leer_archivo(),lista_solucion)
    
def return_cost(nodo):
    return nodo.costo

def return_heuristic(nodo):
    print("holiii",nodo.heuristica)
    return nodo.heuristica

def return_cost_and_heuristic(nodo):
    print("aquiii",nodo.heuristica,nodo.costo)
    return nodo.heuristica + nodo.costo
    
def ordenar_frontera(ordenar_heuristica):
    frontera.sort(key=ordenar_heuristica)