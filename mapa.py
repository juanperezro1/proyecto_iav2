import pygame
import maze
import numpy as np
import os
from graph import Nodo
import sys
from pygame.locals import *
import time

colorF = (0, 0, 0)  
pixel = 70

#Se crea la clase MUROy el constructor
class Muro(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenMuro = pygame.image.load("muro.jpg")
        self.rect = self.imagenMuro.get_rect()
        self.rect.top = posX
        self.rect.left = posY
        pygame.mixer.music.load("camino.mpeg")
        pygame.mixer.music.play(-1) 

    def dibujarMuro(self, superficie):
        superficie.blit(self.imagenMuro, self.rect)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenEnemigo = pygame.image.load("pacman.png")
        self.rect = self.imagenEnemigo.get_rect()
        self.rect.top = posX
        self.rect.left = posY 
      
    def dibujarJugador(self, superficie):
        superficie.blit(self.imagenEnemigo, self.rect)
        
class Sra_pacman(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenLlave = pygame.image.load("srapacman.png")
        self.rect = self.imagenLlave.get_rect()
        self.rect.top = posX
        self.rect.left = posY

    def dibujar_sra_pacman(self, superficie):
        superficie.blit(self.imagenLlave, self.rect)

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenEnemigo = pygame.image.load("enemigo.png")
        self.rect = self.imagenEnemigo.get_rect()
        self.rect.top = posX
        self.rect.left = posY

    def dibujar_enemigo(self, superficie):
        superficie.blit(self.imagenEnemigo, self.rect)   

class Espinaca(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        self.imagenEspinaca = pygame.image.load("espinaca.png")
        self.rect = self.imagenEspinaca.get_rect()
        self.rect.top = posX
        self.rect.left = posY

    def dibujar_espinaca(self, superficie):
        superficie.blit(self.imagenEspinaca, self.rect)   

#Permite leer el archivo .txt (matriz camino,enemigos,inicio,meta)
def leer_archivo():
    archivo = open("matrizMapa.txt")
    matriz = np.loadtxt(archivo, dtype=int, skiprows=0)
    archivo.close()
    matriz = np.asarray(matriz)
    return matriz

def Pacman(matrizAyuda1,Solucion):
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.mixer.init()
    
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
            
            if (matrizAyuda1[i][j] == 4):
                sra_pacman = Sra_pacman(i*pixel,j*pixel)
                sra_pacman.dibujar_sra_pacman(ventana)
                pos_sra_pacman.append(i)
                pos_sra_pacman.append(j)
                print(pos_sra_pacman)
                
            if (matrizAyuda1[i][j] == 5):
                espinaca = Espinaca(i*pixel,j*pixel)
                espinaca.dibujar_espinaca(ventana)
                pos_espinaca.append(i)
                pos_espinaca.append(j)
     
    pygame.display.set_caption("Pacman Univalle")       
    pygame.display.update()

    for i in Solucion:
        for y in pos_enemigo:
            if i == y:
                print("Has sido asesinado por un fantasma en la posición:",y)
                pygame.quit()
                sys.exit() 
            else: 
                pass
        if i == pos_sra_pacman:
            pygame.mixer.music.stop()
        else:
            pass
                        
        jugadorAct = Jugador(pixel*i[0],pixel*i[1])
        time.sleep(0.5) ###############################################
        rectangulo = pygame.Rect(pixel*i[1],pixel*i[0],pixel,pixel)
        actualizarJugador(jugadorAct,ventana)
        pygame.draw.rect(ventana,colorF,rectangulo)

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
        
def actualizarJugador(jugador,superficie):
        jugador.dibujarJugador(superficie)
        pygame.display.update()


  