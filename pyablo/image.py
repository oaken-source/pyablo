'''
This module provides functions for image handling
'''

import pygame
from pyablo.geometry import Rect


class Image(object):
    '''
    a helper class for dealing with image files
    '''
    def __init__(self, resource):
        '''
        constructor - store resource for later use
        '''
        self._resource = resource

        self._frame = pygame.image.load(self._resource)
        self._size = Rect(*self._frame.get_size())

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

    def set_colorkey(self, pos=(0, 0)):
        '''
        key out color from the image
        '''
        pos = (pos[0] % self._size.width, pos[1] % self._size.height)
        self._frame.set_colorkey(self._frame.get_at(pos))

    def split_frames(self, nframes):
        '''
        split a single image into an animation
        '''
        height = self._size.height / nframes
        def generator():
            '''
            generate split frames from the image
            '''
            i = 0
            while True:
                surface = pygame.surface.Surface((self._size.width, height))
                surface.blit(self._frame, (0, -height * i))
                surface.set_colorkey(self._frame.get_colorkey())
                i = (i + 1) % nframes
                yield surface
        return generator()
