'''
This module provides some debug information in an overlay
'''

import pygame
from pyablo.game import Game


class DebugOverlay(object):
    '''
    a drawable with debug information
    '''
    def __init__(self):
        '''
        constructor
        '''
        self._font = pygame.font.SysFont("monospace", 15)
        self._visible = False
        self._dirty = []

    @property
    def visible(self):
        '''
        produce the visibility of the overlay
        '''
        return self._visible

    @visible.setter
    def visible(self, value):
        '''
        set the visibility of the overlay
        '''
        self._visible = value

    @property
    def dirty_frames(self):
        '''
        produce the list of dirty frames
        '''
        return self._dirty

    def draw(self, surface):
        '''
        update the debug info on the given surface unconditionally
        '''
        if not self._visible:
            return

        fps = "fps: %.1f" % Game.clock.get_fps()
        label = self._font.render(fps, 1, (255, 255, 255))
        surface.blit(label, (10, 10))

        for dirty in self._dirty:
            pygame.draw.rect(surface, (0, 255, 0), dirty, 1)
        self._dirty.clear()
