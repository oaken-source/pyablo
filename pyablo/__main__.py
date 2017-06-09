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
    screen.fps = 20
    screen.cursor.visible = False

    # play intro
    screen.play(Resources.open('intro_logos.smk'))
    screen.play(Resources.open('intro_cinematic.smk'))

    # display splash screen
    splash = Resources.open('intro_splash.pcx')
    logo = Resources.open('logo_flames_large.pcx')
    logo.set_colorkey()
    animation = logo.split_frames(15)
    while True:
        screen.show(splash.frame)
        screen.show(next(animation), (45, 182))
        screen.process_events()
        screen.flip()

    # enable the cursor
    screen.cursor.image = Resources.open('cursor.pcx')
    screen.cursor.image.set_colorkey((0, -1))
    screen.cursor.visible = True

    raise NotImplementedError('it ends here')


if __name__ == '__main__':
    main()
