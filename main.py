import busquedas
import busquedaEnemigo
from grafo import Grafo
from grafoEnemigo import GrafoEnemigo

if __name__ == "__main__":
    
    #Se inicializa la clase Graph
    grafo = Grafo()
    busquedas.grafo = grafo

    grafo_enemigo = GrafoEnemigo()
    busquedaEnemigo.grafo_enemigo = grafo_enemigo

    lista_fantasma = busquedaEnemigo.busqueda_por_profundidad()
    #print("fantasma",lista_fantasma)
        
    busquedas.index_validacion = 1 #0 para que grite y 1 para que no grite

    #Busquedas

    #busquedas.busqueda_por_profundidad()
    #busquedas.busqueda_avara()
    busquedas.busqueda_a_estrella(lista_fantasma)
    


    
    


