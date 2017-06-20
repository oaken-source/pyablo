'''
This module is the entry point of pyablo
'''

from pyablo.resources import Resources
from pyablo.screen import Screen, SceneStack
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
    Game.screen.debug.enabled = True

    # initialize the scene stack
    Game.scenes = SceneStack('pyablo.scenes')
    Game.scenes.push('MainMenuScene')
    Game.scenes.push('IntroSplashScene')
    Game.scenes.push('CutScene', args=('intro_cinematic.smk',))
    Game.scenes.push('CutScene', args=('intro_logos.smk',))

    # start the main loop
    Game.main()


if __name__ == '__main__':
    main()
