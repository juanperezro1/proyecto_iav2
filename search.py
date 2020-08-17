from collections import OrderedDict
from mapa import Pacman
from mapa import leer_archivo
import maze
import main

# ############################################## GLOBAL VARIABLES
graph = None
frontier = []
visitado = OrderedDict()  # To prevent duplicates, we use OrderedDict


def busqueda_por_profundidad():
    graph.limpiar_padres()
    dfs_bfs_ids_ucs("Depth First Search(DFS):")


def busqueda_por_amplitud():
    graph.limpiar_padres()
    dfs_bfs_ids_ucs("Breath First Search(BFS):")


def busqueda_iterativa_por_profundidad():
    graph.limpiar_padres()
    dfs_bfs_ids_ucs("Iterative Deepening Search(IDS):")


def costo_uniforme():
    graph.limpiar_padres()
    dfs_bfs_ids_ucs("Uniform costo Search(UCS):")


def busqueda_avara():
    graph.limpiar_padres()
    heuristica("Greedy Best First Search(GBFS):", return_heuristic)


def busqueda_a_estrella():
    graph.limpiar_padres()
    heuristica("A Star Search(A*):", return_cost_and_heuristic)


def heuristica(algoritmo, sort_by):

    # Variables
    estado_meta = None
    costo_solucion = 0
    solucion = []

    # Lets clear frontier and visitado, then add raiz element to the frontier.
    frontier.clear()
    visitado.clear()
    frontier.append(graph.raiz)

    while len(frontier) > 0:

        # Firstly, we need to sort the frontier according to heuristica...
        sort_frontier(sort_by)

        # We need to remove the correct nodo from the frontier and add it to the visitado.
        nodo_actual = frontier.pop(0)
        visitado[nodo_actual] = None

        # Stop GBFS, if we are in a goal state...
        if es_meta(nodo_actual):
            estado_meta = nodo_actual
            break

        # print(nodo_actual, nodo_actual.padres)

        # Add to frontier as in BFS.
        add_to_frontier(nodo_actual, "BFS")

    # Check if GBFS was successful...
    if estado_meta is not None:

        # We need to calculate the costo of the solucion AND get the solucion itself...
        actual = estado_meta
        while actual is not None:
            costo_solucion += actual.costo
            solucion.insert(0, actual)
            # Get the padres nodo and continue...
            actual = actual.padres

        # Print the results...
        imprimir_resultados(algoritmo, costo_solucion, solucion, visitado)
    else:
        print("No goal state found.")


def dfs_bfs_ids_ucs(algoritmo):

    # Variables
    pop_index = 0
    estado_meta = None
    costo_solucion = 0
    solucion = []
    expanded_nodes = []
    iteration = -1

    # DFS_BFS_IDS
    while estado_meta is None and iteration <= graph.profundidad_maxima:

        # For each iteration, we will increase iteration by one and clear frontier and visitado. Also append raiz nodo.
        iteration += 1
        frontier.clear()
        visitado.clear()
        frontier.append(graph.raiz)

        # If IDS, we will add iteration number...
        if "IDS" in algoritmo:
            expanded_nodes.append("Iteration " + str(iteration) + ":")

        while len(frontier) > 0:

            # If DFS or IDS, we will remove last nodo from the frontier.
            # IF BFS, we will remove the first nodo from the frontier.
            if "DFS" in algoritmo or "IDS" in algoritmo:
                pop_index = len(frontier) - 1

            # IF UCS, we need to sort the frontier according to costo...
            if "UCS" in algoritmo:
                sort_frontier(return_cost)

            # We need to remove the correct nodo from the frontier according to the algoritmo and add it to the visitado.
            nodo_actual = frontier.pop(pop_index)
            visitado[nodo_actual] = None

            # Stop DFS_BFS_IDS, if we are in a goal state...
            if es_meta(nodo_actual):
                estado_meta = nodo_actual
                break

            # Lets add all child nodos of the actual element to the end of the list...
            # If IDS, we need to add child nodos according to the iteration number.
            if "IDS" in algoritmo:
                padres = nodo_actual
                for i in range(iteration):
                    # If padres is not none, iterate to upper padres.
                    padres = padres if padres is None else padres.padres

                if padres is None:
                    add_to_frontier(nodo_actual, "DFS")
            # Else, we add all child nodos.
            else:
                add_to_frontier(nodo_actual, algoritmo)

        # Add all visitado nodos to expanded nodos, before clearing it.
        for nodo in visitado:
            expanded_nodes.append(nodo)

        # We will continue only if this is an IDS search...
        if "IDS" not in algoritmo:
            break

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
    imprimir_resultados(algoritmo, costo_solucion, solucion, expanded_nodes)


def add_to_frontier(nodo_actual, algoritmo):
    # If the child nodos are not None AND if they are not in visitado, we will add them to the frontier.
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

    # Then add each nodo to the frontier.
    for nodo in nodes_to_add:
        frontier.append(nodo)


def set_parent(parent_node, child_node, algoritmo):
    # We need to set the padres nodo it is None and if DFS is used.
    if "DFS" in algoritmo or child_node.padres is None:
        child_node.padres = parent_node
    return child_node


def es_visitado(nodo):
    if nodo in visitado:
        return True
    return False


def es_meta(nodo):
    for goal in graph.laberinto.meta:
        if goal[0] == nodo.x and goal[1] == nodo.y:
            return True
    return False

lista_solucion = []
lista2 = []
def imprimir_resultados(algoritmo, costo_solucion, solucion, expanded_nodes):
    print(algoritmo)
    print("costo of the solucion:", costo_solucion)
    print("The solucion path (" + str(len(solucion)) + " nodos):", end=" ")
    
    ##Imprime el camino para llegar a la meta
    
    for nodo in solucion:
        print(nodo, end=" ")
        lista_solucion.append([nodo.x,nodo.y])
        lista2.append([nodo.x,nodo.y])

    #actualizar_mapa(matriz_actualizar)
    #print("aquuuuu toy",lista_solucion)

    print("\nExpanded nodos (" + str(len(expanded_nodes)) + " nodos):", end=" ")
    if "IDS" in algoritmo:
        print()
        for i in range(len(expanded_nodes) - 1):
            if type(expanded_nodes[i+1]) == str:
                print(expanded_nodes[i])
            else:
                print(expanded_nodes[i], end=" ")
    else:
        for nodo in expanded_nodes:
            print(nodo, end=" ")
    print("\n")
    
    reve = maze.Maze()
    reve.funcion(lista2)

    #main.recibir_lista_solucion(lista2)


    Pacman(leer_archivo(),lista_solucion)

    
    
    
    

    


    
    

    

def return_cost(nodo):
    return nodo.costo


def return_heuristic(nodo):
    return nodo.heuristica


def return_cost_and_heuristic(nodo):
    return nodo.heuristica + nodo.costo


def sort_frontier(sort_by):
    frontier.sort(key=sort_by)
