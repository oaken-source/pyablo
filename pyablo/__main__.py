'''
This module is the entry point of pyablo
'''

from pyablo.resources import Resources
from pyablo.screen import Screen


def main():
    '''
    pyablo's main function
    '''
    # initialize the game resources
    Resources.load('resources/diabdat.mpq')

    # initialize pygame
    screen = Screen('Diablo')
    screen.fps = 30

    # play intro
    screen.play(Resources.open('intro_logos.smk'))
    screen.play(Resources.open('intro_cinematic.smk'))

    # display splash screen
    screen.show(Resources.open('intro_splash.pcx').frame)

    while True:
        screen.process_events()
        screen.flip()

    raise NotImplementedError('it ends here')


if __name__ == '__main__':
    main()
