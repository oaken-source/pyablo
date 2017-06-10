'''
This module provides management methods for the pygame screen
'''

import pygame
from pyablo.cursor import Cursor
from pyablo.geometry import Rect
from pyablo.scene import SceneStack


MAX_FPS = 60


class Screen(object):
    '''
    manage the pygame screen
    '''
    def __init__(self, title='pygame'):
        '''
        constructor - initialize pygame and create the screen
        '''
        pygame.mixer.pre_init(channels=1)
        pygame.init()
        pygame.display.set_caption(title)

        self._clock = pygame.time.Clock()

        self._size = (640, 480)
        self._surface = pygame.surface.Surface(self._size)
        self._window = pygame.display.set_mode(self._size)

        self._scenes = SceneStack(self)
        self._cursor = Cursor()

    @property
    def size(self):
        '''
        get the current window resolution
        '''
        return self._size

    @property
    def clock(self):
        '''
        get the screen clock
        '''
        return self._clock

    @property
    def cursor(self):
        '''
        get the window cursor
        '''
        return self._cursor

    @property
    def scenes(self):
        '''
        get the scene stack
        '''
        return self._scenes

    def _flip(self):
        '''
        map the surface to the window and flip the buffers
        '''
        surface = self._surface.copy()
        self._cursor.update(surface)

        native = self._surface.get_size()
        window = self._window.get_size()
        rect = Rect(*native).scaled_to(window).centered_in(window)

        surface = pygame.transform.smoothscale(surface, rect.size)
        self._window.blit(surface, rect.offset)

        pygame.display.flip()
        self._clock.tick(MAX_FPS)

    def blit(self, surface, pos=(0, 0)):
        '''
        display the given frame data on the screen
        '''
        self._surface.blit(surface, pos)

    def start(self):
        '''
        seize control of the main loop
        '''
        while True:
            scene = self._scenes.peek()

            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.VIDEORESIZE:
                        self._window = pygame.display.set_mode(event.dict['size'])
                    scene.on_event(event)

                scene.update(self)

                self._flip()
            except StopIteration:
                self._scenes.pop()
