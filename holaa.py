
"""
a=[1,2,3]
b=[4,5,6] 
c = [a, b] 
with open("list1.txt", "w") as file:
    for x in zip(*c):
        file.write("{0}\t{1}\n".format(*x))
"""

pos_inicio = [2,3]
import numpy as np
matriz = [[5, 0, 4, 0, 0, 0],
          [0, 1, 0, 2, 0, 0],
          [0, 0, 1, 1, 0, 0],
          [0, 3, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0]]



matriz2 = np.array(matriz)
matriz2[pos_inicio[0],pos_inicio[1]] = 3
print(matriz2)


