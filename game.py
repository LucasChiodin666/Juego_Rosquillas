import pygame
import random
import sys
import time
import os
from funciones import *
from constantes import *

# ------------------ CONFIGURACIÓN INICIAL DEL JUEGO ----------------------
FPS = 60
ANCHO = 200  # ancho del personaje Homero
ALTO = 250  # alto del personaje Homero
tamaño_pantalla = (ANCHO, ALTO)
screen = pygame.display.set_mode([800, 800])

# Posiciones iniciales de la boca de Homero
x = 470
y = 640
w = 70
z = 50  # tamaño del rectángulo de la boca
score = 0  # puntaje inicial

# -------------------- INICIALIZACIÓN DE PYGAME --------------------------
pygame.init()
RELOJ = pygame.time.Clock()

# -------------------- TITULO E ICONO DEL JUEGO----------------------------
pygame.display.set_caption("Las Donas de Homero")
icono = pygame.image.load("HOMERO\\Recursos\\ico.png")
pygame.display.set_icon(icono)

#------------------------- MUSICA DE FONDO ----------------------------------
sonido("HOMERO\\Recursos\\sonidos\\musica.mp3", 0.8)

# ------------------------ PANTALLA DE INICIO ----------------------------
pantallas_con_boton("HOMERO\\Recursos\\pantalla\\homero.png", "", 400, 250, 300, 50, AQUEMARINE)

#------------------------------temporizador de caida -------------------------
# Configuración del temporizador para generar eventos cada 100 ms
tick = pygame.USEREVENT + 0
pygame.time.set_timer(tick, 100)

# -------------------- CONFIGURACIÓN DE IMÁGENES Y RECTÁNGULOS -----------
# Cargar imágenes de las direcciones de Homero
imagen_homero_derecha = pygame.image.load("HOMERO\\Recursos\\personaje\\derecha.png")
imagen_homero_derecha = pygame.transform.scale(imagen_homero_derecha, (ANCHO, ALTO))

imagen_homero_izquierda = pygame.image.load("HOMERO\\Recursos\\personaje\\izquierda.png")
imagen_homero_izquierda = pygame.transform.scale(imagen_homero_izquierda, (ANCHO, ALTO))

# Inicializar Homero mirando a la derecha al inicio
imagen_homero = imagen_homero_derecha

# ------------------------ PANTALLA GAME OVER ----------------------------

# ------------------------------- INICIALIZO RECTÁNGULO DE HOMERO\BOCA --------------------
# Rectángulos para colisiones
rect_homero = pygame.Rect(400, 570, 200, 200)  # posición inicial de Homero
rect_boca = pygame.Rect(x, y, w, z)  # rectángulo de la boca para colisiones

# ------------------------------------ PERSONAJE ---------------------------------
# Diccionario que representa al personaje Homero
personaje = {
    "superficie": imagen_homero,
    "rectangulo": rect_homero,
    "rectangulo_boca": rect_boca,
    "puntaje": score,
    "vidas": 3,
    "radio_extra": False,
    "timer_radio": 0
}

# -------------------- CREACIÓN DE LAS ITEMS Y MUSICA DE FONDO -----------
# Crear una lista inicial de los items (cuántas o que tipos de items van a caer)
lista_donas = crear_lista_item(20, "HOMERO\\Recursos\\items\\dona.png")
lista_duff = crear_lista_item(1, "HOMERO\\Recursos\\items\\duff.png")
lista_oveja = crear_lista_item(1, "HOMERO\\Recursos\\items\\oveja.png")
lista_plutonio = crear_lista_item(5, "HOMERO\\Recursos\\items\\barra_plutonio.png")
lista_hamburguesa = crear_lista_item(5, "HOMERO\\Recursos\\items\\hamburguesa.png")
lista_payaso = crear_lista_item(5, "HOMERO\\Recursos\\items\\payaso.png")


# ------------------- CONFIGURACIÓN DEL FONDO DE LA PANTALLA -------------
fondo = pygame.image.load("HOMERO\\Recursos\\pantalla\\fondo.png")
fondo_final = pygame.transform.scale(fondo, tamaño_pantalla)

# ------------------ INICIALIZACIÓN DEL CONTORNO -------------------------
rect_contorno = False

# ------------------------ BUCLE PRINCIPAL DEL JUEGO ---------------------
inicio = True  # variable para mantener el bucle del juego

while inicio:
    RELOJ.tick(FPS)  # establece el FPS del juego
    
    # -------------------------- INICIO DE EVENTOS ------------------------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # cerrar ventana
            inicio = False
            
        elif evento.type == tick:  # tick por estar inicializada en la linea 37
            # actualiza la posición de las items
            pos_item(lista_donas)  
            pos_item(lista_duff)  
            pos_item(lista_oveja)  
            pos_item(lista_plutonio)  
            pos_item(lista_payaso)  
            
        #------------------------------------ CONTORNO--------------------------------------
        # Llamada a contorno dentro del bucle de eventos
        rect_contorno = contorno(evento, rect_contorno)  # Asegúrate de pasar 'event' correctamente

        lista_teclas = pygame.key.get_pressed()  # detecta que tecla fue presionada

        #------------------------------ MOVILIDAD -----------------------------------------
        # Movimiento de Homero utilizando la función
        nueva_imagen = mover_personaje(lista_teclas, rect_homero, rect_boca, imagen_homero_izquierda, imagen_homero_derecha, limite_izquierdo=-30, limite_derecho=600, paso=20)

        if nueva_imagen:
            imagen_homero = nueva_imagen

    # --------------------- VIDAS -------------------------
    # Comprobar si Homero ha perdido
    if personaje["vidas"] == 0:
        guardar_puntaje(personaje["puntaje"])
        # Si las vidas de Homero son cero, mostrar pantalla de Game Over
        resultado = game_over_screen(screen)
        
        if resultado == "Reiniciar!!":
            # Reiniciar el juego
            personaje["vidas"] = 3
            personaje["puntaje"] = 0
            rect_homero.topleft = (400, 570)  # Reiniciar la posición de Homero
            rect_boca.topleft = (x, y)  # Reiniciar la posición de Homero
            lista_donas = crear_lista_item(20, "HOMERO\\Recursos\\items\\dona.png")
            lista_duff = crear_lista_item(1, "HOMERO\\Recursos\\items\\duff.png")
            lista_oveja = crear_lista_item(1, "HOMERO\\Recursos\\items\\oveja.png")
            lista_plutonio = crear_lista_item(5, "HOMERO\\Recursos\\items\\barra_plutonio.png")
            lista_hamburguesa = crear_lista_item(5, "HOMERO\\Recursos\\items\\hamburguesa.png")
            lista_payaso = crear_lista_item(5, "HOMERO\\Recursos\\items\\payaso.png")
            # Aquí reinicias cualquier otra variable o lista si es necesario
        else:
            # Si el jugador elige salir, salir del juego
            inicio = False

    screen.blit(fondo, (0, 0))
    screen.blit(imagen_homero, rect_homero)
    # ----------------------- DIBUJAR ELEMENTOS EN PANTALLA -----------------
    actualizar_pantalla(lista_donas, personaje, screen, rect_contorno)
    actualizar_pantalla(lista_duff, personaje, screen, rect_contorno)
    actualizar_pantalla(lista_oveja, personaje, screen, rect_contorno)
    actualizar_pantalla(lista_plutonio, personaje, screen, rect_contorno)
    actualizar_pantalla(lista_hamburguesa, personaje, screen, rect_contorno)
    actualizar_pantalla(lista_payaso, personaje, screen, rect_contorno)
    
    #-------------- CONTORNO POR PANTALLA -------------------------------
    # Si rect_contorno es True, dibujar los contornos
    if rect_contorno:
        pygame.draw.rect(screen, BLANCO, rect_homero, 2)
        pygame.draw.rect(screen, BLANCO, rect_boca, 2)
    
    # Dibujar elementos en pantalla
    pygame.display.flip()

# -------------------- CIERRE DEL JUEGO -----------------------
pygame.quit()
