import pygame
import laberinto
import numpy as np
import os
from grafo import Nodo
import sys
from pygame.locals import *
import time
import random
from multiprocessing import Process
import threading

colorF = (0, 0, 0)  
pixel = 70

class Mapa:

    lista_profundidad = []
    lista_solucion_pacman = []

    def lista_solucion_profundidad(self,solucion):
        self.lista_profundidad = solucion
        
    def Pacman(self,matrizAyuda1,Solucion):
        
        self.lista_solucion_pacman = Solucion
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        print("Busqueda por profundidad",self.lista_profundidad)
        pygame.init()
        pygame.mixer.init()

        print(self.lista_profundidad)
        global ventana
        ventana = pygame.display.set_mode((pixel * len(matrizAyuda1), pixel * len(matrizAyuda1)))
        ventana.fill(colorF)

        pos_enemigo = []
        pos_sra_pacman = []
        pos_espinaca = []
    
        for i in range(len(matrizAyuda1)):
            for j in range(len(matrizAyuda1)):
                if (matrizAyuda1[i][j] == 1):
                    muro = Muro(i * pixel, j * pixel)
                    muro.dibujarMuro(ventana)

                if (matrizAyuda1[i][j] == 2):
                    enemigo = Enemigo(i*pixel,j*pixel)
                    enemigo.dibujar_enemigo(ventana)
                    pos_enemigo.append([i,j])

                if (matrizAyuda1[i][j] == 3):
                    enemigo = Jugador(i*pixel,j*pixel)
                    enemigo.dibujarJugador(ventana)
                  
                if (matrizAyuda1[i][j] == 4):
                    sra_pacman = Sra_pacman(i*pixel,j*pixel)
                    sra_pacman.dibujar_sra_pacman(ventana)
                    pos_sra_pacman.append(i)
                    pos_sra_pacman.append(j)
                    #print(pos_sra_pacman)
                    
                if (matrizAyuda1[i][j] == 5):
                    espinaca = Espinaca(i*pixel,j*pixel)
                    espinaca.dibujar_espinaca(ventana)
                    pos_espinaca.append(i)
                    pos_espinaca.append(j)

        ultimo_lista_pacman = self.lista_solucion_pacman[-1:]
        ultimo_lista_fantasma = self.lista_profundidad[-1:]

        for i in ultimo_lista_pacman:
            self.ultimo_lista_pacman = i

        for i in ultimo_lista_fantasma:
            self.ultimo_lista_fantasma = i

        if (len(self.lista_solucion_pacman) <= len(self.lista_profundidad)):
            for i in range(len(self.lista_profundidad)):
                self.lista_solucion_pacman.append(ultimo_lista_pacman)
        else:
            for i in range(len(self.lista_solucion_pacman)):
                self.lista_profundidad.append(self.ultimo_lista_fantasma)

        mortal = zip(self.lista_solucion_pacman,self.lista_profundidad)
        contador = 0

        try:
            for i,j in mortal:
                
                fantasma = Enemigo(pixel*j[0],pixel*j[1])
                jugadorAct = Jugador(pixel*i[0],pixel*i[1])
                
                jugadorAct.dibujarJugador(ventana)
                fantasma.dibujar_enemigo(ventana)
                pygame.display.update()

                if i == j:
                    print("Has sido asesinado por un fantasma en la posición:",j)
                    pygame.quit()
                    sys.exit() 
                else: 
                    pass
                if i == pos_sra_pacman:
                    pygame.mixer.music.stop()
                else:
                    pass

                time.sleep(0.5)

                if contador < len(self.lista_solucion_pacman) - 1:
                    rectangulo = pygame.Rect(pixel*i[1],pixel*i[0],pixel,pixel)
                    pygame.draw.rect(ventana,colorF,rectangulo)

                    rectangulo2 = pygame.Rect(pixel*j[1],pixel*j[0],pixel,pixel)
                    pygame.draw.rect(ventana,colorF,rectangulo2)
        
            pygame.display.set_caption("Pacman Univalle")       
            pygame.display.update()
        
        except:
            print("")

        while True:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
    
def actualizarJugador(jugador,superficie):
    jugador.dibujarJugador(superficie)

def actualizarEnemigo(enemigo,superficie):
    enemigo.dibujar_enemigo(superficie)
    
class Muro(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenMuro = pygame.image.load("recursos/muro.jpg")
        self.rect = self.imagenMuro.get_rect()
        self.rect.top = posX
        self.rect.left = posY
        pygame.mixer.music.load("recursos/camino.mpeg")
        pygame.mixer.music.play(-1) 

    def dibujarMuro(self, superficie):
        superficie.blit(self.imagenMuro, self.rect)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenEnemigo = pygame.image.load("recursos/pacman.png")
        self.rect = self.imagenEnemigo.get_rect()
        self.rect.top = posX
        self.rect.left = posY 
      
    def dibujarJugador(self, superficie):
        superficie.blit(self.imagenEnemigo, self.rect)
        
class Sra_pacman(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenLlave = pygame.image.load("recursos/srapacman.png")
        self.rect = self.imagenLlave.get_rect()
        self.rect.top = posX
        self.rect.left = posY

    def dibujar_sra_pacman(self, superficie):
        superficie.blit(self.imagenLlave, self.rect)

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenEnemigo = pygame.image.load("recursos/enemigo.png")
        self.rect = self.imagenEnemigo.get_rect()
        self.rect.top = posX
        self.rect.left = posY

    def dibujar_enemigo(self, superficie):
        superficie.blit(self.imagenEnemigo, self.rect)   

class Espinaca(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenEspinaca = pygame.image.load("recursos/espinaca.png")
        self.rect = self.imagenEspinaca.get_rect()
        self.rect.top = posX
        self.rect.left = posY

    def dibujar_espinaca(self, superficie):
        superficie.blit(self.imagenEspinaca, self.rect)   


#Permite leer el archivo .txt (matriz camino,enemigos,inicio,meta)
def leer_archivo():
    archivo = open("mm.txt")
    matriz = np.loadtxt(archivo, dtype=int, skiprows=0)
    archivo.close()
    matriz = np.asarray(matriz)
    #print(matriz)
    return matriz

def modificar_file(pos_inicio):
    matriz = leer_archivo()
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if (matriz[i][j] == 3):
                matriz[i][j] = 0
            
    matriz[pos_inicio[0],pos_inicio[1]] = 3
    save = np.savetxt('mm.txt',matriz, delimiter= ' ',fmt='%d')


  