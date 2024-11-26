import pygame
import random
from dona import *

# Configuración inicial del juego
FPS = 60
width = 200  # ancho del personaje Homero
height = 250  # alto del personaje Homero
tamaño_pantalla = (width, height)
x = 493  # posición inicial de la boca de Homero en X
y = 658  # posición inicial de la boca de Homero en Y
z = 40   # tamaño del rectángulo de la boca
score = 0  # puntaje inicial
running = True  # variable para mantener el bucle del juego

# Inicialización de Pygame y configuración de la ventana
pygame.init()
RELOJ = pygame.time.Clock()
screen = pygame.display.set_mode([800, 800])  # tamaño de la ventana de juego
pygame.display.set_caption("Las Donas de Homero")
icono = pygame.image.load("HOMERO\Recursos\ico.png")
pygame.display.set_icon(icono)

# Configuración del temporizador para generar eventos cada 100 ms
tick = pygame.USEREVENT + 0
pygame.time.set_timer(tick, 100)

# Configuración de la imagen de Homero y su rectángulo para colisiones
imagen_homero = pygame.image.load("HOMERO\Recursos\derecha.png")
imagen_homero = pygame.transform.scale(imagen_homero, (width, height))
rect_homero = pygame.Rect(400, 570, 200, 200)  # posición inicial de Homero
rect = pygame.Rect(x, y, z, z)  # rectángulo de la boca para colisiones

# Diccionario que representa al personaje Homero
personaje = {
    "surface": imagen_homero,
    "rectangulo": rect_homero,
    "rectangulo_boca": rect,
    "puntaje": score
}

# Crear una lista inicial de donas
lista_donas = crear_lista_donas(50)

# Música de fondo
pygame.mixer.init()
sonido_fondo = pygame.mixer.Sound("HOMERO\Recursos\musica.mp3")
sonido_fondo.set_volume(0.2)
sonido_fondo.play()

# Configuración del fondo de la pantalla
fondo = pygame.image.load("HOMERO\Recursos\\fondo.png")
fondo_final = pygame.transform.scale(fondo, tamaño_pantalla)
screen.blit(fondo, (0, 0))

# Bucle principal del juego
while running:
    RELOJ.tick(FPS)  # establece el FPS del juego
    for event in pygame.event.get():  # escucha eventos de teclado y temporizador
        if event.type == pygame.QUIT:  # cerrar ventana
            running = False
        if event.type == pygame.USEREVENT:
            if event.type == tick:  # evento temporizado
                update(lista_donas)  # actualiza la posición de las donas
    
        lista_teclas = pygame.key.get_pressed()
    
        # Movimiento hacia la izquierda
        if lista_teclas[pygame.K_LEFT]:
            imagen_homero = pygame.image.load("HOMERO\Recursos\izquierda.png")
            imagen_homero = pygame.transform.scale(imagen_homero, (width, height)) 
            screen.blit(imagen_homero, rect_homero)
            nueva_x = rect_homero.x + -10  # nueva posición a la izquierda
            if nueva_x > 0 and nueva_x < 600:  # límite del margen izquierdo
                rect_homero.x += -10
                rect.x += -10  # mueve también el rectángulo de la boca
            
        # Movimiento hacia la derecha
        if lista_teclas[pygame.K_RIGHT]:
            nueva_x = rect_homero.x + 10
            imagen_homero = pygame.image.load("HOMERO\Recursos\derecha.png")
            imagen_homero = pygame.transform.scale(imagen_homero, (width, height))
            screen.blit(imagen_homero, rect_homero)
            if nueva_x > 0 and nueva_x < 600:  # límite del margen derecho
                rect_homero.x += 10
                rect.x += 10

    # Dibujar el fondo y el personaje en la pantalla
    screen.blit(fondo, (0, 0))
    screen.blit(imagen_homero, rect_homero)
        
    # Actualizar la pantalla con donas y puntaje
    actualizar_pantalla(lista_donas, personaje, screen)
    
    pygame.display.flip()  # actualizar la pantalla
    
pygame.quit()  # cerrar pygame
