'''
This module provides functions for image handling
'''

import pygame
from pyablo.geometry import Rect


class Image(object):
    '''
    a helper class for dealing with image files
    '''
    def __init__(self, resource, colorkey=None, fps=None, count=None):
        '''
        constructor - store resource for later use
        '''
        self._resource = resource

        self._frame = pygame.image.load(self._resource)
        self._size = Rect(*self._frame.get_size())

        if colorkey is not None:
            pos = (colorkey[0] % self._size.width, colorkey[1] % self._size.height)
            self._frame.set_colorkey(self._frame.get_at(pos))
        if fps is not None and count is not None:
            self._fps = fps
            self._count = count
            self._animate()

    @property
    def frame(self):
        '''
        produce the image data
        '''
        return self._frame

    @property
    def size(self):
        '''
        produce the size of the image
        '''
        return self._size

    @property
    def fps(self):
        '''
        produce the fps of the anmiated image
        '''
        return self._fps

    @property
    def frames(self):
        '''
        produce the frame generator of the animated image
        '''
        return self._frames

    def _animate(self):
        '''
        split a single image into an animation
        '''
        height = self._size.height / self._count
        surface = pygame.surface.Surface((self._size.width, height))
        surface.set_colorkey(self._frame.get_colorkey())

        def frames():
            '''
            generate split frames from the image
            '''
            i = 0
            while True:
                surface.blit(self._frame, (0, -height * i))
                i = (i + 1) % self._count
                yield surface

        self._frames = frames()
