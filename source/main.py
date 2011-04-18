#!/usr/bin/env python
import display, events, console, globalvars, flippy_pad, pygame

#testing fullscreen
#pygame.display.init()
#size  = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

size = width, height = 640, 480

framerate = 60

#Since it's going to be used a ton, short name gv for global variable access
#TODO add in config.ini class to fill in globalvars


gv = globalvars.globalvars(size, framerate)

gv.version = "Flippy Pad 0.3"

#should toss time in a class eventually
gv.Clock = pygame.time.Clock()
gv.Clock.tick()


displayinstance = display.display(gv)
consoleinstance = console.console(gv)
eventsinstance = events.events(gv)
flippy = flippy_pad.flippy(gv)



#gv.console.log("MAIN: TEST LOG ENTRY - WEE!")


while 1:
    
    eventsinstance.handleEvents()
    flippy.update()

    consoleinstance.begin()
    
    displayinstance.paint()
    gv.Clock.tick(gv.framerate)
