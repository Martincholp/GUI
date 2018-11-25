#! /usr/bin/env python
#-*- coding: UTF-8 -*-

import pygame, sys
from mtn_GUI import *
from UltraColor import *

pygame.init()

# Variables globales
FPS = 0
fps_font = pygame.font.Font("recursos/paris.fon", 20)
clock = pygame.time.Clock()
#_pantalla = "menu"
deltatime = 1
tag = ''

Context.screen = 'menu'



def show_info():
    fps_overlay = fps_font.render(str(FPS), True, Color.Goldenrod)
    pantallaActiva = fps_font.render(Context.screen, True, Color.Goldenrod)
    Tag = fps_font.render(tag, True, Color.Goldenrod)
    altura_linea = fps_font.get_linesize() +10
    window.blit(fps_overlay, (0, 0))
    window.blit(pantallaActiva, (0, altura_linea))
    window.blit(Tag, (0, 2*altura_linea))
    window.blit(fps_font.render(str(pygame.mouse.get_pos()), True, Color.Goldenrod), (0, 3*altura_linea))


def create_window():
    global window, window_height, window_width, window_title
    window_width, window_height =  (800, 800 *9/16) #  (mantiene una relacion 16:9)
                                            # 1366, 768 (resolucion de maquina HP)
    window_title = "Prueba GUI v" + str(InfoVersion())
    pygame.display.set_caption(window_title)
    pygame.display.set_icon(pygame.image.load('recursos/logo-gui-32x32.png'))
    window = pygame.display.set_mode((window_width, window_height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
    window_width, window_height = window.get_size()


def count_fps():
    global FPS, clock

    FPS = clock.get_fps()
    if FPS > 0:
        deltatime = 1 / FPS

def accionClick(boton):
    #global pantalla

    if Context.screen == "menu":
        Context.screen = "config"
    elif Context.screen == "config":
        Context.screen = "menu"
        
    #print "BOTON " + str(boton)


create_window()

# INICIALIZO GUI

# r1 = (200,175,250,25)
# r2 = (200,200,250,25)
# r3 = (200,225,250,25)
# r4 = (200,275,250,100)

# cb4 = Button(r4, accionClick, "DESHABILITADO")
# cb4.screens = ("menu", "config")
# cb4.align = None #"Bottom"
# cb4.pos_text = (20,20)
# cb4.enable = False

# r_check = (150,100,25,25)
# check = CheckBox(r_check)
# check.screens = ('menu',)


# rect_RollList = (200,200,250,50)
# rll=RollList(rect_RollList, (u"Martín",u"Sebastián", u"López", u"Paglione"))
# rll.color_background=Color.Silver
# rll.screens = ('menu',)
# rll.color_backgroundBoton = Color.Blood
# rll.align = None
# rll.pos_text = (4, 15)

# rect_RollList2 = (200,100,250,50)
# rll2=RollList(rect_RollList2, (u"Martín", u"Sebastian", u"López", u"Paglione"))
# rll2.color_background=Color.Silver
# rll2.screens = ('menu',)
# rll2.color_backgroundBoton = Color.Blood
# rll2.align = A_RIGHT

rect_lista = (100,100,400,300)
#lst = TextList(rect_lista, [u"1 Martín", u"2 Sebastián",u"3 López",u"4 Paglione"])
#lst = TextList(rect_lista, [u"1 Martín", u"2 Sebastián",u"3 López",u"4 Paglione", u"5 Martín",u"6 Sebastán",u"7 López",u"8 Paglione",u"9 Martín",u"10 Sebastán",u"11 López",u"12 Paglione",u"13 Martín",u"14 Sebastán",u"15 López",u"16 Paglione",u"17 Martín",u"18 Sebastán",u"19 López",u"20 Paglione"])
lst = TextList(rect_lista, [u"1 Martín", u"Esto es una frase enorme para ver si el rectangulo se corta bien",u"2 Sebastián",u"3 López",u"4 Paglione", u"5 Martín",u"6 Sebastán",u"7 López",u"8 Paglione",u"9 Martín",u"10 Sebastán",u"11 López",u"12 Paglione",u"13 Martín",u"14 Sebastán",u"15 López",u"16 Paglione",u"17 Martín",u"18 Sebastán",u"19 López",u"20 Paglione"])
lst.screens = ('menu',)
lst.align = A_CENTER
lst.color_background = Color.DarkSlateGray
lst.color_foreground = Color.Khaki
lst.linesize_border = 10
lst.border = False
lst.color_normal = Color.Maroon
#lst.posText = 30
#lst.separator = 10
#lst.updateGraphics()


rect_sliderV = (500,100,25,300) #window_width-20,25)
sldV = Slider(rect_sliderV)
sldV.screens = ('menu',)
#sldV.enable = True
sldV.orientation = O_VERTICAL
sldV.minValue = 0
sldV.maxValue = (len(lst.itemList)*(lst.separator + lst.font.get_linesize())) - lst.get_height() + 2*lst.linesize_border
sldV.value = sldV.maxValue
#sldV.visible = True


anchura=0
for i in lst.itemList:
    ancho, alto = lst.font.size(i)
    if ancho>anchura:
        anchura=ancho

rect_sliderH = (100,400,400,25) #window_width-20,25)
sldH = Slider(rect_sliderH)
sldH.screens = ('menu',)
#sldH.enable = False
sldH.minValue = 0
sldH.maxValue = anchura - lst.get_width() + 2*lst.linesize_border
sldH.value = sldH.maxValue/2
#sldH.visible = False


# Creo una muestra de colores
anchoColor = 5
#muestra = pygame.Surface((148*anchoColor, 60))
cols=[]
for i in range(148):
    col=ControlBase((i*anchoColor-15,100,anchoColor,60 ))
    col.color_background = Color.colores[i]
    col.tag = Color.str_colores[i]
    col.screens = ('colores',)
    col.border = False
    cols.append(col)





    #pygame.draw.line(muestra, Color.colDict[i], (i*anchoColor,0),(i*anchoColor,60), anchoColor)

#muestra_rect = muestra.get_rect(topleft = (50, 150))
#imgMuestra = Image(muestra_rect, muestra)
#imgMuestra.screens = ("colores",)


for c in ControlBase.All:
    c.updateGraphics()
 
Context.isRunning = True

while Context.isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Context.isRunning = False

        if event.type == pygame.KEYDOWN:
            
            # Volver al menu
            if event.key == pygame.K_ESCAPE:
                Context.isRunning = False
            elif event.key == pygame.K_m:
                Context.screen = "menu"
            elif event.key == pygame.K_c:
                Context.screen = "colores"
            elif event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle left button click events
            # for btn in Button.All:
            #     btn.click(event.button, pantalla)

            # for chk in CheckBox.All:
            #     chk.click(event.button, pantalla)

            for ctl in ControlBase.All:
                ctl.click(event.button)
        

        elif event.type == pygame.MOUSEMOTION:
            for ctl in ControlBase.All:
                if ctl.is_hover():
                    #print ctl, ctl.is_hover()
                    tag = ctl.tag
                    break
                else:
                    tag = ""
        #             if lbl.is_hover():  #btn.Tag[0] == Globals.scene and btn.Rolling:
        #                 if btn.CommandDown != None:
        #                     btn.MouseDown() #Globals.scene) # Do button event

        #                 #btn.Rolling = False
        #                 break # Exit loop

        #         for chk in Menu.Checkbox.All:
        #             if chk.Rolling:
        #                 chk.Click()
        #                 break

        #         for txl in Menu.Textlist.All:
        #             if txl.Rolling:
        #                 txl.Click()

        # elif event.type == pygame.MOUSEBUTTONUP:
        #     if event.button == 1:  #Left click
        #         # Handle left button click events
        #         for btn in Menu.Button.All:
        #             if btn.CommandUp != None:
        #                 btn.MouseUp() # Do button event
        #             break # Exit loop



    # Process menu
    window.fill(Color.Fog)

    if Context.screen=="colores" and tag != '':
            pygame.draw.rect(window,Color.colDict[tag],pygame.Rect(0,200, window_width, 250),0)

    #rll2.enable = check.value


    # Proceso actividad del usuario
    lst.PosY = sldV.maxValue - sldV.value
    lst.PosX = sldH.value #sldH.maxValue - sldH.value

    #print lst.posX, lst.posY
    
    for c in ControlBase.All:
    	#c.update(pantalla)
    	c.render(window)

    #print sld.value, sld.cursorPos


    show_info()
    
    pygame.display.update()

    clock.tick()
    count_fps()


pygame.quit()
sys.exit()