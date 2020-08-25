
lista_solucion_pacman = [[1, 2],[1, 3],[1, 4],[1, 5],[1, 6],[1, 7],[1, 8],[2, 8],[3, 8],[4, 8],[5, 8],[6, 8],[7, 8],[8, 8],[9, 8],[10, 8],
                        [10, 9],[1, 10],[11, 10]]


lista_profundidad = [[7, 5], [7, 6], [7, 7], [7, 8], [8, 8], [9, 8], [10, 8], [10, 9], [10, 10], [10, 11], [11, 11], [11, 10], [11, 9], [11, 8], 
[11, 7], [11, 6],[7, 5], [7, 6], [7, 7], [7, 8], [8, 8], [9, 8]]

ultimo_lista_pacman = lista_solucion_pacman[-1:]
ultimo_lista_fantasma = lista_profundidad[-1:]

for i in ultimo_lista_pacman:
    ultimo_lista_pacman = i

for i in ultimo_lista_fantasma:
    ultimo_lista_fantasma = i

if (len(lista_solucion_pacman) <= len(lista_profundidad)):
    for i in range(len(lista_profundidad)):
        lista_solucion_pacman.append(ultimo_lista_pacman)
else:
    for i in range(len(lista_solucion_pacman)):
        lista_profundidad.append(ultimo_lista_fantasma)


print(lista_profundidad)
print()
print(lista_solucion_pacman)