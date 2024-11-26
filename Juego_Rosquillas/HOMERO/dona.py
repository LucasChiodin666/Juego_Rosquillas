import pygame
import colores
import random

# Crear una dona en una posición específica y con dimensiones dadas
def crear(x, y, ancho, alto):
    imagen_dona = pygame.image.load("HOMERO\Recursos\dona.png")
    imagen_dona = pygame.transform.scale(imagen_dona, (ancho, alto))
    rect_dona = imagen_dona.get_rect()  # obtiene el rectángulo de la dona
    rect_dona.x = x
    rect_dona.y = y
    dict_dona = {
        "surface": imagen_dona,
        "rect": rect_dona,
        "visible": True,
        "speed": random.randrange(10, 20, 1)  # velocidad aleatoria de caída
    }
    return dict_dona

# Crear una lista de donas con posiciones iniciales aleatorias
def crear_lista_donas(cantidad):
    lista_donas = []
    for i in range(cantidad):
        y = random.randrange(-1000, 0, 60)  # altura inicial aleatoria
        x = random.randrange(0, 740, 60)  # posición X aleatoria
        lista_donas.append(crear(x, y, 60, 60))
    return lista_donas

# Sonido al comer la dona
def niamniam():
    pygame.mixer.init()
    sonido_fondo = pygame.mixer.Sound("HOMERO\Recursos\eat2.mp3")
    sonido_fondo.set_volume(0.7)
    sonido_fondo.play()

# Actualizar posición de las donas en la pantalla
def update(lista_donas):
    for dona in lista_donas:
        rect_dona = dona["rect"]
        rect_dona.y += dona["speed"]  # se mueve hacia abajo según su velocidad

# Dibujar donas en la pantalla y manejar colisiones
def actualizar_pantalla(lista_donas, personaje, ventana_ppal):
    for dona in lista_donas:
        if personaje["rectangulo_boca"].colliderect(dona["rect"]):  # colisión con boca
            personaje["puntaje"] += 100  # incrementa puntaje
            restar_dona(dona)  # reposiciona la dona
            niamniam()  # reproduce sonido de comer
        if dona["rect"].y > 880:  # si la dona toca el piso
            restar_dona(dona)  # reposicionarla arriba
        
        ventana_ppal.blit(dona["surface"], dona["rect"])

    # Muestra el puntaje en la pantalla
    font = pygame.font.SysFont("Arial Narrow", 50)
    text = font.render("SCORE: {0}".format(personaje["puntaje"]), True, colores.ROJO)
    ventana_ppal.blit(text, (0, 0))

# Reposiciona la dona fuera de la pantalla para que reaparezca arriba
def restar_dona(dona):
    dona["rect"].x = random.randrange(0, 740, 60)
    dona["rect"].y = random.randrange(-1000, 0, 60)
