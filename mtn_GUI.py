#! /usr/bin/env python
#-*- coding: UTF-8 -*-
import pygame
from UltraColor import *
from constants import *

'''
mtnGUI
Es un modulo para crear interfaces de usuario graficas usando solo pygame como libreria dependiente.
version 0.0.1
por Martin Lopez Paglione
'''

pygame.init()

class Context(object):
    '''Objeto utilizado para contener parametros globales, con los cuales tambien interactua el modulo'''
    screen = None
    prevScreen = None
    isRunning = False


class Font(object):
    '''Clase que agrupa algunos tamanos y fuentes para facilitar su uso en el modulo'''

    Default = pygame.font.SysFont("Verdana", 20)
    Small = pygame.font.SysFont("Verdana", 15)
    Medium = pygame.font.SysFont("Verdana", 40)
    Large = pygame.font.SysFont("Verdana", 60)
    Scanner = pygame.font.SysFont("Verdana", 30)

    def set_fontsize(self,v):
        return pygame.font.SysFont("Verdana", v)


class ControlBase(pygame.Surface):
    '''Clase base para derivar los controles'''
    All = []
    OnFocus = None

    def __init__(self, rect):
        '''Inicializador del control. El parametro rect contiene el rectángulo que define la posicion y tamaño del control'''

        #pygame.Surface.__init__(self, (rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)
    	super(ControlBase, self).__init__((rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)
        self.screens = ()    #  Tupla con los nombres de los contextos en donde debe formar parte el control. Si esta vacia siempre forma parte
        self.visible = True  #  Indica si es visible o no el control en la pantalla (puede formar parte, pero no necesariamente dibujarse)
        self.enableFocus = True  #  Indica si el control puede obtener el foco
        self.enable = True   #  Indica si el control esta habilitado
        self.tag = None #  Para guardar cualquier cosa que sea necesario
        self._border = True  #  Establece si se mostrará el borde del control. (propiedad border)

        #  Superficies que componen el control
        self.img_foreground = pygame.Surface((rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_foreground_h = pygame.Surface((rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_normal = pygame.Surface((rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_hover = pygame.Surface((rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_down = pygame.Surface((rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_disable = pygame.Surface((rect[2], rect[3]), pygame.HWSURFACE|pygame.SRCALPHA)
           #  Limpio las superficies
        self.img_foreground.fill(Color.Transparent)
        self.img_foreground_h.fill(Color.Transparent)
        self.img_normal.fill(Color.Transparent)
        self.img_hover.fill(Color.Transparent)
        self.img_down.fill(Color.Transparent)
        self.img_disable.fill(Color.Transparent)
        


        #  Colores
        self.color_background = Color.Transparent
        self.color_foreground = Color.DarkSeaGreen
        self.color_foreground_h = Color.LawnGreen
        self.color_normal = Color.Gainsboro
        self.color_hover = Color.White
        self.color_down = Color.Silver
        self.color_disable = Color.Gray
        self.color_focus = Color.Red



        #  Lineas
        self._linesize_border = 4
        self.linesize_foreground = 2
        self.linesize_focus = 1


        #  Atributos privados        
        self._pos = (rect[0], rect[1])  #  Posicion del control. Ver funciones get_pos() y set_pos()
        self._GraphicMode = 0    #  Indica el modo grafico a utilizar. Si es 0 se dibujan los controles, si es 1 se utiliza una imagen provista


        ControlBase.All.append(self)

    @property
    def linesize_border(self):
        '''Estblece el espesor del borde del control. Hacer cero este valor es equivalente a X.border = False'''
        if self._border:
            return self._linesize_border / 2
        else:
            return 0

    @linesize_border.setter
    def linesize_border(self, val):
        if val:
            self._linesize_border = val * 2
        else:
            self.border = False


    @property
    def border(self):
        '''Estblece si se mostrará el borde del control'''
        return self._border
    
    @border.setter
    def border(self, val):
        self._border = val
        #self.updateGraphics()

    @property
    def left(self):
        '''Posicion del borde izquierdo. Solo lectura'''
        return self._pos[0]

    @property
    def top(self):
        '''Posicion del borde superior. Solo lectura'''
        return self._pos[1]

    @property
    def width(self):
        '''Ancho del control. Solo lectura'''
        return self.get_width()
    
    @property
    def height(self):
        '''Alto del control. Solo lectura'''
        return self.get_height()    

    def get_pos(self):
        '''Devuelve la posicion del control en una tupla'''
        return self._pos

    def set_pos(self, p):
        '''Recibe una tupla con las coordenadas X e Y para asignarlas al control'''
        self._pos = p

    def get_rect(self):
        '''Obtiene el rectángulo del control.'''
        return super(ControlBase, self).get_rect(topleft=self.get_pos())

    def set_GraphicMode(self, gm):
        '''Establece el modo gráfico a utilizar. (0=dibujado, 1=imágenes)'''
        self._GraphicMode = gm

    def get_GraphicMode(self):
        '''Devuelve el modo gráfico utilizado. (0=dibujado, 1=imágenes)'''
        return self._GraphicMode

    def is_context(self):
        '''Devuelve True si el contexto actual es válido para el control'''

        screen = Context.screen

        if len(self.screens)==0 or screen==None or screen in self.screens:
            return True
        else:
            return False

    def is_hover(self):
        '''Devuelve un valor mayor que cero si el mouse está sobre el control.
        Si el mouse está fuera del control devuelve cero.'''
        
        if self.visible and self.is_context():
            return int(self.get_rect().collidepoint(pygame.mouse.get_pos()))
            

    def is_down(self, b=None):
        '''Devuelve True si está pulsado el botón del mouse indicado en b.
        Si b=None devuelve True ante la pulsación de cualquier botón'''

        if self.visible and self.is_context():

            btns = pygame.mouse.get_pressed()

            if b==None:
                return (btns[0] or btns[1] or btns[2])
            else:
                return btns[b-1]

    @property
    def is_Focus(self):
        '''Devuelve True si el control tiene el foco. Solo lectura. '''
        enfocada = ControlBase.OnFocus == self
        if enfocada:
            return True
        else:
            return False

    def render(self, target, b=None):
        '''Dibuja el control en la superficie indicada en target.'''

        esta_visible = self.visible
        esta_encontexto = self.is_context()
        esta_activado = self.enable
        esta_encima = self.is_hover()
        esta_enfoco = self.is_Focus


        if esta_visible and esta_encontexto:
            if not esta_activado:
                target.blit(self.img_disable, self.get_pos())
                target.blit(self.img_foreground, self.get_pos())
            else:
                if esta_encima:
                    if self.is_down(b):
                        target.blit(self.img_down, self.get_pos())
                    else:
                        target.blit(self.img_hover, self.get_pos())
                    target.blit(self.img_foreground_h, self.get_pos())
                else:
                    target.blit(self.img_normal, self.get_pos())

                    target.blit(self.img_foreground, self.get_pos())

            if esta_enfoco: #and esta_encontexto:

                pygame.draw.rect(target, Color.Red, (self.left, self.top ,self.get_width(),self.get_height()), self.linesize_focus)

            return True
        else:
            return False

    def updateGraphics(self):
        '''Actualiza como se mostrará el control según el modo gráfico establecido. Debe ser llamado cada vez que la imagen del control cambie'''

        ##### IMPORTANTE: Esta funcion debe extenderse en todas las clases derivadas       

        # Limpio las superficies del control
        self.img_normal.fill(self.color_background)  
        self.img_hover.fill(self.color_background)  
        self.img_down.fill(self.color_background)  
        self.img_disable.fill(self.color_background)  



        if self.get_GraphicMode() == 0:
            # Dibuja el borde del control

            if self.border:
                  # Normal
                pygame.draw.rect(self.img_normal, self.color_normal, (0,0,self.get_width(),self.get_height()), self._linesize_border)
                  # Hover
                pygame.draw.rect(self.img_hover, self.color_hover, (0,0,self.get_width(),self.get_height()),self._linesize_border)
                  # Down
                pygame.draw.rect(self.img_down, self.color_down, (0,0,self.get_width(),self.get_height()),self._linesize_border)
                  # Disable
                pygame.draw.rect(self.img_disable, self.color_disable, (0,0,self.get_width(),self.get_height()),self._linesize_border)

            for l in range(0, self.get_width(), 10):
                pygame.draw.line(self.img_disable, self.color_disable, (l, self.get_height()),(l+10, 0) )

        else:
            print 'El modo grafico ' + self.get_GraphicMode() + ' no existe'

    
    def click(self, boton=None):
        '''Método a llamar cuando se hace click. Devuelve 1 si está encima del control, de lo contrario devuelve 0'''

        ##### IMPORTANTE: Esta funcion debe sobreescribirse en todas las clases derivadas que requieran controlar el click       

        esta_encima = self.is_hover()
                   
        if esta_encima:
            if self.enable:
                if self.enableFocus:
                    ControlBase.OnFocus = self
            
        else:
            ControlBase.OnFocus = None
            
        return esta_encima

    def keydown(self, k=None):
        '''Método a llamar cuando se presiona una tecla. El parámetro k es la tecla que se ha presionado'''

        if self.is_hover() and self.enable and self.is_Focus:
            return True
        else:
            return False


    ###########################################
    ##         METODOS ESPECIALES            ##
    ###########################################
    def __repr__(self):
        # Devuelve un str con el tipo de control y el rectangulo que ocupa
        return (str(type(self)).split('.')[1])[:-2] + str(self.get_rect())[5:-1]
