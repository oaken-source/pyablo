'''
This module is the entry point of pyablo
'''

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

    # play blizzard logo
    Cutscene(Resources.open('File00002910.smk')).play(screen)
    # play opening cinematics
    Cutscene(Resources.open('File00001475.smk')).play(screen)

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
