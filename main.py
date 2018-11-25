#! /usr/bin/env python
#-*- coding: UTF-8 -*-

import pygame, sys
from mtn_GUI import *
from UltraColor import *
from constants import *

pygame.init()

# Variables globales
FPS = 0
fps_font = pygame.font.Font("recursos/paris.fon", 20)
clock = pygame.time.Clock()
Context.screen = "inicio" #  inicio, continuar, configurar, nuevo, vprevia, plantillas, pausa, juego, fin
Context.prevScreen = ""  #  Se usa para saber de donde vinimos al hacer un cambio de pantalla
deltatime = 1


#  Funciones utiles
def show_fps():
    fps_overlay = fps_font.render(str(FPS), True, Color.Goldenrod)
    #pantallaActiva = fps_font.render(pantalla, True, Color.Goldenrod)
    altura_linea = fps_font.get_linesize() +10
    window.blit(fps_overlay, (0, 0))
    #window.blit(pantallaActiva, (0, altura_linea))

def create_window():
    global window, window_height, window_width, window_title
    window_width, window_height = (1366,768) #800, 600  # 800, 800 *9/16  (mantiene una relacion 16:9)
                                            # 1366, 768 (resolucion de maquina HP)
    window_title = "Laberinto" 
    pygame.display.set_caption(window_title)
    pygame.display.set_icon(pygame.image.load('recursos/logo-laberinto-32x32.png'))
    window = pygame.display.set_mode((window_width, window_height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
    window_width, window_height = window.get_size()
    #print window.get_size()


def count_fps():
    global FPS, clock

    FPS = clock.get_fps()
    if FPS > 0:
        deltatime = 1 / FPS


def goto_inicio(boton):
    ##global pantalla, pantAnterior

    Context.prevScreen = Context.screen
    Context.screen = "inicio" 

def goto_continuar(boton):
    #global pantalla, pantAnterior

    Context.prevScreen = Context.screen
    Context.screen = "continuar"    

def goto_configurar(boton):
    #global pantalla, pantAnterior

    Context.prevScreen = Context.screen
    Context.screen = "configurar"  

def goto_nuevo(boton):
    #global pantalla, pantAnterior

    Context.prevScreen = Context.screen
    Context.screen = "nuevo"  

def goto_vprevia(boton):
    #global pantalla, pantAnterior

    Context.prevScreen = Context.screen
    Context.screen = "vprevia"

def goto_plantillas(boton):
    #global pantalla, pantAnterior

    Context.prevScreen = Context.screen
    Context.screen = "plantillas"    

def goto_pausa(boton):
    #global pantalla, pantAnterior

    Context.prevScreen = Context.screen
    Context.screen = "pausa"    

def goto_juego(boton):
    #global pantalla, pantAnterior

    Context.prevScreen = Context.screen
    Context.screen = "juego"   

def goto_fin(boton):
    #global pantalla, pantAnterior

    Context.prevScreen = Context.screen
    Context.screen = "fin" 

def goto_pantAnterior(boton):
    #global pantalla, pantAnterior

    aux = Context.prevScreen
    Context.prevScreen = Context.screen
    Context.screen = aux

def salir(boton):
    #global isRunning
    Context.isRunning=False


create_window()

#########################################################################
#########################################################################
##                                                                     ##
##                       PANTALLAS DEL JUEGO                           ##
##                                                                     ##
#########################################################################
#########################################################################
margenIzq = window_width*0.1  #  Margen izquierdos de los menus
sepTit = 15  #  Separacion entre el elemento y el titulo
sep = 1  #  Separacion cercanaentre elementos
sep2 = 12  #  Separacion lejana entre elementos
anchoBoton = 250
altoBoton = 30

###############################################
#             Pantalla de inicio              #
###############################################
    #  Imagen de inicio
bitmapIlustracion = pygame.image.load('recursos/Laberinto3.png')
imgIlustracion_rect = bitmapIlustracion.get_rect(center = (window_width/2, 75))
imgIlustracion = Image(imgIlustracion_rect, bitmapIlustracion)
del bitmapIlustracion
imgIlustracion.screens = ("inicio",)
imgIlustracion.border = False

    #  Titulo del juego
lblTitulo_rect = (0,        175,  window_width,  60)
lblTitulo = Label(lblTitulo_rect, "LABERINTO")
lblTitulo.font = Font.Large
lblTitulo.align = A_CENTER
lblTitulo.screens = ("inicio",)

    #  Botones
btnContinuar_rect = (window_width/2-125,     310,  anchoBoton,  altoBoton)
btnContinuar = Button(btnContinuar_rect, goto_continuar, "CONTINUAR")
btnContinuar.align = A_CENTER
btnContinuar.screens = ("inicio",)

btnNuevo_rect = (window_width/2-125,         345,  anchoBoton,  altoBoton)
btnNuevo = Button(btnNuevo_rect, goto_nuevo, "NUEVO")
btnNuevo.align = A_CENTER
btnNuevo.screens = ("inicio",)

btnConfiguracion_rect = (window_width/2-125, 380,  anchoBoton,  altoBoton)
btnConfiguracion = Button(btnConfiguracion_rect, goto_configurar, "CONFIGURACION")
btnConfiguracion.align = A_CENTER
btnConfiguracion.screens = ("inicio",)

btnSalir_rect = (window_width/2-125,         415,  anchoBoton,  altoBoton)
btnSalir = Button(btnSalir_rect, salir, "SALIR")
btnSalir.align = A_CENTER
btnSalir.screens = ("inicio",)

lblCreditos_rect = (margenIzq, window_height - 70,  window_width-margenIzq*2,  20)
lblCreditos = Label(lblCreditos_rect, "Idea, diseno y programacion por Martincholp")
lblCreditos.font = Font.Small
lblCreditos.align = A_RIGHT
lblCreditos.screens = ("inicio",)

###############################################
#          Pantalla de configuracion          #
###############################################


    #  Titulo de la pantalla
lblTituloConfig_rect = (lblTitulo_rect[0], 25, lblTitulo_rect[2], lblTitulo_rect[3])
lblConfig = Label(lblTituloConfig_rect, "CONFIGURACION")
lblConfig.font = Font.Large
lblConfig.align = A_CENTER
lblConfig.screens = ("configurar",)

    #  Labels y textbox de los directorios
lbl1Config_rect = (margenIzq, lblTituloConfig_rect[1]+lblTituloConfig_rect[3]+sepTit, window_width*0.8, 25)
txt1Config_rect = (margenIzq, lbl1Config_rect[1]+lbl1Config_rect[3]+sep, window_width*0.8, 25)
lbl2Config_rect = (margenIzq, txt1Config_rect[1]+txt1Config_rect[3]+sep+sep2, window_width*0.8, 25)
txt2Config_rect = (margenIzq, lbl2Config_rect[1]+lbl2Config_rect[3]+sep, window_width*0.8, 25)
lbl3Config_rect = (margenIzq, txt2Config_rect[1]+txt2Config_rect[3]+sep+sep2, window_width*0.8, 25)
txt3Config_rect = (margenIzq, lbl3Config_rect[1]+lbl3Config_rect[3]+sep, window_width*0.8, 25)
lbl4Config_rect = (margenIzq, txt3Config_rect[1]+txt3Config_rect[3]+sep+sep2, window_width*0.8, 25)
txt4Config_rect = (margenIzq, lbl4Config_rect[1]+lbl4Config_rect[3]+sep, window_width*0.8, 25)
lbl5Config_rect = (margenIzq, txt4Config_rect[1]+txt4Config_rect[3]+sep+sep2, window_width*0.8, 25)
txt5Config_rect = (margenIzq, lbl5Config_rect[1]+lbl5Config_rect[3]+sep, window_width*0.8, 25)

lbl1Config = Label(lbl1Config_rect, "Directorio de juegos guardados")
txt1Config = Textbox(txt1Config_rect, "Laberintos/guardados")
lbl2Config = Label(lbl2Config_rect, "Directorio de plantillas")
txt2Config = Textbox(txt2Config_rect, "Laberintos/plantillas")
lbl3Config = Label(lbl3Config_rect, "Directorio de capturas")
txt3Config = Textbox(txt3Config_rect, "Laberintos/capturas")
lbl4Config = Label(lbl4Config_rect, "Directorio de algoritmos")
txt4Config = Textbox(txt4Config_rect, "Laberintos/algoritmos")
lbl5Config = Label(lbl5Config_rect, u"Directorio de estilos")
txt5Config = Textbox(txt5Config_rect, '')  #"Laberintos/estilos")

lblytxt = [lbl1Config, txt1Config, lbl2Config, txt2Config, lbl3Config, txt3Config, lbl4Config,txt4Config, lbl5Config, txt5Config]

for elem in lblytxt:
    elem.screens = ("configurar",)
    elem.align = None
    elem.color_foreground = Color.YellowGreen

    #  Configuracion de sonido, tamano de celdas y pantalla completa
lbl6Config_rect = (margenIzq, txt5Config_rect[1]+txt5Config_rect[3]+sepTit, 150, 35)  # Label sonido

chk1Config_rect = (margenIzq, lbl6Config_rect[1]+lbl6Config_rect[3]+sep2, 25, 25)  # Checkbox musica
chk2Config_rect = (margenIzq, chk1Config_rect[1]+chk1Config_rect[3]+10, 25, 25)  # Checkbox fx

lbl7Config_rect = (chk1Config_rect[0]+chk1Config_rect[2]+sep2*2, chk1Config_rect[1], 100, 25)  # Label musica
lbl8Config_rect = (chk2Config_rect[0]+chk2Config_rect[2]+sep2*2, chk2Config_rect[1], 100, 25)  # Label fx

sld1Config_rect = (lbl7Config_rect[0]+lbl7Config_rect[2]+sep2*2,  lbl7Config_rect[1], 200, 25)  # Slider musica
sld2Config_rect = (lbl8Config_rect[0]+lbl8Config_rect[2]+sep2*2,  lbl8Config_rect[1], 200, 25)  # Slider fx

lbl9Config_rect = (margenIzq+window_width/2, chk1Config_rect[1], 200, 25)  # Label tamano celda
lbl10Config_rect = (margenIzq+window_width/2, chk2Config_rect[1], 200, 25) # Label pantalla completa

chk3Config_rect = (lbl9Config_rect[0]+lbl9Config_rect[2], lbl9Config_rect[1], 60, 25)  # RollList tamano
chk4Config_rect = (lbl10Config_rect[0]+lbl10Config_rect[2]+sep2*2, lbl10Config_rect[1], 25, 25)  # Checkbox pantalla completa

lbl6Config = Label(lbl6Config_rect, "Sonidos")
lbl6Config.font = Font.Scanner
lbl6Config.font.set_underline(True)
lbl6Config.updateGraphics()  #text = "Sonidos"
lbl7Config = Label(lbl7Config_rect, "Musica")
lbl8Config = Label(lbl8Config_rect, "FX")
lbl9Config = Label(lbl9Config_rect, "Tamano de celda")
lbl10Config = Label(lbl10Config_rect, "Pantalla completa")

lbl2 = [lbl6Config, lbl7Config, lbl8Config, lbl9Config, lbl10Config ]

for lbl in lbl2:
    lbl.screens = ("configurar",)
    lbl.align = A_LEFT

chk1Config = CheckBox(chk1Config_rect, True)
chk1Config.screens = ("configurar",)
chk2Config = CheckBox(chk2Config_rect, True)
chk2Config.screens = ("configurar",)
rll3Config = RollList(chk3Config_rect, ("1","2","3","4","5","6","7","8","9","10"))  
rll3Config.screens = ("configurar",)
rll3Config.loop = False
rll3Config.align = None
rll3Config.pos_text = (3,2)
chk4Config = CheckBox(chk4Config_rect, True)
chk4Config.screens = ("configurar",)

sld1Config = Slider(sld1Config_rect)
sld1Config.screens = ("configurar",)
sld2Config = Slider(sld2Config_rect)
sld2Config.screens = ("configurar",)

    #  Botones aceptar y cancelar
btnCancelConfig_rect = (margenIzq+20, window_height-50, anchoBoton, altoBoton)
btnCancelConfig = Button(btnCancelConfig_rect, goto_inicio, "Cancelar")
btnCancelConfig.screens = ("configurar",)

btnAceptarConfig_rect = (window_width-anchoBoton-margenIzq-20, window_height-50,anchoBoton,altoBoton)
btnAceptarConfig = Button(btnAceptarConfig_rect, goto_inicio, "Aceptar")
btnAceptarConfig.screens = ("configurar",)


###############################################
#             Pantalla Continuar              #
###############################################
    #  Titulo
lblTituloContinuar_rect = lblTituloConfig_rect
lblTituloContinuar = Label(lblTituloContinuar_rect, "Continuar")
lblTituloContinuar.screens = ("continuar",)
lblTituloContinuar.font = Font.Large

    #  Imagen e info
imgImagenContinuar_rect = (margenIzq, lblTituloContinuar_rect[1]+lblTituloContinuar_rect[3]+sepTit, window_width*0.5, window_height*0.4)
imgImagenContinuar = Image(imgImagenContinuar_rect, None)  # Reemplazar None por la imagen a mostrar
imgImagenContinuar.screens = ("continuar",)
imgImagenContinuar.lineWidth = 1

lblInfoContinuar_rect = (imgImagenContinuar_rect[0]+imgImagenContinuar_rect[2]+sep2, imgImagenContinuar_rect[1], window_width-2*margenIzq-sep2-imgImagenContinuar_rect[2], imgImagenContinuar_rect[3])
lblInfoContinuar = ControlBase(lblInfoContinuar_rect)  # Reemplazar el control por un label multilinea
lblInfoContinuar.screens = ("continuar",)

    #  Lista de partidas guardadas
lstGuardadosContinuar_rect = (margenIzq, imgImagenContinuar_rect[1]+imgImagenContinuar_rect[3]+sep2, imgImagenContinuar_rect[2], window_height-imgImagenContinuar_rect[1]-imgImagenContinuar_rect[3]-sep2-30 )
lstGuardadosContinuar = TextList(lstGuardadosContinuar_rect, [u"Martín", u"Sebastián", u"López", "Paglione", u"Acá van las", u"partidas guardadas", u"disponibles para continuar"]) 
lstGuardadosContinuar.align = None 
lstGuardadosContinuar.posText = 10 
lstGuardadosContinuar.lineWidth = 1
lstGuardadosContinuar.screens = ("continuar",)

    #  Botones

btnCargarContinuar_rect = (lblInfoContinuar_rect[0]+(lblInfoContinuar_rect[2]-anchoBoton)/2, lstGuardadosContinuar_rect[1]+(lstGuardadosContinuar_rect[3]-altoBoton*3-sep2*2)/2, anchoBoton, altoBoton )
btnBorrarContinuar_rect = (lblInfoContinuar_rect[0]+(lblInfoContinuar_rect[2]-anchoBoton)/2, btnCargarContinuar_rect[1]+btnCargarContinuar_rect[3]+sep2, anchoBoton, altoBoton)
btnAtrasContinuar_rect = (lblInfoContinuar_rect[0]+(lblInfoContinuar_rect[2]-anchoBoton)/2, btnBorrarContinuar_rect[1]+btnBorrarContinuar_rect[3]+sep2 ,anchoBoton, altoBoton)

btnCargarContinuar = Button(btnCargarContinuar_rect, goto_vprevia, "Cargar")
btnCargarContinuar.screens = ("continuar",)

btnBorrarContinuar = Button(btnBorrarContinuar_rect, goto_inicio, "Borrar")  #  Reemplazar la funcion goto_inicio por la correspondiente al borrado del elemento de la lista
btnBorrarContinuar.screens = ("continuar",)

btnAtrasContinuar = Button(btnAtrasContinuar_rect, goto_inicio, "Atras")
btnAtrasContinuar.screens = ("continuar",)







###############################################
#          Pantalla Nuevo laberinto           #
###############################################


    #  Botones

btnCargarNuevo_rect = (lblInfoContinuar_rect[0]+(lblInfoContinuar_rect[2]-anchoBoton)/2, lstGuardadosContinuar_rect[1]+(lstGuardadosContinuar_rect[3]-altoBoton*3-sep2*2)/2, anchoBoton, altoBoton )
btnSiguienteNuevo_rect = (lblInfoContinuar_rect[0]+(lblInfoContinuar_rect[2]-anchoBoton)/2, btnCargarContinuar_rect[1]+btnCargarContinuar_rect[3]+sep2, anchoBoton, altoBoton)
btnAtrasNuevo_rect = (lblInfoContinuar_rect[0]+(lblInfoContinuar_rect[2]-anchoBoton)/2, btnBorrarContinuar_rect[1]+btnBorrarContinuar_rect[3]+sep2 ,anchoBoton, altoBoton)

btnCargarNuevo = Button(btnCargarNuevo_rect, goto_plantillas, "Cargar plantilla")
btnCargarNuevo.screens = ("nuevo",)

btnBorrarNuevo = Button(btnSiguienteNuevo_rect, goto_vprevia, "Siguiente")  #  Reemplazar la funcion goto_inicio por la correspondiente al borrado del elemento de la lista
btnBorrarNuevo.screens = ("nuevo",)

btnAtrasNuevo = Button(btnAtrasNuevo_rect, goto_inicio, "Atras")
btnAtrasNuevo.screens = ("nuevo",)



###############################################
#           Pantalla de plantillas            #
###############################################
    #  Titulo
lblTituloPlantillas_rect = lblTituloConfig_rect
lblTituloPlantillas = Label(lblTituloPlantillas_rect, "Plantillas")
lblTituloPlantillas.screens = ("plantillas",)
lblTituloPlantillas.font = Font.Large

    #  Imagen e info
imgImagenPlantillas_rect = (margenIzq, lblTituloPlantillas_rect[1]+lblTituloPlantillas_rect[3]+sepTit, window_width*0.5, window_height*0.4)
imgImagenPlantillas = Image(imgImagenPlantillas_rect, None)  # Reemplazar None por la imagen a mostrar
imgImagenPlantillas.screens = ("plantillas",)
imgImagenPlantillas.lineWidth = 1

lblInfoPlantillas_rect = (imgImagenPlantillas_rect[0]+imgImagenPlantillas_rect[2]+sep2, imgImagenPlantillas_rect[1], window_width-2*margenIzq-sep2-imgImagenPlantillas_rect[2], imgImagenPlantillas_rect[3])
lblInfoPlantillas = ControlBase(lblInfoPlantillas_rect)  # Reemplazar el control por un label multilinea
lblInfoPlantillas.screens = ("plantillas",)

    #  Lista de plantillas guardadas
lstGuardadosPlantillas_rect = (margenIzq, imgImagenPlantillas_rect[1]+imgImagenPlantillas_rect[3]+sep2, imgImagenPlantillas_rect[2], window_height-imgImagenPlantillas_rect[1]-imgImagenPlantillas_rect[3]-sep2-30 )
lstGuardadosPlantillas = TextList(lstGuardadosPlantillas_rect, [u"Esta es la", u"lista de plantillas", u"disponible para usar"]) 
lstGuardadosPlantillas.lineWidth = 1
lstGuardadosPlantillas.screens = ("plantillas",)

    #  Botones

btnCargarPlantillas_rect = (lblInfoPlantillas_rect[0]+(lblInfoPlantillas_rect[2]-anchoBoton)/2, lstGuardadosPlantillas_rect[1]+(lstGuardadosPlantillas_rect[3]-altoBoton*3-sep2*2)/2, anchoBoton, altoBoton )
btnAtrasPlantillas_rect = (lblInfoPlantillas_rect[0]+(lblInfoPlantillas_rect[2]-anchoBoton)/2, btnCargarPlantillas_rect[1]+btnCargarPlantillas_rect[3]+sep2 ,anchoBoton, altoBoton)

btnCargarPlantillas = Button(btnCargarPlantillas_rect, goto_nuevo, "Cargar")
btnCargarPlantillas.screens = ("plantillas",)


btnAtrasPlantillas = Button(btnAtrasPlantillas_rect, goto_inicio, "Atras")
btnAtrasPlantillas.screens = ("plantillas",)




###############################################
#           Pantalla vista previa             #
###############################################
    #  Nombre del laberinto
lblNombreVprevia_rect = lblTituloConfig_rect
lblNombreVprevia = Label(lblNombreVprevia_rect, "Nombre del laberinto")
lblNombreVprevia.screens = ("vprevia",)
lblNombreVprevia.font = Font.Large

    #  Imagen de la vista previa
imgImagenVprevia_rect = (window_width*0.15, lblNombreVprevia_rect[1]+lblNombreVprevia_rect[3]+sepTit, window_width*0.7, window_height*0.7)
imgImagenVprevia = Image(imgImagenVprevia_rect, None)  # Reemplazar None por la imagen a mostrar
imgImagenVprevia.screens = ("vprevia",)
imgImagenVprevia.lineWidth = 1

    #  Botones 
btnCancelVprevia_rect = (margenIzq+20, window_height-50, anchoBoton, altoBoton)
btnCancelVprevia = Button(btnCancelVprevia_rect, goto_pantAnterior, "Cancelar")
btnCancelVprevia.screens = ("vprevia",)

btnAceptarConfig_rect = (window_width-anchoBoton-margenIzq-20, window_height-50,anchoBoton,altoBoton)
btnAceptarConfig = Button(btnAceptarConfig_rect, goto_juego, "A jugar!")
btnAceptarConfig.screens = ("vprevia",)

###############################################
#           Pantalla menu de pausa            #
###############################################

    #  Titulo
lblTituloPausa_rect = lblTituloConfig_rect
lblTituloPausa = Label(lblTituloPausa_rect, "PAUSA")
lblTituloPausa.font = Font.Large
lblTituloPausa.screens = ("pausa",)

    #  Botones (primeros 3)
btnReanudarPausa_rect = ((window_width-anchoBoton)/2, lblTituloPausa_rect[1] + lblTituloPausa_rect[3] + 3*sepTit,  anchoBoton,  altoBoton)
btnReanudarPausa = Button(btnReanudarPausa_rect, goto_juego, "Reanudar")
btnReanudarPausa.screens = ("pausa",)

btnReiniciarPausa_rect = ((window_width-anchoBoton)/2, btnReanudarPausa_rect[1] + btnReanudarPausa_rect[3] + sep2,  anchoBoton,  altoBoton)
btnReiniciarPausa = Button(btnReiniciarPausa_rect, goto_vprevia, "Reiniciar")  #  Reemplazar con la funcion para reiniciar
btnReiniciarPausa.screens = ("pausa",)

btnSalirPausa_rect = ((window_width-anchoBoton)/2, btnReiniciarPausa_rect[1] + btnReiniciarPausa_rect[3] + sep2,  anchoBoton,  altoBoton)
btnSalirPausa = Button(btnSalirPausa_rect, goto_inicio, "Volver al menu inicial")
btnSalirPausa.screens = ("pausa",)

    #  Label y checkbox
lblMusicaPausa_rect = ((window_width-anchoBoton)/2, btnSalirPausa_rect[1] + btnSalirPausa_rect[3] + sep2, anchoBoton - 25 - sep2, altoBoton)
lblMusicaPausa = Label(lblMusicaPausa_rect, "Musica")
lblMusicaPausa.screens = ("pausa",)

chkMusicaPausa_rect = (lblMusicaPausa_rect[0]+lblMusicaPausa_rect[2]+sep2, btnSalirPausa_rect[1] + btnSalirPausa_rect[3] + sep2, 25,25)
chkMusicaPausa = CheckBox(chkMusicaPausa_rect, True)
chkMusicaPausa.screens = ("pausa",)

lblMinimapaPausa_rect = ((window_width-anchoBoton)/2, lblMusicaPausa_rect[1] + lblMusicaPausa_rect[3] + sep2, anchoBoton - 25 - sep2, altoBoton)
lblMinimapaPausa = Label(lblMinimapaPausa_rect, "Minimapa")
lblMinimapaPausa.screens = ("pausa",)

chkMinimapaPausa_rect = (lblMinimapaPausa_rect[0]+lblMinimapaPausa_rect[2]+sep2, lblMusicaPausa_rect[1] + lblMusicaPausa_rect[3] + sep2, 25,25)
chkMinimapaPausa = CheckBox(chkMinimapaPausa_rect, True)
chkMinimapaPausa.screens = ("pausa",)

    #  Botones (ultimos 3)
btnCaptVistaPausa_rect = ((window_width-anchoBoton)/2, lblMinimapaPausa_rect[1] + lblMinimapaPausa_rect[3] + sep2,  anchoBoton,  altoBoton)
btnCaptVistaPausa = Button(btnCaptVistaPausa_rect, goto_inicio, "Capturar vista")   #  Reemplazar con la funcion de captura correspondiente  
btnCaptVistaPausa.screens = ("pausa",)

btnCaptLabPausa_rect = ((window_width-anchoBoton)/2, btnCaptVistaPausa_rect[1] + btnCaptVistaPausa_rect[3] + sep2,  anchoBoton,  altoBoton)
btnCaptLabPausa = Button(btnCaptLabPausa_rect, goto_inicio, "Capturar laberinto")   #  Reemplazar con la funcion de captura correspondiente
btnCaptLabPausa.screens = ("pausa",)

btnGuardarPausa_rect = ((window_width-anchoBoton)/2, btnCaptLabPausa_rect[1] + btnCaptLabPausa_rect[3] + sep2,  anchoBoton,  altoBoton)
btnGuardarPausa = Button(btnGuardarPausa_rect, goto_juego, "Guardar")    #  Reemplazar con la funcion de guardado
btnGuardarPausa.screens = ("pausa",)

###############################################
#             Pantalla de guardar             #
###############################################


###############################################
#              Pantalla de juego              #
###############################################

#  ESTE BOTON NO DEBE EXISTIR. ES SOLO PARA PROBAR LA PAUSA
btnPausaJuego_rect = (400, 400,  anchoBoton,  altoBoton)
btnPausaJuego = Button(btnPausaJuego_rect, goto_pausa, "Pausa")    
btnPausaJuego.screens = ("juego",)

###############################################
#          Pantalla de fin de juego           #
###############################################




#########################################################################
#########################################################################
##                                                                     ##
##                   FIN DE PANTALLAS DEL JUEGO                        ##
##                                                                     ##
#########################################################################
#########################################################################


    #  Genero todos los graficos de los controles
for c in ControlBase.All:
    c.updateGraphics()






Context.isRunning = True

while Context.isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Context.isRunning = False

        if event.type == pygame.KEYDOWN:
            #print event.key, event.unicode, event.mod
            if ControlBase.OnFocus != None:
                ControlBase.OnFocus.keydown(event)
            else:
            # Volver al menu
                if event.key == pygame.K_m:
                    Context.screen = "inicio"
                elif event.key == pygame.K_c:
                     Context.screen = "configurar"

            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.key == pygame.K_ESCAPE:
                Context.isRunning = False


        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle left button click events
            for ctl in ControlBase.All:
                if ctl.click(event):
                    break
        


    # Process menu
    window.fill(Color.Fog)
    
    for c in ControlBase.All:
    	c.render(window)



    show_fps()



    
    pygame.display.update()

    clock.tick()
    count_fps()




pygame.quit()
sys.exit()