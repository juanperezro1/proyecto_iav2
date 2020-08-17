import search
from graph import Graph
import mapa
from maze import Maze




if __name__ == "__main__":
    # Setting graph we initiated to search class...
    graph = Graph()
    search.graph = graph
    

    
    #search.busqueda_por_profundidad()
    #search.busqueda_por_amplitud()
    #search.busqueda_iterativa_por_profundidad()
    #search.costo_uniforme()
    #search.busqueda_avara()
    search.busqueda_a_estrella()
    
    

##Iligal
