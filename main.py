import search
from graph import Graph
import mapa
from maze import Maze

if __name__ == "__main__":
    
    #Se inicializa la clase Graph
    graph = Graph()
    search.graph = graph

    #Busquedas

    search.busqueda_por_profundidad()
    #search.busqueda_avara()
    #search.busqueda_a_estrella()


