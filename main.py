import busquedas
from grafo import Grafo

if __name__ == "__main__":
    
    #Se inicializa la clase Graph
    grafo = Grafo()
    busquedas.grafo = grafo

    #Busquedas

    #busquedas.busqueda_por_profundidad()
    #busquedas.busqueda_avara()
    busquedas.busqueda_a_estrella()


