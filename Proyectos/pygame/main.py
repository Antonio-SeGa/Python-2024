import pygame
import random
import math
from pygame import mixer

# Inicializa Pygame
pygame.init()

# Crea la pantalla
pantalla = pygame.display.set_mode((800,600))

# Titulo e icono
pygame.display.set_caption("Invación espacial")
icono = pygame.image.load('Proyectos\\pygame\\ovni.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Proyectos\\pygame\\Fondo.jpg')

#Agregar musica
mixer.music.load('Proyectos\\pygame\\MusicaFondo.mp3')
mixer.music.set_volume(0.6)
mixer.music.play(-1)


# Variables de Jugador 
img_judador = pygame.image.load('Proyectos\\pygame\\cohete.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Variables de enemigo 
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 5

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('Proyectos\\pygame\\enemigo.png'))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Variables de bala 
balas = []
img_bala = pygame.image.load('Proyectos\\pygame\\Bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 2.5
bala_visible = False

# Variable global
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf',32)
texto_x = 10
texto_y = 10

# Texto final de juego
fuente_final = pygame.font.Font('freesansbold.ttf',40)

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255,255,255))
    pantalla.blit(mi_fuente_final,(60,200))

# funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255,255,255))
    pantalla.blit(texto, (x, y))


# Función jugador
def jugador(x,y):
    pantalla.blit(img_judador, (x, y))

# Función enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# Funcion disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala,(x+16, y+10))

# Funcion detectar colision
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False

# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # imagen de fondo
    pantalla.blit(fondo,(0,0))
    # jugador_x += 0.1

    # Iterar eventos
    for evento in pygame.event.get():
        # Event Cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # tecla presionada
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.9
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.9
            # Disparar bala
            if evento.key == pygame.K_SPACE:
                sonido_disparo = mixer.Sound('Proyectos\\pygame\\disparo.mp3')
                sonido_disparo.play()
                '''if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)'''
                nueva_vala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_vala)
        # Tecla soltar
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicación del jugador
    jugador_x += jugador_x_cambio
    # Mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736
    

    # Modificar ubicación del enemigo
    for e in range(cantidad_enemigos):
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]
        # Mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.9
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.9
            enemigo_y[e] += enemigo_y_cambio[e]
        
        # Colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound('Proyectos\\pygame\\Golpe.mp3')
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break
        
        
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    '''if bala_y <= -64:
        bala_y = 500 
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio'''
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)



    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    # Actualizar
    pygame.display.update()