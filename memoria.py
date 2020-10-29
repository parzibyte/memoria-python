import pygame
import sys
import math
import time
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()
NOMBRE_IMAGEN_OCULTA = "ocultar.png"
MEDIDA_CUADRADO = 150
SEGUNDOS_MOSTRAR_PIEZA = 1

imagen_oculta = pygame.image.load(NOMBRE_IMAGEN_OCULTA)
imagen_oculta = pygame.transform.scale(imagen_oculta, (MEDIDA_CUADRADO, MEDIDA_CUADRADO))


class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierta = False
        self.fuente_imagen = fuente_imagen
        imagen_real = pygame.image.load(fuente_imagen)
        self.imagen_real = pygame.transform.scale(imagen_real, (MEDIDA_CUADRADO, MEDIDA_CUADRADO))


cuadros = [
    [Cuadro("conejo.jpg"), Cuadro("conejo.jpg"), Cuadro("leon.jpg"), Cuadro("leon.jpg")],
    [Cuadro("oveja.jpg"), Cuadro("oveja.jpg"), Cuadro("perro.jpg"), Cuadro("perro.jpg")],
    [Cuadro("gato.jpg"), Cuadro("gato.jpg"), Cuadro("cabra.jpg"), Cuadro("cabra.jpg")],
    [Cuadro("cocodrilo.jpg"), Cuadro("cocodrilo.jpg"), Cuadro("huron.jpg"), Cuadro("huron.jpg")],
]


def ocultar_todos_los_cuadros():
    print("Ocultando cuadros")
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierta = False


def aleatorizar_cuadros():
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal


def comprobar_si_gana():
    if gana():
        pygame.mixer.Sound.play(sonido_exito)
        reiniciar_juego()


def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierta:
                return False
    return True


def reiniciar_juego():
    global juego_iniciado
    juego_iniciado = False


def iniciar_juego():
    pygame.mixer.Sound.play(sonido_clic)
    global juego_iniciado
    # Aleatorizar 3 veces
    for i in range(3):
        # TODO: descomentar cuando se dejen de hacer pruebas
        # aleatorizar_cuadros()
        pass
    ocultar_todos_los_cuadros()

    # pygame.mixer.Channel(0).play(pygame.mixer.Sound("click.mpeg"))
    juego_iniciado = True


sonido_fondo = pygame.mixer.Sound("fondo.wav")
sonido_clic = pygame.mixer.Sound("clic.wav")
sonido_exito = pygame.mixer.Sound("exito.wav")
sonido_fracaso = pygame.mixer.Sound("fracaso.wav")
pygame.mixer.Sound.play(sonido_fondo, -1)
ALTURA_BOTON = 30
anchura_pantalla = len(cuadros[0]) * MEDIDA_CUADRADO
altura_pantalla = (len(cuadros) * MEDIDA_CUADRADO) + ALTURA_BOTON

ANCHURA_BOTON = anchura_pantalla
pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
pygame.display.set_caption('Memoria')

boton = pygame.Rect(0, altura_pantalla - ALTURA_BOTON, ANCHURA_BOTON, altura_pantalla)

cuadro_actual = None
deberia_ocultar = False
ultimos_segundos = None
puede_jugar = True
juego_iniciado = False
x1 = None
y1 = None
x2 = None
y2 = None

color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
tamanio_fuente = 20
fuente = pygame.font.SysFont("Arial", tamanio_fuente)
xFuente = int((ANCHURA_BOTON / 2) - (tamanio_fuente / 2))
yFuente = int(altura_pantalla - ALTURA_BOTON)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:

            xx, yy = event.pos
            if boton.collidepoint(event.pos):
                if not juego_iniciado:
                    iniciar_juego()

            else:
                # Si no hay juego iniciado, ignoramos el clic
                if not juego_iniciado:
                    continue
                x = math.floor(xx / MEDIDA_CUADRADO)
                y = math.floor(yy / MEDIDA_CUADRADO)
                # Primero lo primero. Si  ya está mostrada o descubierta, no hacemos nada
                cuadro = cuadros[y][x]
                if cuadro.mostrar or cuadro.descubierta:
                    continue
                # Si es la primera vez que tocan la imagen (es decir, no están buscando el par de otra, sino apenas
                # están descubriendo la primera)
                if x1 is None and y1 is None:
                    # Entonces la actual es en la que acaban de dar clic, la mostramos
                    x1 = x
                    y1 = y
                    cuadros[y1][x1].mostrar = True
                    print("OK tienes una, busca su par")
                else:
                    # En caso de que ya hubiera una clickeada anteriormente y estemos buscando el par, comparamos...
                    x2 = x
                    y2 = y
                    cuadros[y2][x2].mostrar = True
                    cuadro1 = cuadros[y1][x1]
                    cuadro2 = cuadros[y2][x2]
                    # Si coinciden, entonces a ambas las ponemos en descubiertas:
                    if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                        print("Sí era! le diste")
                        cuadros[y1][x1].descubierta = True
                        cuadros[y2][x2].descubierta = True
                        x1 = None
                        x2 = None
                        y1 = None
                        y2 = None
                    else:
                        pygame.mixer.Sound.play(sonido_fracaso)
                        # Si no, tenemos que ocultarlas en el plazo de 1 segundo. Así que establecemos la bandera
                        ultimos_segundos = int(time.time())
                        print("No era, vamos a ocultarlas en 3 segundos")
                        print(ultimos_segundos)
                        puede_jugar = False
                comprobar_si_gana()

    ahora = int(time.time())
    if ultimos_segundos is not None and ahora - ultimos_segundos >= 2:
        print("Se oculta")
        print(ahora)
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        ultimos_segundos = None
        puede_jugar = True

    pantalla_juego.fill(color_blanco)
    x = 0
    y = 0
    for fila in cuadros:
        x = 0
        for cuadro in fila:
            if cuadro.descubierta or cuadro.mostrar:
                pantalla_juego.blit(cuadro.imagen_real, (x, y))
            else:
                pantalla_juego.blit(imagen_oculta, (x, y))
            x += MEDIDA_CUADRADO
        y += MEDIDA_CUADRADO

    # También dibujamos el botón
    if juego_iniciado:
        pygame.draw.rect(pantalla_juego, color_blanco, boton)
        pantalla_juego.blit(fuente.render("Iniciar juego", True, color_gris), (xFuente, yFuente))
    else:
        pygame.draw.rect(pantalla_juego, color_blanco, boton)
        pantalla_juego.blit(fuente.render("Iniciar juego", True, color_negro), (xFuente, yFuente))

    pygame.display.update()
