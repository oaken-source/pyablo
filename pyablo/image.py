'''
This module provides functions for image handling
'''

import itertools
import pygame
from pygame import Rect
from pyablo.scene import SceneObject
from pyablo.game import Game


class Image(SceneObject):
    '''
    a helper class for dealing with image files
    '''
    def __init__(self, resource, colorkey=None):
        '''
        constructor - store resource for later use
        '''
        super(Image, self).__init__()

        self._resource = resource

        self.surface = pygame.image.load(self._resource).convert()
        self.rect = self.surface.get_rect()

        # key out given color
        if colorkey is not None:
            pos = (colorkey[0] % self.rect.width, colorkey[1] % self.rect.height)
            self.surface.set_colorkey(self.surface.get_at(pos))


class SolidColorImage(SceneObject):
    '''
    a helper class for solid color rects
    '''
    def __init__(self, size, color=(0, 0, 0)):
        '''
        constructor
        '''
        super(SolidColorImage, self).__init__()

        self.surface = pygame.surface.Surface(size)
        self.surface.fill(color)
        self.rect = Rect((0, 0), size)


class AnimatedImage(Image):
    '''
    a base class for dealing with animated images
    '''
    def __init__(self, resource, colorkey, fps, count):
        '''
        constructor
        '''
        super(AnimatedImage, self).__init__(resource, colorkey)

        self._fps = fps
        self._elapsed = 0

        # split into animated frames
        self._full_height = self.rect.height
        self._full_surface = self.surface

        self.rect.height //= count
        self._frames = itertools.cycle(
            self._full_surface.subsurface(0, y, *self.rect.size)
            for y in range(0, self._full_height, self.rect.height))

        self.surface = next(self._frames)

    def update(self):
        '''
        update the animated image on screen
        '''
        self._elapsed += Game.clock.get_time()
        while self._elapsed >= 1000.0 / self._fps:
            self._elapsed -= 1000.0 / self._fps
            self.surface = next(self._frames)
