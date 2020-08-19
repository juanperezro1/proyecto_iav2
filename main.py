import search
import search2
from graph import Graph
import mapa
from graph2 import Graph2
from maze import Maze
import threading

if __name__ == "__main__":
    # Setting graph we initiated to search class...
    graph = Graph()
    
    search.graph = graph

    #graph2 = Graph2()
    #search2.graph2 = graph2

    #search.busqueda_por_profundidad()
    #search.busqueda_a_estrella()
    search.busqueda_avara()
    
    

