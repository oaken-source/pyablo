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
