#!/usr/bin/env python
import pygame
from pygame.locals import *
#import pygame.gfxdraw

#for menu support
import menu
#to change the mouse pointer based on context
import mousePointer

class flippy:
    def __init__(self, globalvariables):
        self.gv = globalvariables
        self.gv.registerInstance("Playfield", self)
        self.registerForEvents()

        self.mousePointer = mousePointer.mousePointer(self.gv)
        self.mouseDown = False
        
        self.display = self.gv.display
        self.menuList = []

        #currentSurface is an instance of the canvas class
        self.currentSurface = None
        #
        self.currentSurfaceNumber = 0
        #store surfaces in a list
        self.surfaces = []
        #... and store undo states in a list
        self.undoHistory = []

        self.clicked = False
        self.init()

    def init(self):

        self.rect = self.gv.getRect()
        self.initSurface()
        self.addMenu()

        #floating toolbox was for testing but the code is still here
        #self.addToolbox()

    def initSurface(self):
        '''
        Initializes a canvas for us to draw on.
        '''
        
        self.currentSurface = canvas(self.gv, self.rect)
        self.clearCurrentSurface()

        self.surfaces.insert(self.currentSurfaceNumber, self.currentSurface)
        self.currentSurfaceNumber += 1
        

    def clearCurrentSurface(self):
        self.currentSurface.clear()
        self.clearUndo()

    def newPage(self):
        self.initSurface()

    def previousPage(self):
        self.changeCurrentSurface(-1)
            
    def nextPage(self):
        self.changeCurrentSurface(1)
            

    def changeCurrentSurface(self, number):
        self.currentSurfaceNumber += number
        if self.currentSurfaceNumber < 1:
            self.currentSurfaceNumber = len(self.surfaces)
        elif self.currentSurfaceNumber > len(self.surfaces):
            self.currentSurfaceNumber = 1
            
        self.currentSurface = self.surfaces[self.currentSurfaceNumber - 1]
        self.clearUndo()

    def clearUndo(self):
        self.undoHistory = []
    
    def addMenu(self):
        self.simplemenu = menu.menu(self.gv, 58, "left")
        self.simplemenu.addButton((50,50), (3, 3), self.nextPage, \
                                  "Next Page", \
                                  "images/menu/newpagenormal.png", \
                             "images/menu/newpagehover.png", \
                              "images/menu/newpagepressed.png")
        
        self.simplemenu.addButton((50,50), (3,57), self.newPage, \
                                  "New Page", \
                                  "images/menu/newpagenormal.png", \
                             "images/menu/newpagehover.png", \
                              "images/menu/newpagepressed.png")
        
        self.simplemenu.addButton((50,50), (3,111), self.previousPage, \
                                  "Previous Page", \
                                  "images/menu/newpagenormal.png", \
                             "images/menu/newpagehover.png", \
                              "images/menu/newpagepressed.png")
        
        self.simplemenu.addButton((50,50), (3,199), self.clearCurrentSurface, \
                                  "Delete Page", \
                                  "images/menu/newpagenormal.png", \
                             "images/menu/newpagehover.png", \
                              "images/menu/newpagepressed.png")

        #we'll hold on to this reference to update it later
        self.playButton = self.simplemenu.addButton((50,50), (3,277), \
                                                    self.doNothing, \
                                  "Play", \
                                  "images/menu/newpagenormal.png", \
                             "images/menu/newpagehover.png", \
                              "images/menu/newpagepressed.png")

        self.simplemenu.addButton((25,50), (3,385), self.doNothing, \
                                  "Slower", \
                                  "images/menu/newpagenormal.png", \
                             "images/menu/newpagehover.png", \
                              "images/menu/newpagepressed.png")

        self.simplemenu.addButton((25,50), (28,385), self.doNothing, \
                                  "Faster", \
                                  "images/menu/newpagenormal.png", \
                             "images/menu/newpagehover.png", \
                              "images/menu/newpagepressed.png")
        
        #..and we'll hold onto a reference to this for later updates.        
        self.statusText = self.simplemenu.addStatusText((62,4), "Page 1 of 1", \
                                                        (210,210,210))
        
        
        self.menuList.append(self.simplemenu)

    def updateStatusText(self):
        self.statusText.setText("Page %s of %s" % \
                                (self.currentSurfaceNumber, \
                                            len(self.surfaces)))
        
    def doNothing(self):
        self.gv.console.log("PLAYFIELD: This button does nothing!")

    def registerForEvents(self):
        self.gv.events.registerEventUser(self)
        self.gv.console.log("PLAYFIELD: Registered %s for events!" % self)
    
    def handleEvent(self, event):
        '''
        Handles a pygame event. If it doesn't belong to this, return False.
        Event class will continue down its tree.
        '''

        if event.type == KEYDOWN:
            #print event
            if event.key == pygame.K_z:
                #print "PLAYFIELD: UNDO!"
                self.undo()
            elif event.key == pygame.K_c:
                self.clearCurrentSurface()
            return True
        
        elif event.type in (MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP):
            #print event
            self.handleMouse(event)
            return True
        
        return True
    
    def drawOnSurface(self, position):
        self.currentSurface.applyBrush(1, (0,0,0), self.lastPosition, position)
        self.lastPosition = position

    def undo(self):
        if len(self.undoHistory) > 0:
            self.currentSurface.setSurface(self.undoHistory.pop())

    def addToUndoStack(self, surface):
        self.undoHistory.append(self.currentSurface.copy())
        if len(self.undoHistory) > 10:
            del self.undoHistory[0]
    
    
    def handleMouse(self, event):
        #print "mouse movie yay! %s" % position
        #print position
        if event.type == MOUSEBUTTONDOWN:
            self.lastPosition = event.pos
            self.addToUndoStack(self.currentSurface.copy())
            self.clicked = True

        if event.type == MOUSEBUTTONUP:
            self.clicked = False
            
        if event.type == MOUSEMOTION and event.buttons[0] == True and \
           self.clicked == True:
                self.drawOnSurface(event.pos)

    def setMouseDown(self, down):
        self.mouseDown == down

    def getMouseDown(self):
        return self.mouseDown
    
    def update(self):

        #self.updateStatusText()
        self.draw()

        #for each of the menus instantiated, draw
        for menu in self.menuList:
            menu.draw()                
        
    def draw(self):

        #draw the mouse pointer
        self.updateStatusText()
        self.mousePointer.draw()
        
        self.currentSurface.draw()
        
class canvas:
    def __init__(self, gv, rect):
        self.gv = gv
        self.rect = rect
        self.surface = pygame.surface.Surface(self.rect.size)
        self.postitColor = (239,231,120)
        self.surface.fill(self.postitColor)

        #WOO, polymorphism! my first real use!
        #use shitty non-aaed drawing if bit depth is too low
        if self.gv.screenBitDepth < 24:
            self.gv.console.log("CANVAS: Screen bit depth %s does not support AA drawing."  \
                                         % self.gv.screenBitDepth)
            self.gv.console.log("CANVAS: Continuing happily.")
            self.drawLine = self.drawLineLowBitDepth

        self.init()

    def init(self):
        
        pass

    def applyBrush(self, brush, color, lastPosition, currentPosition):
        #print "woudlv'e painted %s size spot at %s" % (brush, position)
        #TODO: oh god so much is missing
        self.drawLine(brush, color, lastPosition, currentPosition)
        #self.paint(position)

    def drawLineLowBitDepth(self, brush, color, lastPosition, currentPosition):
        pygame.draw.line(self.surface, color, lastPosition, currentPosition)
        
    def drawLine(self, brush, color, lastPosition, currentPosition):
        pygame.draw.aaline(self.surface, color, lastPosition, \
                           currentPosition, True)
        
        #pygame.gfxdraw.line(self.surface, lastPosition[0], lastPosition[1], \
        #                    currentPosition[0], currentPosition[1], \
        #                    (0,0,0))

    def clear(self):
        self.surface.fill(self.postitColor)
    
    #def paint(self, position):
    #    self.surface.set_at(position, (0,0,0))    

    def getRect(self):
        return self.rect                

    def copy(self):
        return self.surface.copy()

    def setSurface(self, surface):
        self.surface = surface
        
    def draw(self):
        
        self.gv.display.drawitem(self.surface, self.rect, self.gv.zorder_actor)
