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

    #Se agraga a la lista de FRONTERA el nodo raiz
    frontera.append(graph.raiz)

    while len(frontera) > 0:

        #Se organiza la frontera de acuerdo a la heuristica
        ordenar_frontera(ordenar_heuristica)

        # We need to remove the correct nodo from the frontera and add it to the visitado. ****
        nodo_actual = frontera.pop(0)
        visitado[nodo_actual] = None

        #Sale del metodo si encuentra la meta
        if es_meta(nodo_actual):
            estado_meta = nodo_actual
            break

        # Add to frontera as in BFS. ***
        add_to_frontier(nodo_actual, "BFS")

    #Verifica si la busqueda AVARA fue exitosa
    if estado_meta is not None:

        #Se calcula el costo de la solución y la ruta 
        actual = estado_meta
        while actual is not None:
            costo_solucion += actual.costo
            solucion.insert(0, actual)
            # Get the padres nodo and continue...***
            actual = actual.padres

        #Imprimir resultados
        imprimir_resultados(algoritmo, costo_solucion, solucion, visitado)
    else:
        print("No se encontro una meta")

def busqueda_profundidad(algoritmo):

    # Variables
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

        #***
        while len(frontera) > 0: 

            if "DFS" in algoritmo:
                pop_index = len(frontera) - 1

            # We need to remove the correct nodo from the frontera according to the algoritmo and add it to the visitado. **
            nodo_actual = frontera.pop(pop_index)
            visitado[nodo_actual] = None

            #Detener el metodo si se ha llegado a la meta
            if es_meta(nodo_actual):
                estado_meta = nodo_actual
                break

            #***
            add_to_frontier(nodo_actual, algoritmo)

        #Se guardan todos los nodos visitado en la lista NODOS_EXPANDIDOS
        for nodo in visitado:
            nodos_expandidos.append(nodo)

        # We will continue only if this is an IDS search...
        # if "IDS" not in algoritmo:
        #     break

    # Check if DFS_BFS_IDS was successful...
    if estado_meta is None:
        print("No goal state found.")
        return

    # We need to calculate the costo of the solucion AND get the solucion itself...
    actual = estado_meta

    while actual is not None:
        costo_solucion += actual.costo
        solucion.insert(0, actual)
        # Get the padres nodo and continue...
        actual = actual.padres
    
    # Print the results...
    imprimir_resultados(algoritmo, costo_solucion, solucion, nodos_expandidos)


def add_to_frontier(nodo_actual, algoritmo):
    # If the child nodos are not None AND if they are not in visitado, we will add them to the frontera.
    nodes_to_add = []
    
    if nodo_actual.derecha is not None and not es_visitado(nodo_actual.derecha):
        nodes_to_add.append(set_parent(nodo_actual, nodo_actual.derecha, algoritmo))
    if nodo_actual.abajo is not None and not es_visitado(nodo_actual.abajo):
        nodes_to_add.append(set_parent(nodo_actual, nodo_actual.abajo, algoritmo))
    if nodo_actual.izquierda is not None and not es_visitado(nodo_actual.izquierda):
        nodes_to_add.append(set_parent(nodo_actual, nodo_actual.izquierda, algoritmo))
    if nodo_actual.arriba is not None and not es_visitado(nodo_actual.arriba):
        nodes_to_add.append(set_parent(nodo_actual, nodo_actual.arriba, algoritmo))

    # For DFS we'll do it in reverse order because we add each nodo to the end and derecha should be the last nodo.
    # For BFS we'll do it in correct order.
    if "DFS" in algoritmo:
        nodes_to_add.reverse()

    # Then add each nodo to the frontera.
    for nodo in nodes_to_add:
        frontera.append(nodo)


def set_parent(parent_node, child_node, algoritmo):
    # We need to set the padres nodo it is None and if DFS is used. ****
    if "DFS" in algoritmo or child_node.padres is None:
        child_node.padres = parent_node
    return child_node

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