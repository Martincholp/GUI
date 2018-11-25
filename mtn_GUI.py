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

class Label(ControlBase):
    '''Control para mostrar un texto sin interacción con el usuario'''
    All = []
    def __init__(self, rect, texto):
        super(Label, self).__init__(rect)
        self._text = texto
        self.enableFocus = False

        # Configuracion del texto
        self.pos_text = (0,0)
        self.font = Font.Default
        self.align = A_CENTER

        #  Colores
        self.color_background = Color.Transparent
        self.color_foreground = Color.DarkSeaGreen
        self.color_disable = Color.Gray
            #  Como es un label se supone que no interactua con el usuario, por eso
            #  los colores normal, hover y down son igual al background. Ademas el
            #  color del foreground y del foreground_h tambien son iguales
        self.color_normal = self.color_background
        self.color_hover = self.color_background
        self.color_down = self.color_background
        self.color_foreground_h = self.color_foreground



        Label.All.append(self)

    @property
    def text(self):
        '''Texto del Label'''
        return self._text

    @text.setter
    def text(self, texto):
        
        self._text = texto

        # Construye el bitmap de texto correspondiente y lo coloca en el foreground
        bitmap = self.font.render(texto, True, self.color_foreground)
        bitmap_h = self.font.render(texto, True, self.color_foreground_h)
        bitmap_disable = self.font.render(texto, True, self.color_disable)
        bitmapWidth, bitmapHeight = self.font.size(texto) 

        # Calculo la posicion
            # Valor del usuario
        if self.align == None:
            posX, posY = self.pos_text
        
            # Posicion X
        if self.align == A_LEFT or self.align == A_TOPLEFT or self.align == A_BOTTOMLEFT:
            posX = 0
        
        if self.align == A_CENTER or self.align == A_TOP or self.align == A_BOTTOM:
            posX = self.get_width()/2 - bitmapWidth/2

        if self.align == A_RIGHT or self.align == A_BOTTOMRIGHT or self.align == A_TOPRIGHT:
            posX = self.get_width() - bitmapWidth 

            # Posicion Y
        if self.align == A_TOPLEFT or self.align == A_TOP or self.align == A_TOPRIGHT:
            posY = 0
        
        if self.align == A_CENTER or self.align == A_LEFT or self.align == A_RIGHT:
            posY = self.get_height()/2 - bitmapHeight/2

        if self.align == A_BOTTOMLEFT or self.align == A_BOTTOMRIGHT or self.align == A_BOTTOM:
            posY = self.get_height() - bitmapHeight

        # Dibujo el texto sobre la img_foreground (normal y hover)
        self.img_foreground.fill(Color.Transparent)
        self.img_foreground.blit(bitmap, (posX, posY))
        self.img_foreground_h.fill(Color.Transparent)
        self.img_foreground_h.blit(bitmap_h, (posX, posY))
        self.img_disable.blit(bitmap_disable, (posX, posY))

    def updateGraphics(self):
        '''Actualiza como se mostrara nuestro control segun el modo grafico establecido'''

        super(Label, self).updateGraphics()
        self.text = self._text  # Solo para ctualizar el bitmap de texto 



class Image(ControlBase):
    '''Contenedor para mostrar una imagen'''

    All = []
    def __init__(self, rect, imagen=None):
        super(Image, self).__init__(rect)
        self.imagen = imagen
        self.border = True

        Image.All.append(self)


    def updateGraphics(self):
        '''Actualiza como se mostrara nuestro control segun el modo grafico establecido'''


        # Limpio las superficies del control
        self.img_normal.fill(self.color_background)  
        self.img_hover.fill(self.color_background)  
        self.img_down.fill(self.color_background)  
        self.img_disable.fill(self.color_background)  

        if self.imagen == None:
            self.imagen = pygame.Surface(self.get_size(), pygame.HWSURFACE|pygame.SRCALPHA)
            self.imagen.fill(Color.Transparent)


        if self.border:
            pygame.draw.rect(self.imagen, self.color_foreground, (0,0,self.get_width(),self.get_height()), self.linesize_border)

        if self.get_GraphicMode() == 0:
            # Como solo es para mostrar una imagen todas las superficies del control tendran la imagen en cuestion
              # Normal
            self.img_normal.blit(self.imagen, (0,0))
              # Hover
            self.img_hover.blit(self.imagen, (0,0))
              # Down
            self.img_down.blit(self.imagen, (0,0))
              # Disable
            self.img_disable.blit(self.imagen, (0,0))
            for l in range(0, self.get_width(), 10):
                pygame.draw.rect(self.img_disable, self.color_disable, (0,0,self.get_width(),self.get_height()), self.linesize_foreground)
                pygame.draw.line(self.img_disable, self.color_disable, (l, self.get_height()),(l+10, 0), self.linesize_foreground )

        else:
            print 'El modo grafico ' + self.get_GraphicMode() + ' no existe'


class Button(Label):
    '''Boton para interaccion con el usuario'''
    All = []
    
    def __init__(self, rect, command, texto=""):
        super(Button, self).__init__(rect,texto)
        self.command = command
        self.enableFocus = True

        #  Colores
        self.color_background = Color.Transparent
        self.color_foreground = Color.DarkSeaGreen
        self.color_foreground_h = Color.LawnGreen
        self.color_normal = Color.Gainsboro
        self.color_hover = Color.White
        self.color_down = Color.Silver
        self.color_disable = Color.Gray
        

        Button.All.append(self)

    def click(self, boton=None):

        es_click = super(Button, self).click(boton)
        if es_click:
            self.command(boton)
        
        return es_click


class CheckBox(ControlBase):
    '''Caja de verificacion'''
    All = []

    def __init__(self, rect, value=False):
        super(CheckBox, self).__init__(rect)
        
        self._value = value

        CheckBox.All.append(self)


    def updateGraphics(self):
        '''Actualiza como se mostrara nuestro control segun el modo grafico establecido'''

        # Dibujo los bords con la llamada a la funcion de la clase base
        super(CheckBox, self).updateGraphics()

        # Dibujo el check
          # Puntos
        self._p1 = (self.get_width()*0.2, self.get_height()*0.5)
        self._p2 = (self.get_width()*0.4, self.get_height()*0.8)
        self._p3 = (self.get_width()*0.8, self.get_height()*0.25)

          # Imagen normal
        pygame.draw.line(self.img_foreground, self.color_foreground, self._p1, self._p2, self.linesize_foreground/2)
        pygame.draw.line(self.img_foreground, self.color_foreground, self._p2, self._p3, self.linesize_foreground/2)

          # Imagen hover
        pygame.draw.line(self.img_foreground_h, self.color_foreground_h, self._p1, self._p2, self.linesize_foreground/2)
        pygame.draw.line(self.img_foreground_h, self.color_foreground_h, self._p2, self._p3, self.linesize_foreground/2)
    
        self.value = self._value # Esto es solo para que dibuje la imagen disable

    @property
    def value(self):
        '''Propiedad para establecer el estado del check'''
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

        # Como no hay un foreground_disable actualizo el img_disable segun el valor del check
        self.img_disable.fill(self.color_background)

        for l in range(0, self.get_width(), 10):
            pygame.draw.rect(self.img_disable, self.color_disable, (0,0,self.get_width(),self.get_height()),self.linesize_foreground)
            pygame.draw.line(self.img_disable, self.color_disable, (l, self.get_height()),(l+10, 0) )

        # Imagen disable
        if val:
            pygame.draw.line(self.img_disable, self.color_disable, self._p1, self._p2, self.linesize_foreground/2)
            pygame.draw.line(self.img_disable, self.color_disable, self._p2, self._p3, self.linesize_foreground/2)


    def render(self, target, b=None):
        '''Dibujar nuestro control en la superficie indicada.'''
        
        if self.visible and self.is_context():
            if not self.enable:
                target.blit(self.img_disable, self.get_pos())
            else:
                
                if self.is_hover():
                    if self.value:
                        target.blit(self.img_hover, self.get_pos())
                        target.blit(self.img_foreground_h, self.get_pos())
                    else:
                        target.blit(self.img_hover, self.get_pos())
                else:
                    if self.value:
                        target.blit(self.img_normal, self.get_pos())
                        target.blit(self.img_foreground, self.get_pos())
                    else:
                        target.blit(self.img_normal, self.get_pos())
                
                if self.is_Focus:
                    pygame.draw.rect(target, Color.Red, (self.left, self.top ,self.get_width(),self.get_height()), self.linesize_focus)


    def click(self, boton=None):
        '''Cambia el valor del control'''
        es_click = super(CheckBox, self).click(boton)

        if es_click:
            self.value = not self._value 

        return es_click

class Textbox(Label): 
    '''Caja de texto'''
    All = []
    __tiempo = pygame.time.get_ticks() # Para usar en el parpadeo del cursor
    __parpadeo = True # Para usar en el parpadeo del cursor

    def __init__(self, rect, texto=""):

        super(Textbox, self).__init__(rect, texto)

        #  Vuelvo a la configuracion de colores del ControlBase y no del label
        self.color_background = Color.Transparent
        self.color_foreground = Color.DarkSeaGreen
        self.color_foreground_h = Color.LawnGreen
        self.color_normal = Color.Gainsboro
        self.color_hover = Color.White
        self.color_down = Color.Silver
        self.color_disable = Color.Gray
        self.color_cursor = self.color_foreground

        self.enableFocus = True
        self.cursorVisible = True
        self.cursorFreq = 300
        self.linesize_border = 1
        self._cursorPos = len(texto)
        self.pos_text = (5,0)

        pygame.key.set_repeat(400,100)

    @property
    def cursorPos(self):
        '''Define la posicion del cursor'''
        return self._cursorPos

    @cursorPos.setter
    def cursorPos(self, pos):
        self._cursorPos = pos
    

    def movCursorIzq(self):
        '''Mueve el cursos un caracter hacia la izquierda'''
        self._cursorPos -= 1
        if self._cursorPos < 0:
            self._cursorPos = 0

        return self.cursorPos


    def movCursorDer(self):
        '''Mueve el cursos un caracter hacia la derecha'''
        self._cursorPos += 1
        if self._cursorPos > len(self.text):
            self._cursorPos = len(self.text)

        return self.cursorPos

    def keydown(self, k=None):

        #esKeyDown = super(Textbox,self).keydown(k) 
        if self.enable and self.is_Focus:
            esKeyDown = True
        else:
            esKeyDown = False

        if esKeyDown:
            if k.key == pygame.K_LEFT:
                #nuevo = self.text
                self.movCursorIzq()

            elif k.key == pygame.K_RIGHT:
                #nuevo = self.text
                self.movCursorDer()


            elif k.key == pygame.K_BACKSPACE:
                self.text = self.text[:self.cursorPos][:-1] + self.text[self.cursorPos:]
                self.movCursorIzq()

            elif k.key == pygame.K_DELETE:
                self.text = self.text[:self.cursorPos] + self.text[self.cursorPos+1:]

            #elif k.key == pygame.K_RETURN:  # Para que no haga nada
            #    nuevo = self.text
            
            else:
                self.text = self.text[:self.cursorPos] + k.unicode + self.text[self.cursorPos:]
                self.movCursorDer()
            

        return esKeyDown

    def render(self, target, b=None):
        '''Redefinicion de la funcion render del Label para incluir el cursor con parpadeo'''


        dibCursor = super(Textbox, self).render(target, b)
        esta_activado = self.enable
        esta_enfoco = self.is_Focus

        tiemporTranscurrido = pygame.time.get_ticks() - Textbox.__tiempo
        if tiemporTranscurrido>self.cursorFreq:
            Textbox.__tiempo = pygame.time.get_ticks()
            Textbox.__parpadeo = not Textbox.__parpadeo

        if  dibCursor and esta_activado and esta_enfoco and Textbox.__parpadeo :
            anchoTexto, altoTexto = self.font.size(self.text[0:self.cursorPos])
            posXcur = self.left + self.pos_text[0] + anchoTexto
            if posXcur < self.left + self.img_normal.get_width():
                pygame.draw.line(target, self.color_foreground, (posXcur , self.top + self.pos_text[1]), (posXcur , self.top + self.pos_text[1]+ altoTexto) , 2)

        return dibCursor

    def click(self, c=None):  
        # c es el evento de MOUSEBUTTONDOWN 
        # c.pos -> posicion del click 
        # c.button -> boton del click (1 es el principal, 2 es secundario, 3 es central, 4 es rueda arriba, 5 es rueda abajo)
         
        #super(Textbox, self).click(c, screen)

        hover = super(Textbox, self).click(c) 
        
        if hover:
            posClick = c.pos

            if posClick[0] > self.left+self.pos_text[0]+self.font.size(self.text)[0]:
                self.cursorPos = len(self.text)
                return hover
            
            if posClick[0] < self.left+self.pos_text[0]:
                self.cursorPos = 0
                return hover

            else:
                tamizqant = 0

                for i in range(0,len(self.text)+1):
                    izq = self.text[0:i]
                    tamizq = self.font.size(izq)[0]
                    if posClick[0] > self.left + self.pos_text[0] + tamizqant+ (tamizq-tamizqant)/2:
                        tamizqant = tamizq
                    else:    
                        self.cursorPos = len(izq) -1
                        break    

        return hover


class RollList(ControlBase):
    '''Lista rotable'''
    All = []

    def __init__(self, rect, lista):

        super(RollList,self).__init__(rect)

        # Atributos propios del control
        self._lista = lista  #  Cada elemento puede contener 2-upla, donde elem[0] sera el nombre a mostrar y elem[1] el elemento a devolver 
        self._indice = 0
        self.loop = True # Si True, al final de la lista vuelve a empezar. Si False, se queda en el ultimo elemento
        
        # Configuracion del texto
        self.pos_text = (0,0)
        self.font = Font.Default
        self.align = A_CENTER

        # Posicion y tamaño de los botones
        self._boton_size = (30, rect[3]/2) # tamaño del boton por defecto. Para cambiarlo actuar sobre los rect
        self.rect_botonNext = pygame.Rect(rect[0]+rect[2]-self._boton_size[0], 0, self._boton_size[0], self._boton_size[1])
        self.rect_botonPrev = pygame.Rect(rect[0]+rect[2]-self._boton_size[0], self._boton_size[1], self._boton_size[0], self._boton_size[1])

        # Color de los botones
        self.color_backgroundBoton = Color.DimGray

        # Imagenes de este control
        # self.img_normal   Es la superficie normal (sin hover ni down). Heredada de ControlBase
        self.img_normalPrev = pygame.Surface(self.rect_botonPrev.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_hoverPrev = pygame.Surface(self.rect_botonPrev.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_downPrev = pygame.Surface(self.rect_botonPrev.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_normalNext = pygame.Surface(self.rect_botonNext.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_hoverNext = pygame.Surface(self.rect_botonNext.size, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_downNext = pygame.Surface(self.rect_botonNext.size, pygame.HWSURFACE|pygame.SRCALPHA)
        # self.img_disable   Es la superficie deshabilitada. Heredada de ControlBase


        RollList.All.append(self)

    def is_hover(self):
        '''Devuelve un entero mayor que cero cuando el cursor del mouse está sobre el control.
        Tabla de valores:
            0 --> No está sobre el control
            1 --> Está sobre el área de texto
            2 --> Está sobre el botón siguiente
            3 --> Está sobre el botón anterior'''


        if self.visible and self.is_context():
            pos = pygame.mouse.get_pos()  #  Posicion del mouse
            res = 0  #  Valor por defecto

            self.rect_botonNext.topright = self.get_rect().topright
            self.rect_botonPrev.bottomright = self.get_rect().bottomright
            if self.get_rect().collidepoint(pos):
                res = 1
            if self.rect_botonNext.collidepoint(pos):
                res = 2
            if self.rect_botonPrev.collidepoint(pos):
                res = 3

            return res

    @property
    def text(self):
        '''Devuelve el texto que esta seleccionado en la lista. Solo lectura.'''

        return self._lista[self._indice]
            


    def updateGraphics(self):
        '''Actualiza como se mostrara nuestro control segun el modo grafico establecido'''

        # Limpio las superficies del control
        self.img_normal.fill(self.color_background)  
        self.img_hover.fill(self.color_background)  
        self.img_down.fill(self.color_background)  
        self.img_disable.fill(self.color_background)  



        if self.get_GraphicMode() == 0:

            # boton previo
             # Estado normal
            self.img_normalPrev.fill(self.color_backgroundBoton)  
            pygame.draw.rect(self.img_normalPrev, self.color_normal, ((0,0),self.rect_botonPrev.size,), self.linesize_foreground)
            pygame.draw.line(self.img_normalPrev, self.color_normal, (0,0), (self._boton_size[0]/2,self._boton_size[1]), self.linesize_foreground)
            pygame.draw.line(self.img_normalPrev, self.color_normal, (self._boton_size[0]/2,self._boton_size[1]), (self._boton_size[0],0), self.linesize_foreground)
           
              # Estado hover
            self.img_hoverPrev.fill(self.color_backgroundBoton)
            pygame.draw.rect(self.img_hoverPrev, self.color_hover, ((0,0),self.rect_botonPrev.size), self.linesize_foreground)
            pygame.draw.line(self.img_hoverPrev, self.color_hover, (0,0), (self._boton_size[0]/2,self._boton_size[1]), self.linesize_foreground)
            pygame.draw.line(self.img_hoverPrev, self.color_hover, (self._boton_size[0]/2,self._boton_size[1]), (self._boton_size[0],0), self.linesize_foreground)
        
              # Estado down
            self.img_downPrev.fill(self.color_backgroundBoton)
            pygame.draw.rect(self.img_downPrev, self.color_down, ((0,0),self.rect_botonPrev.size), self.linesize_foreground)
            pygame.draw.line(self.img_downPrev, self.color_down, (0,0), (self._boton_size[0]/2,self._boton_size[1]), self.linesize_foreground)
            pygame.draw.line(self.img_downPrev, self.color_down, (self._boton_size[0]/2,self._boton_size[1]), (self._boton_size[0],0), self.linesize_foreground)
        
            # boton siguiente
             # Estado normal
            self.img_normalNext.fill(self.color_backgroundBoton)
            pygame.draw.rect(self.img_normalNext, self.color_normal, ((0,0),self.rect_botonNext.size), self.linesize_foreground)
            pygame.draw.line(self.img_normalNext, self.color_normal, (0,self._boton_size[1]), (self._boton_size[0]/2,0), self.linesize_foreground)
            pygame.draw.line(self.img_normalNext, self.color_normal, (self._boton_size[0]/2,0), (self._boton_size[0],self._boton_size[1]), self.linesize_foreground)
           
              # Estado hover
            self.img_hoverNext.fill(self.color_backgroundBoton)
            pygame.draw.rect(self.img_hoverNext, self.color_hover, ((0,0),self.rect_botonNext.size), self.linesize_foreground)
            pygame.draw.line(self.img_hoverNext, self.color_hover, (0,self._boton_size[1]), (self._boton_size[0]/2,0), self.linesize_foreground)
            pygame.draw.line(self.img_hoverNext, self.color_hover, (self._boton_size[0]/2,0), (self._boton_size[0],self._boton_size[1]), self.linesize_foreground)
        
              # Estado down
            self.img_downNext.fill(self.color_backgroundBoton)
            pygame.draw.rect(self.img_downNext, self.color_down, ((0,0),self.rect_botonNext.size), self.linesize_foreground)
            pygame.draw.line(self.img_downNext, self.color_down, (0,self._boton_size[1]), (self._boton_size[0]/2,0), self.linesize_foreground)
            pygame.draw.line(self.img_downNext, self.color_down, (self._boton_size[0]/2,0), (self._boton_size[0],self._boton_size[1]), self.linesize_foreground)
        
            # Estado disable. Solo agrego los botones con el color disable a la imagen
              # boton siguiente
            pygame.draw.rect(self.img_disable, self.color_disable, pygame.Rect((self.width-self._boton_size[0], 0),self._boton_size), self.linesize_foreground)
            pygame.draw.line(self.img_disable, self.color_disable, (self.width-self._boton_size[0],self._boton_size[1]), (self.width-self._boton_size[0]/2,0), self.linesize_foreground)
            pygame.draw.line(self.img_disable, self.color_disable, (self.width-self._boton_size[0]/2,0), (self.width,self._boton_size[1]), self.linesize_foreground)

              # boton prev
            pygame.draw.rect(self.img_disable, self.color_disable, pygame.Rect((self.width-self._boton_size[0], self._boton_size[1]),self._boton_size), self.linesize_foreground)
            pygame.draw.line(self.img_disable, self.color_disable, (self.width-self._boton_size[0],self._boton_size[1]), (self.width-self._boton_size[0]/2,self._boton_size[1]*2), self.linesize_foreground)
            pygame.draw.line(self.img_disable, self.color_disable, (self.width-self._boton_size[0]/2,self._boton_size[1]*2), (self.width,self._boton_size[1]), self.linesize_foreground)
        

            # Dibuja el borde del control
            if self.border:
                  # Normal
                pygame.draw.rect(self.img_normal, self.color_normal, (0,0,self.get_width(),self.get_height()), self.linesize_border)
                  # Hover
                pygame.draw.rect(self.img_hover, self.color_hover, (0,0,self.get_width(),self.get_height()),self.linesize_border)
                  # Down
                pygame.draw.rect(self.img_down, self.color_down, (0,0,self.get_width(),self.get_height()),self.linesize_border)
                  # Disable
                pygame.draw.rect(self.img_disable, self.color_disable, (0,0,self.get_width(),self.get_height()),self.linesize_border)

            for l in range(0, self.get_width(), 10):
                pygame.draw.line(self.img_disable, self.color_disable, (l, self.get_height()),(l+10, 0) )

        else:
            print 'El modo grafico ' + self.get_GraphicMode() + ' no existe'

       


    def render(self, target, b=None):
        '''Dibuja nuestro control en la superficie indicada.'''
         
        esta_visible = self.visible
        esta_encontexto = self.is_context()
        esta_activado = self.enable
        esta_encima = self.is_hover()
        esta_enfoco = self.is_Focus


        # Construye el bitmap de texto correspondiente y lo coloca en el foreground
        bitmap = self.font.render(self.text, True, self.color_foreground)
        bitmap_h = self.font.render(self.text, True, self.color_foreground_h)
        bitmap_disable = self.font.render(self.text, True, self.color_disable)
        bitmapWidth, bitmapHeight = self.font.size(self.text) 

        # Calculo la posicion del texto
            # Valor del usuario
        if self.align == None:
            posX, posY = self.pos_text
        
            # Posicion X
        if self.align == A_LEFT or self.align == A_TOPLEFT or self.align == A_BOTTOMLEFT:
            posX = 0
        
        if self.align == A_CENTER or self.align == A_TOP or self.align == A_BOTTOM:
            posX = self.get_width()/2 - bitmapWidth/2

        if self.align == A_RIGHT or self.align == A_BOTTOMRIGHT or self.align == A_TOPRIGHT:
            posX = self.get_width() - bitmapWidth - self._boton_size[0]

            # Posicion Y
        if self.align == A_TOPLEFT or self.align == A_TOP or self.align == A_TOPRIGHT:
            posY = 0
        
        if self.align == A_CENTER or self.align == A_LEFT or self.align == A_RIGHT:
            posY = self.get_height()/2 - bitmapHeight/2

        if self.align == A_BOTTOMLEFT or self.align == A_BOTTOMRIGHT or self.align == A_BOTTOM:
            posY = self.get_height() - bitmapHeight

        # Dibujo el texto sobre la img_foreground (normal y hover)
        self.img_foreground.fill(Color.Transparent)
        self.img_foreground.blit(bitmap, (posX, posY))
        self.img_foreground_h.fill(Color.Transparent)
        self.img_foreground_h.blit(bitmap_h, (posX, posY))
        self.img_disable.blit(bitmap_disable, (posX, posY))


        if esta_visible and esta_encontexto:
            if not esta_activado:
                target.blit(self.img_disable, self.get_pos())
                #target.blit(self.img_foreground, self.get_pos())
            else:

                if esta_encima == 0:
                    target.blit(self.img_normal, self.get_pos())
                    target.blit(self.img_normalNext, self.rect_botonNext)
                    target.blit(self.img_normalPrev, self.rect_botonPrev)
                    target.blit(self.img_foreground, self.get_pos())

                if esta_encima == 1:  # Area de texto. No me importa si esta down
                    target.blit(self.img_hover, self.get_pos())
                    target.blit(self.img_normalNext, self.rect_botonNext)
                    target.blit(self.img_normalPrev, self.rect_botonPrev)
                    target.blit(self.img_foreground_h, self.get_pos())

                if esta_encima == 2:  # boton siguiente
                    if self.is_down(b):
                        target.blit(self.img_hover, self.get_pos())
                        target.blit(self.img_downNext, self.rect_botonNext)
                        target.blit(self.img_normalPrev, self.rect_botonPrev)
                    else:
                        target.blit(self.img_hover, self.get_pos())
                        target.blit(self.img_hoverNext, self.rect_botonNext)
                        target.blit(self.img_normalPrev, self.rect_botonPrev)
                    
                    target.blit(self.img_foreground, self.get_pos())
                    
                if esta_encima == 3:  # boton anterior
                    if self.is_down(b):
                        target.blit(self.img_hover, self.get_pos())
                        target.blit(self.img_normalNext, self.rect_botonNext)
                        target.blit(self.img_downPrev, self.rect_botonPrev)
                    else:
                        target.blit(self.img_hover, self.get_pos())
                        target.blit(self.img_normalNext, self.rect_botonNext)
                        target.blit(self.img_hoverPrev, self.rect_botonPrev)
                                    
                    target.blit(self.img_foreground, self.get_pos())

            if esta_enfoco:
                pygame.draw.rect(target, self.color_focus, self.get_rect(), self.linesize_focus)

            return True
        else:
            return False

    def next(self):
        '''Aumenta en 1 el elemento en la lista.'''
        self._indice += 1
        if self._indice > len(self._lista)-1:
            if self.loop:
                self._indice = 0
            else:
                self._indice = len(self._lista)-1

    def prev(self):
        '''Disminuye en 1 el elemento en la lista.'''
        self._indice -= 1
        if self._indice < 0:
            if self.loop:
                self._indice = len(self._lista)-1
            else:
                self._indice = 0


    def click(self, button=None):
        '''Método a llamar cuando se hace click. Devuelve 1 si está encima del control, de lo contrario devuelve 0'''

        esta_encima = super(RollList,self).click(button)

        if self.enable:
            if esta_encima == 2:
                self.next()

            elif esta_encima == 3:
                self.prev()


class Slider(ControlBase):
    '''Barra deslizable'''
    All=[]

    def __init__(self, rect):
        super(Slider,self).__init__(rect)
    
    
        self._max = 100
        self._min = 0
        self._value = 50
        self._orientation = O_HORIZONTAL
        self.border = False   # Sin bordes


        # Cursor
        self._cursorThickness = 5
        self._cursorSize = (self._cursorThickness,rect[3])
        self._cursorPos = (0,0)
        self.img_cursorNormal = pygame.Surface(self._cursorSize, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_cursorHover = pygame.Surface(self._cursorSize, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_cursorDown = pygame.Surface(self._cursorSize, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_cursorDisable = pygame.Surface(self._cursorSize, pygame.HWSURFACE|pygame.SRCALPHA)
        self._arrastrar = False # variable auxiliar para el arrastrado del cursor

        # Linea central
        self._thicknessLineSize = 4  #  Grosor de la linea central del control
        self._centralLineSize = pygame.Rect(0, (self.height-self._thicknessLineSize)/2, self.width, self._thicknessLineSize)  #  Rectangulo de la linea central

        self._setCursorPos()  # Actualiza la posicion del cursor

        Slider.All.append(self)

    @property
    def cursorThickness(self):
        return self._cursorThickness
    
    @cursorThickness.setter
    def cursorThickness(self, v):
        self._cursorThickness = v

        if self._orientation == O_HORIZONTAL:
            self.cursorSize = (self._cursorThickness, self.height) 
        elif self._orientation == O_VERTICAL:
            self.cursorSize = (self.width, self._cursorThickness) 


    @property
    def cursorSize(self):
        '''Tupla con el tamaño del cursor.'''
        return self._cursorSize
    
    @cursorSize.setter
    def cursorSize(self, val):
        self._cursorSize = val
        self.img_cursorNormal = pygame.Surface(val, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_cursorHover = pygame.Surface(val, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_cursorDown = pygame.Surface(val, pygame.HWSURFACE|pygame.SRCALPHA)
        self.img_cursorDisable = pygame.Surface(val, pygame.HWSURFACE|pygame.SRCALPHA)
        self._setCursorPos()

    
    @property
    def centralLineSize(self):
        '''Ancho de la línea central del control'''

        return self._thicknessLineSize


    @centralLineSize.setter
    def centralLineSize(self, val):
        self._thicknessLineSize = val

        if self.orientation == O_HORIZONTAL:
            self._centralLineSize = pygame.Rect(0, (self.height-val)/2, self.width, val)
        
        elif self.orientation == O_VERTICAL:
            self._centralLineSize = pygame.Rect((self.width-val)/2, 0, val ,self.height)
        


    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, v):
        self._orientation = v
        self.cursorThickness = self._cursorThickness  # Solo actualiza la relacion de aspecto del cursor
        self.updateGraphics()    

    @property
    def cursorPos(self):
        '''Posicion del cursor. Solo lectura'''
        return self._cursorPos
    
    def _setCursorPos(self):
        '''Setea la posicion del cursor en funcion del valor max, valor min y el valor actual. Es de uso privado'''

        if self.orientation == O_HORIZONTAL:
            self._cursorPos = ((self.width-self._cursorThickness)*(self._value-self._min)/(self._max-self._min)+self.left, self.top +(self.height-self._cursorSize[1])/2 )
        
        elif self.orientation == O_VERTICAL:
            self._cursorPos = (self.left +(self.width-self._cursorSize[0])/2, (-1*(self.height-self._cursorThickness)*(self._value-self._min)/(self._max-self._min)+self.top+self.height-self._cursorThickness )) #-self.height)


    @property
    def maxValue(self):
        '''Valor máximo'''
        return self._max

    @maxValue.setter
    def maxValue(self, v):
        self._max = v

        if (self._max-self._min):  # Esto es para evitar division por cero
            self.value = self._value  # Recalcula la posicion actual, por si quedo fuera del nuevo limiteself.value = self._value  # Recalcula la posicion actual, por si quedo fuera del nuevo limite

    @property
    def minValue(self):
        '''Valor mínimo'''
        return self._min

    @minValue.setter
    def minValue(self, v):
        self._min = v

        if (self._max-self._min):  # Esto es para evitar division por cero
            self.value = self._value  # Recalcula la posicion actual, por si quedo fuera del nuevo limiteself.value = self._value  # Recalcula la posicion actual, por si quedo fuera del nuevo limite

    @property
    def value(self):
        '''Valor actual'''
        return self._value

    @value.setter
    def value(self, v):
        if v < self._min:
            self._value = self._min
        elif v > self._max:
            self._value = self._max
        else:            
            self._value = v
    
        self._setCursorPos()
        

    def render(self, target, b=None):
        '''Dibuja el control en la superficie indicada en target.'''

        r = super(Slider, self).render(target, b)

        #  Las siguientes instrucciones solo dibujan el cursor en la posicion correspondiente,
        #  el rectangulo del control ya fue dibujado por el render del ControlBase

        #  Si no hay presionado ningun boton detiene la operacion de arrastrar si se ha iniciado
        btns = pygame.mouse.get_pressed()
        if not (btns[0] or btns[1] or btns[2]):  
            self._arrastrar = False

        if r :
            h = self.is_hover()

            if not self.enable:
                target.blit(self.img_cursorDisable, self.cursorPos)
            else:
                if h: 
                    if self.is_down(b):

                        if self._arrastrar:
                            if self.orientation == O_HORIZONTAL:
                                self.value = ((self.maxValue-self.minValue+1)*(pygame.mouse.get_pos()[0]-self.left)/self.width)+self.minValue

                            elif self.orientation == O_VERTICAL:
                                self.value = self.minValue + (pygame.mouse.get_pos()[1]-self.top-self.height)*(self.maxValue-self.minValue)/(-1*self.height)

                        target.blit(self.img_cursorDown, self.cursorPos)
                    else:
                        target.blit(self.img_cursorHover, self.cursorPos)
                else:
                    target.blit(self.img_cursorNormal, self.cursorPos)
       




    def updateGraphics(self):
        '''Actualiza como se mostrará el control según el modo gráfico establecido. Debe ser llamado cada vez que la imagen del control cambie'''


        if self.get_GraphicMode() == 0:

            # Actualizo la linea central y el tamaño del cursor
            self.centralLineSize = self._thicknessLineSize
            self.cursorSize = self._cursorSize

            # Actualizo la posicion del cursor
            self._setCursorPos()

            # Linea central
            pygame.draw.rect(self.img_normal, self.color_normal, self._centralLineSize, 1) #(0, (self.height-self.centralLineSize)/2, self.width, self.centralLineSize), 1)
            pygame.draw.rect(self.img_hover, self.color_hover, self._centralLineSize, 1) #(0, (self.height-self.centralLineSize)/2, self.width, self.centralLineSize), 1)
            pygame.draw.rect(self.img_down, self.color_down, self._centralLineSize, 1) #(0, (self.height-self.centralLineSize)/2, self.width, self.centralLineSize), 1)
            # Cursor
            pygame.draw.rect(self.img_cursorNormal, self.color_normal, (0,0,self.cursorSize[0], self.cursorSize[1]), 0)
            pygame.draw.rect(self.img_cursorHover , self.color_hover , (0,0,self.cursorSize[0], self.cursorSize[1]), 0)
            pygame.draw.rect(self.img_cursorDown, self.color_down, (0,0,self.cursorSize[0], self.cursorSize[1]), 0)
    
        


    def is_hover(self):
        '''Devuelve un entero mayor que cero cuando el cursor del mouse está sobre el control.
        Tabla de valores:
            0 --> No está sobre el control
            1 --> Está sobre el cursor del control
            2 --> Está sobre la línea central del control
            3 --> Está sobre el control (pero fuera del cursor y la línea central)'''
        
        pos = pygame.mouse.get_pos()  #  Posicion del mouse
        res = 0  #  Valor por defecto
        
        if self.visible and self.is_context():

                #  Sobre el control
            if self.get_rect().collidepoint(pos):
                res = 3  

                #  Sobre la linea
            if self._centralLineSize.move(self.left,self.top).collidepoint(pos):
                res = 2

                #  Sobre el cursor
            if self.img_cursorNormal.get_rect(topleft = self.cursorPos).collidepoint(pos):
                res = 1

            return res


    def click(self, boton=None):
        '''Establece el valor del control según donde se hizo click. Si es sobre la línea central
        posiciona el cursor allí y establece el valor. Si es sobre el cursor inicia una operación
        de arrastrar para posicionarlo y establecer el valor'''


        esta_encima = self.is_hover()
        pos = pygame.mouse.get_pos()
                   
        if esta_encima:
            if self.enable:
                if self.enableFocus:
                    ControlBase.OnFocus = self

            if esta_encima == 1:  # sobre el cursor
                self._arrastrar = True

            elif esta_encima == 2:  # Sobre la linea
                if self.orientation == O_HORIZONTAL:
                    self.value = ((self.maxValue-self.minValue+1)*(pos[0]-self.left)/self.width)+self.minValue
                
                elif self.orientation == O_VERTICAL:
                    self.value = self.minValue + (pygame.mouse.get_pos()[1]-self.top-self.height)*(self.maxValue-self.minValue)/(-1*self.height)

        else:
            ControlBase.OnFocus = None
            
        return esta_encima


class TextList(ControlBase):
    '''Control que muestra una lista y donde se puede seleccionar un elemento de la lista'''
    All = []

    def __init__(self, rect):
        super(TextList, self).__init__(rect)
        

        TextList.All.append(self)


class Option(ControlBase):
    All = []

    def __init__(self, rect):
        super(Option, self).__init__(rect)
        

        Option.All.append(self)



class Grid(ControlBase):
    All = []

    def __init__(self, rect):
        super(Grid, self).__init__(rect)
        

        Grid.All.append(self)


class Tab(ControlBase):
    All = []

    def __init__(self, rect):
        super(Tab, self).__init__(rect)
        

        Tab.All.append(self)


class Animation(ControlBase):

    All = []

    def __init__(self, rect):
        super(Animation, self).__init__(rect)
        

        Animation.All.append(self)


class InfoVersion(object):
    """Informacion sobre la version"""
    def __init__(self):
        self._version = 0
        self._subversion = 0
        self._revision = 1
        self._estado = "a" 

    def get_version(self):
        return self._version

    def get_subversion(self):
        return self._subversion

    def get_revision(self):
        return self._revision

    def get_estado(self):
        return self._estado

    def __str__(self):
        return str(self.get_version()) + "." + str(self.get_subversion()) + "." + str(self.get_revision()) + self.get_estado()

