'''
This module provides management methods for the pygame screen
'''

import sys
import pygame


class MetaGame(type):
    '''
    the metaclass for the game class - this implements classproperties on Game
    '''
    @property
    def clock(cls):
        '''
        produce the game clock
        '''
        return cls._clock

    @property
    def screen(cls):
        '''
        get the game screen
        '''
        return cls._screen

    @screen.setter
    def screen(cls, value):
        '''
        set the game screen
        '''
        cls._screen = value

    @property
    def scenes(cls):
        '''
        get the game scene stack
        '''
        return cls._scenes

    @scenes.setter
    def scenes(cls, value):
        '''
        set the game scene stack
        '''
        cls._scenes = value


class Game(object, metaclass=MetaGame):
    '''
    manage the pygame screen
    '''
    _clock = None
    _screen = None
    _scenes = None

    _fps_unlocked = False
    _max_fps = 0

    @classmethod
    def init(cls, title='pygame', max_fps=0):
        '''
        initialize pygame and some other important things
        '''
        # initialize pygame
        pygame.mixer.pre_init(channels=1)
        pygame.init()

        # set window caption
        pygame.display.set_caption(title)

        # initialize game clock
        cls._clock = pygame.time.Clock()
        cls._max_fps = max_fps

    @classmethod
    def main(cls):
        '''
        start the main loop of the game
        '''
        while cls._scenes:
            # get the scene on top of the scene stack
            scene = cls._scenes.peek()

            try:
                # process events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.VIDEORESIZE:
                        cls.screen.resize(event.dict['size'])
                    elif event.type == pygame.KEYUP and event.key == pygame.K_HASH:
                        cls.screen.debug.enabled = not cls.screen.debug.enabled
                    elif event.type == pygame.KEYUP and event.key == pygame.K_EXCLAIM:
                        cls._fps_unlocked = not cls._fps_unlocked
                    else:
                        scene.on_event(event)

                # update the scenegraph objects and redraw
                scene.update()

                # flip the buffers at the given maximum refresh rate
                cls.screen.flip()
                cls._clock.tick(0 if cls._fps_unlocked else cls._max_fps)
            except StopIteration:
                Game.scenes.pop()

    @classmethod
    def quit(cls):
        '''
        quit the game
        '''
        sys.exit(0)
