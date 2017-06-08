'''
This module is the entry point of pyablo
'''

import sys
import pygame
from pyablo.resources import Resources
from pyablo.video import Cutscene
from pyablo.screen import Screen
from pyablo.util import QuitGame


def main():
    '''
    pyablo's main function
    '''
    # initialize the game resources
    Resources.init('resources/diabdat.mpq')

    # initialize pygame
    screen = Screen()

    # play intro
    Cutscene(Resources.open('intro_logos.smk')).play(screen)
    Cutscene(Resources.open('intro_cinematic.smk')).play(screen)

    # display splash screen
    Screen.fps = 30
    frame = pygame.image.load(Resources.open('intro_splash.pcx')).convert()
    screen.show(frame, scaled=True, centered=True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.VIDEORESIZE:
                screen.size = event.dict['size']

        screen.show(frame, scaled=True, centered=True)
        screen.flip()

    raise NotImplementedError('it ends here')


def _main():
    '''
    a wrapper around main to catch QuitGame exceptions
    '''
    try:
        main()
    except QuitGame:
        return 0


if __name__ == '__main__':
    _main()
