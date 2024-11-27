import pygame
import constantes
import random

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
        boton_exit = dibujar_boton(imagen_inicio, "", 400, 450, 300, 50, color_boton, "HOMERO\\Recursos\\pantalla\\exit.png")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    esperando = False
                elif boton_score.collidepoint(event.pos):
                    pass
                elif boton_exit.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        screen.blit(imagen_inicio, (0, 0))

    return esperando
#--------------------- FUNCION DE CREAR BOTON - LINEA DE 156 A 158 - FUNCIONES------------------------------------------------
def dibujar_boton(pantalla, texto, pos_x, pos_y, ancho, alto, color, imagen=None):
    """
    Dibuja un botón interactivo en la pantalla y, opcionalmente, coloca una imagen sobre él.

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