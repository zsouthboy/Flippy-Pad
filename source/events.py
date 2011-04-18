#!/usr/bin/env python
import pygame, sys
from pygame.locals import *

class events():
    def __init__(self, globalvariables):
        #remember to grab a console instance DONE, and a mouse instance eventually
        self.gv = globalvariables
        self.gv.registerInstance("Events", self)
        
        self.display = self.gv.display
        self.console = self.gv.console
        self.eventUsers = []
    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                self.handleResize(event.size)
                self.sendEvents(event)
            elif event.type == KEYDOWN and event.key == pygame.K_BACKQUOTE:
                self.console.enable()
            elif (event.type == KEYDOWN and event.key == pygame.K_ESCAPE) \
                 or event.type == QUIT:
                sys.exit()                
            else:
                self.sendEvents(event)
                   

            
                
    #Todo: programmable minimum size, probably set in gv and ini
    def handleResize(self, newSize):
        size = newSize
        if size[0] < 640:
            size = 640, size[1]
        if size[1] < 480:
            size = size[0], 480
            
        self.gv.setSize(size)
        self.display.init()
        self.console.init()

    def registerEventUser(self, eventUser):
        '''
        Registers a target that we want events sent to.
        '''
        #For each menu instance, playfield instance, etc. we'll need to register
        #as someone to handle the events
        #push on top of list each time, FILO queue
        
        self.eventUsers.insert(0, eventUser)
        self.gv.console.log("EVENTS: Registered %s" % eventUser)
        
    def unregisterEventUser(self, eventUser):
        '''
        Unregister the instance from recieving events.
        '''

        self.eventUsers.remove(eventUser)
        #print "UNREGISTER"
        self.gv.console.log("EVENTS: Unregistered %s" % eventUser)
        

    def sendEvents(self, event):
        if self.gv.consoleenabled == True:
            self.console.getKeys(event)
            if event.type == VIDEORESIZE:
                for user in self.eventUsers:
                    #don't allow users to swallow resize events
                    user.handleEvent(event)
        else:
            for user in self.eventUsers:
                if user.handleEvent(event) == True:
                    break
            
        
