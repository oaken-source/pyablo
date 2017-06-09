'''
This module provides management code for the screen cursor
'''

import pygame


class Cursor(object):
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
    def visible(self):
        '''
        produce the visibility state of the cursor
        '''
        return self._visible

    @visible.setter
    def visible(self, value):
        '''
        set the visibility state of the cursor
        '''
        self._visible = value
        pygame.mouse.set_visible(self._image is None and value)

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

        if value is not None:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(self.visible)

    def update(self, surface):
        '''
        update the cursor (software or hardware)
        '''
        if self.image is not None and self.visible:
            surface.blit(self.image.frame, pygame.mouse.get_pos())
