'''
This module provides functions for image handling
'''

import pygame
from pyablo.geometry import Rect


class Image(object):
    '''
    a helper class for dealing with image files
    '''
    def __init__(self, resource, colorkey=None):
        '''
        constructor - store resource for later use
        '''
        self._resource = resource

        self._frame = pygame.image.load(self._resource)
        self._animation = None
        self._size = Rect(*self._frame.get_size())

        if colorkey is not None:
            pos = (colorkey[0] % self._size.width, colorkey[1] % self._size.height)
            self._frame.set_colorkey(self._frame.get_at(pos))

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
        if self._animation is None:
            raise ValueError('image is not animated')
        return self._animation[0]

    @property
    def frames(self):
        '''
        produce the frame generator of the animated image
        '''
        if self._animation is None:
            raise ValueError('image is not animated')
        return self._animation[1]

    def animate(self, fps, length):
        '''
        split a single image into an animation
        '''
        height = self._size.height / length
        surface = pygame.surface.Surface((self._size.width, height))
        surface.set_colorkey(self._frame.get_colorkey())

        def frames():
            '''
            generate split frames from the image
            '''
            i = 0
            while True:
                surface.blit(self._frame, (0, -height * i))
                i = (i + 1) % length
                yield surface

        self._animation = (fps, frames())
