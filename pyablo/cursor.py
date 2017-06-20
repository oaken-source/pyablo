'''
This module provides management code for the screen cursor
'''

import pygame
from pygame import Rect


class CursorOverlay(object):
    '''
    manage the pygame cursor
    '''
    def __init__(self):
        '''
        constructor - set defaults
        '''
        self._visible = True
        self._image = None

    @property
    def image(self):
        '''
        produce the image of the cursor if any
        '''
        return self._image

    @image.setter
    def image(self, value):
        '''
        set the image of the cursor
        '''
        self._image = value
        pygame.mouse.set_visible(value is None and self.visible)

    @property
    def visible(self):
        '''
        get the visibility state of the cursor
        '''
        return self._visible

    @visible.setter
    def visible(self, value):
        '''
        set the visibility state of the cursor
        '''
        self._visible = value
        pygame.mouse.set_visible(self._image is None and value)

    def draw(self, surface):
        '''
        draw the cursor unconditionally
        '''
        rect = Rect(surface.get_abs_offset(), surface.get_size())
        pos = pygame.mouse.get_pos()

        clipped = (
            min(max(pos[0], rect.left), rect.right),
            min(max(pos[1], rect.top), rect.bottom))

        if pos != clipped:
            pygame.mouse.set_pos(clipped)

        self._image.rect.topleft = clipped

        if self._visible and self._image is not None:
            self._image.do_draw(surface, self._image.rect)

