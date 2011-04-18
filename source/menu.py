#!/usr/bin/env python
import pygame, sys
from pygame.locals import *

NORMAL = 0
CLICKED = 1
DISABLED = 2

class menu:
    def __init__(self, globalvariables, size, position, floating = False):
        '''
        Instantiate a new menu.
        Floating or docked.
        If floating, position and size are normal. Floating menus can be
        dragged by a mouse click and move on a non-hotspot part of the surface.
        If docked, position defines docking side [top, bottom, left, right]
        and size relates to how far from the edge the menu extends.
        For example:
            menu.menu(gv, 100, "top")
                Creates a docked menu that is 100 pixels in height.
            menu.menu(gv, (100,300), (234, 453), True)
                Creates a floating toolbar that is 100x300, whose uppper-left
                corner is at (234,453).
        '''
        self.gv = globalvariables
        self.display = self.gv.display
        self.registerForEvents()

        self.floating = floating
        self.rect = None

        #position and size could be a string
        self.position = position
        self.size = size

        self.isMoving = False
        self.init(size, position, self.gv.getSize())
        self.buttonList = []
        self.statusTextList = []
        
    def init(self, size, position, sizeOfScreen):
        if self.floating:
            temp = position
            #if the origin is off screen after a resize, place in the center
            #TODO: there is still an edge case here, if the resize is just right
            #the menu is barely showing and the user cannot find it
            if position[0] > sizeOfScreen[0] or position[1] > sizeOfScreen[1]:
                temp = ((self.gv.getWidth() / 2), (self.gv.getHeight() / 2))
                self.gv.console.log("MENU: Moved offscreen menu onscreen.")
            self.rect = pygame.Rect(temp, size)
            
        else:
            #todo test each of these for correctness
            if position == "top":
                self.rect = pygame.Rect((0,0), (self.gv.getWidth(), size))
                
            elif position == "bottom":
                self.rect = pygame.Rect((0,self.gv.getHeight() - size), \
                                    (self.gv.getWidth(), size))
                
            elif position == "left":
                self.rect = pygame.Rect((0,0), (size, self.gv.getHeight()))
                
            elif position == "right":
                self.rect = pygame.Rect((self.gv.getWidth() - self.size,0), \
                                    (size, self.gv.getHeight()))
                
            else:
                self.rect = pygame.Rect(position, size)

        #todo: allow gradient/image background, curved corners, etc
        self.background = pygame.surface.Surface((self.rect.size))
        self.background.fill((214,216,142))
        #TODO: The word "Menu" is silly here. Titling a menu might be useful
        #but would need "real" implementation
        #self.background.blit(self.display.renderText("Menu!", (255,0,56)), (4,4))


    def resize(self, sizeOfScreen):

        #call init with already recorded information
        if self.floating:
            self.init(self.rect.size, self.rect.topleft, sizeOfScreen)
        else:
            self.init(self.size, self.position, sizeOfScreen)

        
    def addButton(self, size, position, functionToCall, name, imageNormal, \
                  imageHover, imageClicked, \
                  imageDisabled = None):
        temp = button(self.gv, size, position, functionToCall, \
                                      name, \
                                      imageNormal, imageHover, \
                                       imageClicked, imageDisabled)
        self.buttonList.append(temp)
        self.gv.console.log("MENU: Added '%s' - %s button at %s, filename %s!" % \
                            (name, size, position, imageNormal))
        return temp

    #def removeButton(self, button):
    #    self.buttonList.remove(button)        
    #    print "removed button!"

    def addStatusText(self, position, text, color):
        temp = statusText(self.gv, position, text, color)
        self.statusTextList.append(temp)
        self.gv.console.log("MENU: Added status text.")
        return temp
        

    def move(self, position):
        #moves in a relative manner by position
        if self.floating:
            #print self.rect
            self.rect.move_ip(position)
            #print self.rect
            #print "Moved menu"

    def moveMenu(self, click = None, position = (0,0)):
        '''
        Handles deciding to move the menu. Actually moves via move().
        '''
        if self.isMoving:
            self.move(position)
        if click != None:
            if click == True:
                self.isMoving = True
            elif click == False:
                self.isMoving = False
        
    def draw(self):
        #draw solid gray background at self.position for self.size
        self.display.drawitem(self.background, self.rect, self.gv.zorder_ui)
        #then for each button in the button list, draw
        
        for button in self.buttonList:

            self.display.drawitem(button.draw(), \
                button.getRect().move(self.rect.topleft), \
                    self.gv.zorder_ui)

        for text in self.statusTextList:
            self.display.drawitem(text.draw(), \
                    text.getRect().move(self.rect.topleft), \
                    self.gv.zorder_ui)
        
        
    def registerForEvents(self):
        self.gv.events.registerEventUser(self)
        self.gv.console.log("MENU: Registered %s for events!" % self)

    def unregisterForEvents(self):
        self.gv.events.unregisterEventUser(self)
        self.gv.console.log("MENU: Unregistered %s for events!" % self)

    def handleEvent(self, event):
        '''
        Handles a pygame event. If it doesn't belong to this menu, return False.
        Event class will continue down its tree.
        '''
        #TODO: fill me in, figure out if the event belongs to us, if not
        #send it onward

        #TODO: playfield class needs to be able to set and unset keys that
        #its menu instances handle dynamically


        #TODO: If the menu is floating and the window is resized, it's possible
        #to lose the menu offscreen
        #need to check for resize event and move the menus appropriately

        
        #TODO: even if the rect isn't intersected, if we're moveMenu()ing
        #and mouse is still down, we need to move it
        if self.isMoving == True:
            
            if event.type == MOUSEBUTTONUP:
                #clear this here, regardless of if we're in this rect
                self.moveMenu(False)
                
            elif event.type == MOUSEMOTION:
                self.moveMenu(None, event.rel)
                
        
        if event.type in (KEYDOWN, KEYUP):
            if event.key == pygame.K_d and event.type == KEYDOWN:
                self.gv.console.log("MENU: %s" % event)
                self.temp()
                return True

        if event.type in (MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP):
            
            for button in self.buttonList:
                button.clearHover()
                
            if self.rect.collidepoint(event.pos):
                #self.gv.console.log("MENU: %s" % event)
                
                if event.type == MOUSEBUTTONDOWN:
                    
                    for button in self.buttonList:                        
                        if self.getHotspot(button).collidepoint(event.pos):
                            
                            button.depress()
                            
                            return True

                    self.moveMenu(True)

                if event.type == MOUSEBUTTONUP:
                    
                    for button in self.buttonList:                        
                        if self.getHotspot(button).collidepoint(event.pos):
                            
                            button.clicked()
                        else:
                            button.reset()
                            
                        

                elif event.type == MOUSEMOTION: #MOUSEMOTION
                    
                    for button in self.buttonList:                        
                        if self.getHotspot(button).collidepoint(event.pos):
                            button.Hover()
                        
                        else:
                            button.clearHover()
                        
                        
                    
                    #self.moveMenu(None, event.rel)

                return True
            
            else:
                #since we're surely not over a button, clear the state
                self.clearAllButtonState()
                #
                

                
        #We didn't want this event. Return False and the event class will
        #continue with it

        if event.type == VIDEORESIZE:
            #resize menus if they're docked
            #check if floating menus are off screen, if so move them visible

            
            self.resize(event.size)
            self.gv.console.log("MENU: Saw a resize event %s" % event)
            #don't return true, we don't want to swallow this event

            
            
        return False
    
    def clearAllButtonState(self):        
        for button in self.buttonList:
            button.reset()
            
    def getHotspot(self, button):
        temp = button.getRect().move(self.rect.topleft)
        
        return temp

    def getButtonList(self):
        return self.buttonList[:]

    def disableButton(self, button):

        button.disable()        

    def enableButton(self, button):

        button.enable()
        
            
    def remove(self):
        self.unregisterForEvents()
        self.background = None
        for button in self.buttonList:
            button.remove()
            del button
        

class button:
    def __init__(self, gv, size, position, functionToCall, name, \
                 imageNormal, imageHover, imageClicked, imageDisabled = None):
        self.gv = gv        
        self.state = NORMAL

        self.name = name
        
        self.rect = pygame.Rect(position, size)
        self.functionToCall = functionToCall
        
        self.hovered = False

        self.initImages(imageNormal, imageHover, imageClicked, imageDisabled)

    def initImages(self, imageNormal, imageHover, imageClicked, \
                                                   imageDisabled = None):
        
        self.imageNormal = self.loadImage(imageNormal)
            
        self.imageHover = self.loadImage(imageHover)

        self.imageClicked = self.loadImage(imageClicked)
        
        #if we didn't get a disabled image, we'll make one automatically
        if imageDisabled == None:
            self.imageDisabled = self.imageNormal.copy()
            self.imageDisabled.fill((200,200,200), \
                                    self.imageDisabled.get_rect(), BLEND_MULT)
        else:
            self.imageDisabled = self.loadImage(imageDisabled)

    def __repr__(self):
        return (str(self.name) + " " + str(self.rect) + " " + "State: " +\
                " " + str(self.state))
    
    def setState(self, state):    
        #print "%s -> %s" % (self, state)
        #print "\t\\->", inspect.stack()[2][3:]
        self.state = state
            
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def remove(self):
        self.rect = None
        self.imageNormal = None
        self.imageHover = None
        self.imageDisabled = None
        self.imageClicked = None

    def loadImage(self, image):
        temp = pygame.image.load(image)
        temp.convert()
        if temp.get_rect() != self.rect:
            temp = pygame.transform.smoothscale(temp, self.rect.size)
        return temp
    
    def updateButtonImages(self, imageNormal, imageHover, imageClicked, \
                           imageDisabled = None):
        
        self.initImages(imageNormal, imageHover, imageClicked, \
                        imageDisabled)        

    def draw(self):
        if self.getState() == DISABLED:
            return self.imageDisabled
        if self.hovered == True:
            return self.imageHover
        else:
            if self.getState() == NORMAL:
                return self.imageNormal
            elif self.getState() == CLICKED:
                return self.imageClicked
            self.gv.console.log("MENU: ERROR: FELL THROUGH DRAW!")

    def getRect(self):
        
        return self.rect

    def getSize(self):

        return self.rect.size
        
    def disable(self):
        #print "4 Disable %s" % self
        #if self.getState() == DISABLED:
        #    print "ALREADY DISABLED"
        self.setState(DISABLED)

    def enable(self):
        #print "button enabled"
        #if self.getState() == NORMAL:
        #    print "ALREADY ENABLED DAMMIT"
        self.setState(NORMAL)

    def clearHover(self):
        if self.getState() != DISABLED:           
            self.hovered = False
            
    def reset(self):
        if self.getState() != DISABLED:           
            self.setState(NORMAL)

    def depress(self):
        if self.getState() != DISABLED:
            #print "Button depressed"
            self.setState(CLICKED)
            self.clearHover()
        
    def clicked(self):
        if self.getState() == CLICKED:
            self.setState(NORMAL)
            self.functionToCall()
            

    def Hover(self):
        if self.getState() == NORMAL:
            self.hovered = True

    def getState(self):
        return self.state

class statusText:
    def __init__(self, gv, position, text, color):
        self.gv = gv
        self.position = position
        self.text = text
        self.color = color
        self.rect = None
        self.surface = None

        self.init()

    def init(self):
        self.updateSurface()
        self.rect = pygame.rect.Rect(self.position, self.surface.get_rect().size)

    def __repr__(self):
        return self.text

    def updateSurface(self):
        self.surface = self.gv.display.renderText(self.text, self.color)

    def getColor(self):
        return self.color

    def setColor(self):
        self.color = color
        self.updateSurface()
        
    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text
        self.updateSurface()

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position
        self.rect = pygame.rect.Rect(self.position, self.surface.get_rect().size)

    def getRect(self):
        return self.rect

    def draw(self):
        return self.surface
