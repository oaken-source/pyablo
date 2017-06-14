'''
This module is the entry point of pyablo
'''

from pyablo.resources import Resources
from pyablo.screen import Screen
from pyablo.scene import SceneStack
from pyablo.game import Game


def main():
    '''
    pyablo's main function
    '''
    # initialize the game resources
    Resources.load('resources/diabdat.mpq')

    # initialize the game
    Game.init('Diablo', max_fps=60)

    # initialize the screen
    Game.screen = Screen((640, 480))
    Game.screen.cursor.image = Resources.open('cursor.pcx')
    Game.screen.debug.visible = True

    # initialize the scene stack
    Game.scenes = SceneStack('pyablo.scenes')
    Game.scenes.push('main_menu')
    Game.scenes.push('intro_splash')
    Game.scenes.push('intro_cinematic')
    Game.scenes.push('intro_logos')

    # start the main loop
    Game.main()


if __name__ == '__main__':
    main()
