import sys
from maze import Maze

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

    def set_costo(self,costo_nuevo):
        self.costo = costo_nuevo

class Graph2:

    nodos = []  # Keeping all nodos in a list to prevent duplicate nodos.
    laberinto = None

    def __init__(self):
        # Creating the graph.
        self.laberinto = Maze()
        self.raiz = self.crear_nodo(self.laberinto.inicio_enemigo[0], self.laberinto.inicio_enemigo[1])

        # Finding maximum depth.
        self.profundidad_maxima = self.encuentra_maxima_profundidad() - 1

        # Creating heuristica...
        self.crear_heuristica()

        # We will make the costo of raiz nodo 0, because that's where we inicio.
        self.raiz.costo = 0

    def crear_nodo(self, x, y):
        nodo = Nodo()

        # Initializing nodo's coordinates.
        nodo.x = x
        nodo.y = y

        # Adding the nodo into the nodos list.
        self.nodos.append(nodo)

        """
        # Setting the costo 1 if it is not a trap square.
        if self.laberinto.trampas[nodo.x][nodo.y] == 1:
            nodo.costo = 7
        else:
            nodo.costo = 1
        """
        
        if self.laberinto.beneficio[nodo.x][nodo.y] == 1:
            nodo.costo = 0.5
        else:

            nodo.costo = 1
        

        # Setting all child nodos.
        if self.laberinto.puede_pasar(nodo.x, nodo.y, "derecha"):
            # Before creating a new nodo, we should check if that nodo exists. If yes, we don't need to create it.
            nodo.derecha = self.nodo_existente(nodo.x, nodo.y + 1)
            if nodo.derecha is None:
                nodo.derecha = self.crear_nodo(nodo.x, nodo.y + 1)
                nodo.derecha.padres = nodo
                
        if self.laberinto.puede_pasar(nodo.x, nodo.y, "izquierda"):
            nodo.izquierda = self.nodo_existente(nodo.x, nodo.y - 1)
            if nodo.izquierda is None:
                nodo.izquierda = self.crear_nodo(nodo.x, nodo.y - 1)
                nodo.izquierda.padres = nodo

        if self.laberinto.puede_pasar(nodo.x, nodo.y, "abajo"):
            nodo.abajo = self.nodo_existente(nodo.x + 1, nodo.y)
            if nodo.abajo is None:
                nodo.abajo = self.crear_nodo(nodo.x + 1, nodo.y)
                nodo.abajo.padres = nodo

        if self.laberinto.puede_pasar(nodo.x, nodo.y, "arriba"):
            nodo.arriba = self.nodo_existente(nodo.x - 1, nodo.y)
            if nodo.arriba is None:
                nodo.arriba = self.crear_nodo(nodo.x - 1, nodo.y)
                nodo.arriba.padres = nodo

        return nodo

    def nodo_existente(self, x, y):
        for nodo in self.nodos:
            if nodo.igualdad(x, y):
                return nodo
        return None

    def encuentra_maxima_profundidad(self):
        profundidad_maxima = 0

        for nodo in self.nodos:
            nodo_actual = nodo
            profundidad_local = 0
            while nodo_actual is not None:
                nodo_actual = nodo_actual.padres
                profundidad_local += 1

            # If profundidad_local is greater, we will set it as profundidad_maxima.
            profundidad_maxima = max(profundidad_maxima, profundidad_local)

        return profundidad_maxima

    def get_nodo_costo(self, x, y):
        for nodo in self.nodos:
            if nodo.igualdad(x, y):
                return nodo.costo
        return 0

    def limpiar_padres(self):
        for nodo in self.nodos:
            nodo.padres = None

    def crear_heuristica(self):
        # Create a heuristica for each nodo...
        for nodo in self.nodos:
            # Select minimum distance to a closest goal...
            costo_total = sys.maxsize
            for goal in self.laberinto.meta_enemigo:
                costo = 0
                distancia_vertical = goal[1] - nodo.y
                distancia_horizontal = goal[0] - nodo.x

                # Then we will add each nodo's costo until to the goal state...
                x = 0
                y = 0
                
                while distancia_vertical > 0:
                    y += 1
                    costo += self.get_nodo_costo(nodo.x, nodo.y + y)
                    distancia_vertical -= 1
                while distancia_horizontal > 0:
                    x += 1
                    costo += self.get_nodo_costo(nodo.x + x, nodo.y + y)
                    distancia_horizontal -= 1
                while distancia_vertical < 0:
                    y -= 1
                    costo += self.get_nodo_costo(nodo.x + x, nodo.y + y)
                    distancia_vertical += 1
                while distancia_horizontal < 0:
                    x -= 1
                    costo += self.get_nodo_costo(nodo.x + x, nodo.y + y)
                    distancia_horizontal += 1

                # Select the minimum heuristica...
                costo_total = min(costo_total, costo)

            # After calculating the total costo, we assign it into nodo's heuristica...
            nodo.heuristica = costo_total
