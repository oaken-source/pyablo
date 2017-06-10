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

    # initialize the screen
    screen = Screen('Diablo')
    screen.scenes.load('pyablo.scenes')

    # initialize the cursor
    cursor = Resources.open('cursor.pcx', colorkey=(0, -1))
    screen.cursor.image = cursor

    # load the first scene
    screen.scenes.push('main_menu')
    screen.scenes.push('intro_splash')
    screen.scenes.push('intro_cinematic')
    screen.scenes.push('intro_logos')

    # start the main loop
    screen.start()


if __name__ == '__main__':
    main()
