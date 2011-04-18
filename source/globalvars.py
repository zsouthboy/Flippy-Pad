#!/usr/bin/env python
import pygame
from pygame.locals import *

class globalvars:

    def __init__(self, size, framerate):
        #TODO really gotta pull these from an INI instead.
        self.setSize(size)
        
        self.framerate = framerate
        self.consoleenabled = False
        self.showFPS = False
        self.blinkrate = 200 #blinkrate is a misnomer, it's actually ms between blinks
        #for each layer, a new z order that allows us to paint everything, while
        #stil getting overwritten correctly
        self.zorder_bg = -1
        self.zorder_actor = 0
        self.zorder_ui = 1
        self.zorder_aboveui = 2
        self.zorder_mousecursor = 3
        self.screenBitDepth = 0
        self.dirty = False

    def setSize(self, size):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.rect = pygame.Rect((0,0), size)

    def getSize(self):
        return self.size

    def getWidth(self):
        return self.width

    def getRect(self):
        return self.rect

    def getHeight(self):
        return self.height

    def registerInstance(self, which, instance):
        if which == "Display":
            self.display = instance
        elif which == "Playfield":
            self.playfield = instance
        elif which == "Console":
            self.console = instance
        elif which == "Events":
            self.events = instance
        elif which == "mousePointer":
            self.mousePointer = instance
        else:
            print "ERROR: No matching instance for %s" % which
