import pygame, sys
from pygame.locals import *

class console:
    
    def __init__(self, globalvariables, bgcolor=(10,10,150)):
        self.gv = globalvariables
        self.gv.registerInstance("Console", self)
        self.display = self.gv.display
        
        self.size = self.gv.size
        self.height = self.gv.size[1]
        self.width = self.gv.size[0]

        #TODO pull this into global vars
        self.bgcolor = bgcolor
        self.input = u""
        self.output = []
        self.outputcolor = (245,245,155)
        self.textposition = [4,4]
        self.itemslist = [()]
        self.time = 0
        self.blink = True
        self.error = ()
        self.inputhistory = []
        self.inputhistoryitemnumber = 0
        self.isAnimating = False
        self.POSITION = (0,0)
        self.animationProgress = None
        self.animationSpeed = 5
        self.init()


    def init(self):
        #call when first setting up and when resizing
        self.backSurface = pygame.surface.Surface((self.gv.size))        
        self.backSurface.fill(self.bgcolor)
        self.backSurface.set_alpha(128)
        self.textSurface = pygame.surface.Surface((self.gv.size), SRCALPHA)
        self.textSurface.fill((255,255,255,0))
        
    #no longer needed, moved Clock to a global variable
    def begin(self):
        '''
        Pass in last frame time in ms for cursor blinking goodness.
        '''
        self.time += self.gv.Clock.get_time()

        self.draw()
        
    def getKeys(self, event):
        if self.gv.consoleenabled == True:
            if event.type == KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if pygame.key.get_mods() & KMOD_RCTRL or \
                       pygame.key.get_mods() & KMOD_LCTRL:
                        self.input = u""
                    self.input = self.input[:-1]

                elif event.key == pygame.K_TAB:
                    #eventually, pass this to console for autocompletion
                    pass
                elif event.key == pygame.K_BACKQUOTE:
                    pass
                elif event.key == pygame.K_RETURN:
                    if len(self.input.strip()) != 0:
                        self.parseinput(self.input)
                        
                        
                elif event.key == pygame.K_UP:
                    if self.inputhistoryitemnumber > 0:
                        self.inputhistoryitemnumber += -1
                        self.input = self.inputhistory[self.inputhistoryitemnumber]
                        #print self.inputhistoryitemnumber
                    
                elif event.key == pygame.K_DOWN:
                    if self.inputhistoryitemnumber < len(self.inputhistory) - 1:
                        self.inputhistoryitemnumber += 1
                        self.input = self.inputhistory[self.inputhistoryitemnumber]
                else:
                    self.input += str(event.unicode)
            
    def parseinput(self, text):
        '''
        give the console text to execute
        '''
        
        if text == u"\\exit" or \
           text == u"\\quit":
            sys.exit()

        #output from commands, actions too
            
        #if text[:1] != u"\\":
        #    self.output.append(text + u"?")
        #    self.output.append(u"Well, that did nothing.")
#            self.output.append(u"Try a command. Commands start with backslash, sparky.")

        if text[:4] == u"\\set":            
            self.setcommand(text[4:])

        else:
        #elif text[:5] == u"\\eval":
            
            try:
                temp = eval(text)
                #temp = eval("print 'i'")
                if temp == None:
                    self.output.append("OK")
                else:
                    self.output.append(str(temp))
                
            except:
                self.output.append(u"Cannot evaluate Python expression " + text)                

                
        self.inputhistory.append(text)
        self.inputhistoryitemnumber = len(self.inputhistory)
        self.input = u""

    def textout(self, text, color, enter=True):
        '''
        Add a textual string to the console buffer. Pass enter=True to add
        a newline after the text.
        '''

        #TODO WTF is this shit? Why did I do this this way?
        #the buffer and it's presentation shouldn't be intrisnic here
        #i don't know why I avoided adding \n to the strings here. wtf.


        
        #print "Text out: %s" % text        
        self.itemslist.append((text, color, enter))

    def log(self, text):
        '''
        Same as textout, but for easy logging capability.
        '''
        self.output.append(text)
        
            
    def setcommand(self, command):
        command = command.strip()
        
        if len(command) < 5:
            self.output.append(u"WTF. I can't set nothing to nothing.")
        else:
            #self.output.append(u"Requested to set: %s" % command)

            try:
                #TODO this sholud be abstracted to use a function
                if command[:9] == u"framerate":                                    
                    self.gv.framerate = int(command[10:])
                    self.output.append(u"Framerate set to %i" % self.gv.framerate)                    
                elif command[:7] == u"showfps":
                    self.gv.showFPS = bool(int(command[8:]))
                else:
                    self.output.append(u"WTF. I can't do that.")
            except ValueError:
                #print "Command error."
                self.output.append(u"WTF. I can't do that.")
                
        #this should use exceptions instead DONE
    def enable(self):
        self.gv.consoleenabled = not self.gv.consoleenabled
        #print "Console: %s" % self.gv.consoleenabled
        if self.gv.consoleenabled == True:
            #todo: some simple animations in a class?
            self.isAnimating = True

    def handleAnimation(self):
        #TODO change to time-invariant version when I get a chance.
        #not particularly critical
        
        #avoid some complicated if elses by using the exception handler
        try:
            self.animationProgress += 1
        except:
            self.animationProgress = 0

        if self.animationProgress < self.animationSpeed:
            #only screw with the vertical position
            self.POSITION = (0, -self.gv.height + ((self.gv.height / self.animationSpeed) \
                             * self.animationProgress))
            #print self.POSITION
        else:
            self.POSITION = (0,0)
            self.animationProgress = None
            self.isAnimating = False
            
        
        
    def draw(self):
        '''
        Send commands to draw the console as we've set it up for this frame.
        '''
        
        #todo: let's animate this into view.
            #todo: which means we need to blit to a surface DONE
        #todo: parse \n's here, wtf was I doing before
        
        
        if self.gv.consoleenabled == True:
            #duplicate the standard background surface we've already set up
            backgroundSurface = self.textSurface.copy()
            
            
            
            #remember to draw bgcolor and size of bg - skip for now
            #remember to draw self.input text after > DONE
            #remember to draw blinking caret
            #remember to add the contents of self.input first, if any DONE

            #----------
            #TODO: this is being done once per frame. it's not changing, ever,
            #i should initialize the surface once at runtime and then just reuse
            #it
            #----------
            
            #temp = pygame.surface.Surface((self.gv.size))
            #temp.fill(self.bgcolor)
            #temp.set_alpha(128)
            
            #self.display.drawitem(temp, temp.get_rect(), self.gv.zorder_ui)
            
            
            self.itemslist.append((u">", (255,255,255), False))
            self.itemslist.append((self.input, (255,255,255), False))
            
            ###
            ###Caret
            ###
            
            if self.time > self.gv.blinkrate:
                self.blink = not self.blink
                self.time = 0

            if self.blink == True:
                #RGBA see below
                self.itemslist.append((u"|", (255,255,255), True))
            else:
                #RGBA - since I don't know the bgcolor, just paint nothing.wee!
                #wrong. this doesn't work.wtf
                self.itemslist.append((u"|", self.bgcolor, True))

            ###
            ###
            ###

            if len(self.output) > 23:
                #should be set to maxrows eventually. query that on __init__()
                self.output = self.output[-23:]
                #change to 24 once display draws FPS

            for item in self.output:
                self.itemslist.append((item, self.outputcolor, True))

            #Toss version string at the top
            self.itemslist.insert(0, (self.gv.version, (255,0,0), True))
            
            for item in self.itemslist:
                if item != ():

                    #let's blit this instead to a separate surface, which we
                    #can do magic to
                    #render the text, get back a surface
                    temp = self.display.renderText(item[0], \
                                                   item[1])

                    #now spit that on our combined console surface
                    backgroundSurface.blit(temp, self.textposition)

                    


                    

                    #temp = self.display.drawtext(item[0], \
                    #                             item[1], \
                    #                             self.textposition, \
                    #                             self.gv.zorder_aboveui)
                    #temp is now a rect that was the size of the text we sent

                    #temp = pygame.surface.Blit(

                    if item[2] == True:
                        self.textposition[1] += temp.get_rect().height
                        self.textposition[0] = 4
                    else:                    
                        self.textposition[0] += temp.get_rect().width

                
            self.textposition = [4,4]
            self.itemslist = [()]

            #very last step is to blit the newly made backgroundSurface
            #self.POSITION will be set by the animation handler
            if self.isAnimating == True:
                self.handleAnimation()
            self.display.drawitem(self.backSurface, self.POSITION, self.gv.zorder_aboveui)
            self.display.drawitem(backgroundSurface, self.POSITION, self.gv.zorder_aboveui)
            
            backgroundSurface = None
            

            #do this in display.longestwidth?
            #get max width at startup and never check again
            #same with number of characters height
            #
            #
#    def findlongesttextthatfitsscreenwidth(text):
#        
#        while UItext.size(text)[0] > width:
#            pass
#        return numcharacters

                
                #timesinceblink += + Clock.get_time()
                
                #if len(line) > 0:
                #    paintconsole(line)            
                    
                #if timesinceblink > blinkrate:
                #    blink = not blink
                #    timesinceblink = 0
                #if blink == True:
                    
                #    screen.blit(UItext.render(u"|", 1, (255,255,255)), UIRect)
                    
                #else:
                       
                #    screen.blit(UItext.render(u"|", 1, (0,0,0)), UIRect)

        #while len(input) > 0:
            
            #if UItext.size(input)[0] > width - 4:
            #        numcharacters = findlongesttextthatfitsscreenwidth(input)
                    
                    #multiline format fun
                    
                    #self.display.showtext((input, 1, (255,255,255)))
                    #screen.blit(temp, UIRect)
                    #UIRect.right +=+ temp.get_rect().width
                    
                    #print "Multiline input. Jerk."          
