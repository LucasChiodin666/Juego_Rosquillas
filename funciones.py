import pygame
import sys
import constantes
import random
import json
import os
import time

#--------------------------CREADOR DE ITEMS LINEAS 29 FUNCIONES ---------------------------------
# Crear una dona en una posición específica y con dimensiones dadas
def crear(x, y, ancho, alto, imagen_item):
    imagen_objeto = pygame.image.load(imagen_item)
    imagen_objeto = pygame.transform.scale(imagen_objeto, (ancho, alto))
    rect_item = imagen_objeto.get_rect()  # obtiene el rectángulo de la dona
    rect_item.x = x
    rect_item.y = y
    dict_item = {
        "superficie": imagen_objeto,# superficie
        "rect": rect_item,# rectangulo
        "tipo": imagen_item,# imagenes de los items
        "visible": False,
        "velocidad": random.randrange(10, 20, 1)  # velocidad aleatoria de caída
    }
    return dict_item

#--------------------------GENERADOR DE ITEMS LINEAS 68 A 73 GAME ---------------------------------
# Crear una lista de donas con posiciones iniciales aleatorias
def crear_lista_item(cantidad, imagen_item):
    lista_items = []
    for i in range(cantidad):
        y = random.randrange(-900, 0, 60)  # altura inicial aleatoria
        x = random.randrange(15, 740, 45)  # posición X aleatoria
        lista_items.append(crear(x, y, 70, 70, imagen_item))
    return lista_items



#--------------------------EVENTOS DE SONIDO LINEAS DENTRO DE ACTUALIZAR_PANTALLA ------------------------------
#--------------------------EVENTOS DE SONIDO LINEAS 30 GAME ---------------------------------
# Sonido al comer item
def sonido(sonido, volumen):
    pygame.mixer.init()
    sonido_fondo = pygame.mixer.Sound(sonido)
    sonido_fondo.set_volume(volumen)
    sonido_fondo.play()
    


#--------------------------GENERADOR DE ITEMS EN CAIDA LINEA 97 A 100 - GAME ---------------------------------
# Actualizar posición de las donas en la pantalla
def pos_item(lista_item):
    for item in lista_item:
        rect_item = item["rect"]
        rect_item.y += item["velocidad"]  # se mueve hacia abajo según su velocidad

#--------------------------ELIMINACION DE ITEMS LINEA 95 A 98 - FUNCIONES---------------------------------
# Reposiciona la dona fuera de la pantalla para que reaparezca arriba
def restar_item(item):
    item["rect"].x = random.randrange(0, 740, 60)
    item["rect"].y = random.randrange(-1000, 0, 60)


#--------------------------ACTUALIZACION DE ACCIONES LINEA 126 A 129 - GAME----------------------------------
# Reposiciona la dona fuera de la pantalla para que reaparezca arriba
def actualizar_pantalla(lista_items, personaje, ventana_ppal, contorno):
    """
    Actualiza los elementos en la pantalla, detecta colisiones y maneja el puntaje, las vidas y los efectos visuales.
    
    Args:
        lista_items (list): Lista de ítems en el juego.
        personaje (dict): Datos del personaje (puntaje, vidas, etc.).
        ventana_ppal (pygame.Surface): Superficie principal del juego.
        contorno (bool): Si `True`, dibuja los contornos de los rectángulos de colisión.
    """
    # Procesar los ítems
    for item in lista_items:
        if personaje["rectangulo_boca"].colliderect(item["rect"]): # colliderect comprueba si dos rect se superponen
            # Manejo de ítems según su tipo
            if item["tipo"] == "HOMERO\\Recursos\\items\\dona.png":
                personaje["puntaje"] += 100
                sonido("HOMERO\\Recursos\\sonidos\\dona.mp3", 5.0)
                
            if item["tipo"] == "HOMERO\\Recursos\\items\\hamburguesa.png":
                personaje["puntaje"] += 500
                
            elif item["tipo"] == "HOMERO\\Recurso\\items\\mano_mono.png":
                personaje["radio_extra"] = True
                personaje["timer_radio"] = pygame.time.get_ticks() + 5000  # 5 segundos
                
            elif item["tipo"] == "HOMERO\\Recursos\\items\\duff.png":
                personaje["vidas"] += 1
                
                sonido("HOMERO\\Recursos\\sonidos\\eructo.mp3", 0.1)
                personaje["puntaje"] += 1000
                
            elif item["tipo"] == "HOMERO\\Recursos\\items\\barra_plutonio.png":
                personaje["vidas"] -= 1
                sonido("HOMERO\\Recursos\\sonidos\\douh.mp3", 1.0)
            
            elif item["tipo"] == "HOMERO\\Recursos\\items\\payaso.png":
                personaje["puntaje"] -= 1000
                sonido("HOMERO\\Recursos\\sonidos\\douh.mp3", 1.0)
                
            elif item["tipo"] == "HOMERO\\Recursos\\items\\oveja.png":
                personaje["vidas"] = 0
                sonido("HOMERO\\Recursos\\sonidos\\fin_del_juego.mp3", 5.0)
                
            restar_item(item)
        if item["rect"].y > 880:  # Si el ítem sale de la pantalla
            restar_item(item)
        ventana_ppal.blit(item["superficie"], item["rect"])
        
        if contorno:
            pygame.draw.rect(ventana_ppal, constantes.BLANCO, item["rect"], 2)

    # Temporizador de "Mano de Mono"
    if personaje["radio_extra"] and pygame.time.get_ticks() > personaje["timer_radio"]:
        personaje["radio_extra"] = False

    # Dibujar el puntaje y las vidas
    font = pygame.font.Font(None, 50)  # Usar fuente predeterminada
    ventana_ppal.blit(font.render(f"PUNTAJE: {personaje['puntaje']}", True, (255, 0, 0)), (0, 0))
    ventana_ppal.blit(font.render(f"VIDAS: {personaje['vidas']}", True, (255, 0, 0)), (0, 50))
    

#-------------------------- VISUALIZA CONTORNO DE LOS OBJETOS - LINEA - 99 A 100 FUNCIONES----------------------------
#-------------------------- VISUALIZA CONTORNO DE LOS OBJETOS - LINEA - 133 A 135 GAME----------------------------
def contorno(evento, contorno):
    """
    Alterna la visibilidad del contorno de los rectángulos en pantalla al presionar la tecla 'C'.

    Argumentos:
        event (pygame.event.Event): El evento capturado por Pygame.
        show_contour (bool): Estado actual de la visibilidad del contorno.

    Retorno:
        bool: El nuevo estado de visibilidad del contorno.
    """
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_c:  # Tecla "C" para alternar el contorno
            contorno = not contorno
    return contorno



#------------------------------ PANTALLA DE INICIO - LINEA 33 - GAME-----------------------------------
def pantallas_con_boton(imagen_fondo, texto_boton, pos_boton_x, pos_boton_y, ancho_boton, alto_boton, color_boton):
    """
    Muestra una pantalla inicial con un fondo y botones interactivos que realizan diferentes acciones.

    Argumentos:
        imagen_fondo (str): Ruta de la imagen de fondo.
        texto_boton (str): Texto a mostrar en el botón.
        pos_boton_x (int): Coordenada X del botón.
        pos_boton_y (int): Coordenada Y del botón.
        ancho_boton (int): Ancho del botón.
        alto_boton (int): Alto del botón.
        color_boton (tuple): Color del botón en formato RGB.

    Retorno:
        bool: `False` si el jugador comienza el juego, `True` si permanece en la pantalla inicial.
    """
    imagen_inicio = pygame.image.load(imagen_fondo)
    imagen_inicio = pygame.transform.scale(imagen_inicio, (800, 800))
    screen = pygame.display.set_mode([800, 800])
    
    esperando = True

    while esperando:
        boton_jugar = dibujar_boton(imagen_inicio, "", 400, 250, 300, 50, color_boton, "HOMERO\\Recursos\\pantalla\\start.png")
        boton_score = dibujar_boton(imagen_inicio, "", 400, 350, 300, 50, color_boton, "HOMERO\\Recursos\\pantalla\\score.png")
        boton_exit = dibujar_boton(imagen_inicio, "", 400, 450, 300, 50, color_boton, "HOMERO\\Recursos\\pantalla\\exit(1).png")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    esperando = False
                elif boton_score.collidepoint(event.pos):
                    mostrar_puntajes(screen)
                    
                elif boton_exit.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        screen.blit(imagen_inicio, (0, 0))

    return esperando


#--------------------- FUNCION DE CREAR BOTON - LINEA DE 156 A 158 - FUNCIONES------------------------------------------------
def dibujar_boton(pantalla, texto, pos_x, pos_y, ancho, alto, color, imagen=None):
    """

    Argumentos:
        pantalla (pygame.Surface): La superficie donde se dibujará el botón.
        texto (str): El texto a mostrar en el botón.
        pos_x (int): Coordenada X de la posición del botón.
        pos_y (int): Coordenada Y de la posición del botón.
        ancho (int): Ancho del botón.
        alto (int): Alto del botón.
        color (tuple): Color del botón en formato RGB.
        imagen (str, opcional): Ruta de la imagen a colocar sobre el botón.

    Retorno:
        pygame.Rect: Un objeto Rect que representa el área del botón.
    """
    rect_boton = pygame.Rect(pos_x, pos_y, ancho, alto)
    pygame.draw.rect(pantalla, color, rect_boton)

    fuente = pygame.font.Font(None, 36)
    texto_boton = fuente.render(texto, True, color)
    pantalla.blit(
        texto_boton,
        (pos_x + (ancho - texto_boton.get_width()) // 2,
         pos_y + (alto - texto_boton.get_height()) // 2)
    )

    if imagen:
        imagen_cargada = pygame.image.load(imagen)
        imagen_cargada = pygame.transform.scale(imagen_cargada, (ancho, alto))
        pantalla.blit(imagen_cargada, (pos_x, pos_y))

    return rect_boton

#--------------------------MOVILIDAD DE PERSONAJE LINEA - 111- GAME -------------------------------------------
def mover_personaje(teclas, rect_personaje, rect_boca, imagen_izquierda, imagen_derecha, limite_izquierdo, limite_derecho, paso):
    """
    Maneja el movimiento horizontal del personaje y actualiza su dirección.

    Argumentos:
        teclas (list): Lista de teclas presionadas (pygame.key.get_pressed()).
        rect_personaje (pygame.Rect): Rectángulo principal del personaje.
        rect_boca (pygame.Rect): Rectángulo que representa la boca del personaje.
        imagen_izquierda (pygame.Surface): Imagen del personaje mirando a la izquierda.
        imagen_derecha (pygame.Surface): Imagen del personaje mirando a la derecha.
        limite_izquierdo (int): Límite izquierdo de movimiento.
        limite_derecho (int): Límite derecho de movimiento.
        paso (int): Cantidad de píxeles que se mueve el personaje por acción.

    Retorno:
        pygame.Surface: Imagen actualizada del personaje (izquierda o derecha). Retorna `None` si no hay movimiento.
    """
    if teclas[pygame.K_LEFT]:
        nueva_x = rect_personaje.x - paso
        if nueva_x > limite_izquierdo:
            rect_personaje.x -= paso
            rect_boca.x -= paso
        return imagen_izquierda

    if teclas[pygame.K_RIGHT]:
        nueva_x = rect_personaje.x + paso
        if limite_izquierdo < nueva_x < limite_derecho:
            rect_personaje.x += paso
            rect_boca.x += paso
        return imagen_derecha

    return None
#------------------------------- GAME OVER --------------------------------------------------------
def game_over_screen(screen):
    # Cargar las imágenes
    imagen_homero_mal = pygame.image.load("HOMERO\Recursos\pantalla\ouh.png")  # Imagen de Homero mal
    imagen_homero_mal = pygame.transform.scale(imagen_homero_mal, (800, 800))  # Ajustar tamaño
    
    imagen_homero_muerto = pygame.image.load("HOMERO\Recursos\pantalla\game_over.png")  # Imagen de Homero muerto
    imagen_homero_muerto = pygame.transform.scale(imagen_homero_muerto, (800, 800))  # Ajustar tamaño
    
    imagen_game_over = pygame.image.load("HOMERO\Recursos\pantalla\game_over.png")  # Imagen de Game Over
    imagen_game_over = pygame.transform.scale(imagen_game_over, (800, 800))

    imagen_exit = pygame.image.load("HOMERO\Recursos\pantalla\exit.png")  # Botón de Exit
    imagen_exit = pygame.transform.scale(imagen_exit, (200, 100))  # Ajustar tamaño del botón

    imagen_restart = pygame.image.load("HOMERO\Recursos\pantalla\play-again.png")  # Botón de Restart
    imagen_restart = pygame.transform.scale(imagen_restart, (200, 100))  # Ajustar tamaño del botón

    # Rectángulos de los botones
    exit_rect = imagen_exit.get_rect(center=(400, 650))  # Ajusta la posición
    restart_rect = imagen_restart.get_rect(center=(400, 550))  # Ajusta la posición
    
    # Reproducir sonido de muerte
    sonido("HOMERO\\Recursos\\sonidos\\fin_del_juego.mp3", 0.5)

    # Mostrar la imagen de Homero mal durante 3 segundos
    start_ticks = pygame.time.get_ticks()  # Tiempo inicial
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Cerrar el juego
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar el juego
                    return "Reiniciar!!"
                elif event.key == pygame.K_q:  # Salir del juego
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):  # Si el clic está sobre el botón de Exit
                    pygame.quit()
                    sys.exit()
                elif restart_rect.collidepoint(event.pos):  # Si el clic está sobre el botón de Restart
                    return "Reiniciar!!"
        
        # Dibujar la imagen de Homero mal durante 3 segundos
        screen.blit(imagen_homero_mal, (0, 0))
        
        # Si han pasado 3 segundos, cambiar a la imagen de Homero muerto
        if pygame.time.get_ticks() - start_ticks > 3000:  # 3000 ms = 3 segundos
            screen.blit(imagen_homero_muerto, (0, 0))  # Mostrar Homero muerto
            screen.blit(imagen_game_over, (0, 0))  # Mostrar Game Over
            screen.blit(imagen_restart, restart_rect)  # Mostrar botón de Restart
            screen.blit(imagen_exit, exit_rect)  # Mostrar botón de Exit
        
        pygame.display.flip()  # Actualizar la pantalla


# Ruta absoluta al archivo JSON
directorio_homero = os.path.dirname(os.path.abspath(__file__))
ruta_puntajes = os.path.join(directorio_homero, "puntajes.json")


def guardar_puntaje(puntaje):
    """
    Guarda el puntaje final del jugador en un archivo JSON en la carpeta HOMERO.
    """
    try:
        with open(ruta_puntajes, "r") as archivo:
            puntajes = json.load(archivo)  # Cargar las puntuaciones previas
    except (FileNotFoundError, json.JSONDecodeError):
        puntajes = []  # Si no existe el archivo o está vacío, inicializar una lista vacía

    # Asegurar que el puntaje es un número o un diccionario válido
    if isinstance(puntaje, (int, float, str)):
        puntajes.append({"puntaje": puntaje})
    elif isinstance(puntaje, dict):
        puntajes.append(puntaje)
    else:
        raise ValueError("El puntaje debe ser un número, texto o un diccionario válido.")

    # Guardar la lista de puntajes en el archivo JSON
    with open(ruta_puntajes, "w") as archivo:
        json.dump(puntajes, archivo, indent=4)  # Guardar el archivo con formato legible


def cargar_puntajes():
    """
    Carga las puntuaciones desde el archivo JSON.
    """
    try:
        with open(ruta_puntajes, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def mostrar_puntajes(screen):
    """
    Muestra la pantalla de puntuaciones con un contador regresivo de 5 segundos.
    """
    # Cargar puntuaciones desde el archivo JSON
    puntuaciones = cargar_puntajes()

    # Configurar la fuente para mostrar las puntuaciones y el temporizador
    fuente = pygame.font.SysFont("Arial", 30)

    # Inicio del temporizador
    tiempo_total = 5  # Segundos
    inicio = time.time()

    corriendo = True
    while corriendo:
        # Tiempo transcurrido
        tiempo_actual = time.time()
        tiempo_restante = max(0, int(tiempo_total - (tiempo_actual - inicio)))

        # Limpiar pantalla
        screen.fill((0, 0, 0))

        # Mostrar título
        texto_titulo = fuente.render("Puntuaciones", True, (255, 255, 255))
        screen.blit(texto_titulo, (320, 100))

        # Mostrar cada puntuación
        y_offset = 150
        for puntaje in puntuaciones:
            if isinstance(puntaje, dict):  # Si es un diccionario
                texto_puntaje = fuente.render(f"Puntaje: {puntaje.get('puntaje', 'N/A')}", True, (255, 255, 255))
            else:  # Si es un número u otro tipo de dato
                texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
            screen.blit(texto_puntaje, (320, y_offset))
            y_offset += 40

        # Mostrar temporizador
        texto_temporizador = fuente.render(f"Tiempo restante: {tiempo_restante} s", True, (255, 255, 255))
        screen.blit(texto_temporizador, (320, y_offset + 40))

        # Actualizar pantalla
        pygame.display.flip()

        # Verificar si el tiempo se ha agotado
        if tiempo_restante <= 0:
            corriendo = False

        # Manejar eventos de salida para evitar que el programa se cuelgue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()