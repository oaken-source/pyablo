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
        self._enabled = False
        self.redraws = []

    @property
    def enabled(self):
        '''
        produce the visibility of the overlay
        '''
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        '''
        set the visibility of the overlay
        '''
        self._enabled = value

    def draw(self, surface):
        '''
        update the debug info on the given surface unconditionally
        '''
        if not self._enabled:
            return

        scene = "scene: %s" % type(Game.scenes.peek()).__name__
        fps = "fps: %.1f" % Game.clock.get_fps()

        label = self._font.render(scene, 1, (255, 255, 255))
        surface.blit(label, (10, 10))
        label = self._font.render(fps, 1, (255, 255, 255))
        surface.blit(label, (10, 10 + self._font.get_linesize()))

        for rect in self.redraws:
            pygame.draw.rect(surface, (0, 255, 0), rect, 1)
        self.redraws.clear()
