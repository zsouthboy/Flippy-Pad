#!/usr/bin/env python
import pygame
from pygame.locals import *

class mousePointer:
    def __init__(self, gv, defaultImage=None):
        #this is a GIGANTIC difference in doing an "image" cursor
        #and a regular one
        #TODO: decision
        
        self.gv = gv
        self.gv.registerInstance("mousePointer", self)
        self.display = self.gv.display

        self.pointerList = []
        pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))
        
        self.init()

    def init(self):
        pass

    #Cursor size/type will be set by others

    def setPointer(self, pointer):
        '''
        Changes the mouse pointer to an image.
        Get a list of images from mousePointer.getPointerList()
        '''
        self.currentPointer = pointer
        self.gv.console.log("MOUSE: Changed pointer.")

    def getPointerList(self):
        return self.pointerList

    def loadImage(self, path, image):
        return pygame.image.load(path, image).convert_alpha()        

    def draw(self):
        
        #todo: mousepointer shadow?
        #self.display.drawitem(self.currentShadow, \
        #        (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 4), \
        #                     self.gv.zorder_mousecursor)
        
        #self.display.drawitem(self.currentPointer, pygame.mouse.get_pos(), \
        #                      self.gv.zorder_mousecursor)
        pass

                                
