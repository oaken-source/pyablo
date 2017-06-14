'''
This module provides management code for the screen cursor
'''

import pygame


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
        if self._visible and self._image is not None:
            surface.blit(self._image.surface, pygame.mouse.get_pos())
