#!/usr/bin/env python
import pygame
from pygame.locals import *

import mousePointer

class display:
    def __init__(self, globalvariables, background=None):
        #TODO: add background handling
        self.gv = globalvariables
        self.gv.registerInstance("Display", self)
                
        self.background = background
        self.displaylist = []
        pygame.display.init()
        pygame.key.set_repeat(350, 100)
        ##TODO remember to create and set an icon
        #pygame.display.set_icon(ball)
        
        pygame.font.init()
        #todo: why the F am i hardcoding one font?
        self.UItext = pygame.font.Font("LiberationMono-Regular.ttf", 15)
        
        self.init()

    def init(self):
        #moved init items in here
        self.size = self.gv.size
        self.width = self.gv.size[0]
        self.height = self.gv.size[1]
        pygame.display.set_caption(self.gv.version)
        #todo: allow setting resizable on main window or not / FULLSCREEN
        self.screen = pygame.display.set_mode((self.gv.size))        
        #self.screen = pygame.display.set_mode((self.gv.size), RESIZABLE)
        #self.screen = pygame.display.set_mode((self.gv.size), FULLSCREEN | HWSURFACE | DOUBLEBUF)
        
        self.gv.screenBitDepth = pygame.display.Info().bitsize
        
    def drawtext(self, text, color, rect, zorder):
        '''
        Pass unicode text, a color tuple(RGB), a rect to draw at.
        Get a rect back that represents the size of the text.
        '''
        #this is immediately added to the drawitems queue
        #rendertext is to return a surface
        temp = self.UItext.render(text, 1, color)
        self.drawitem(temp, rect, zorder)       
        #return the rect it got drawn at
        return temp.get_rect()
    
    def renderText(self, text, color):
        '''
        Returns a surface containing the text in the color specified
        '''
        temp = self.UItext.render(text, 1, color).copy()
        
        return temp
                
    def drawitem(self, item, itemxy, zorder):
        '''
        Blits pygame surface item to screen at itemrect.
        '''

        self.displaylist.append((item, itemxy[:], zorder))


    def paint(self):
        self.screen.fill((0,0,0))
        
        #obviously paint the FPS marker last
        if self.gv.showFPS == True:
            self.drawtext(u"FPS: %s" % int(self.gv.Clock.get_fps()), (0,255,0), (0, self.height - 15), self.gv.zorder_aboveui)


        #iterate through our list and paint, in z order, from lowest to highest

        self.displaylist.sort(key=lambda x: x[2])

        for item in self.displaylist:
            self.screen.blit(item[0], item[1])
            
        
        pygame.display.flip()
        self.displaylist = []
