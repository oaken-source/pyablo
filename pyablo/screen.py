'''
This module provides management methods for the pygame screen
'''

import pygame
from pyablo.cursor import CursorOverlay
from pyablo.debug import DebugOverlay


class Screen(object):
    '''
    manage the pygame screen
    '''
    def __init__(self, size):
        '''
        initialize pygame and most other important things
        '''
        # create a surface in native resolution as frame buffer
        self._native_surface = pygame.surface.Surface(size)

        # initialize the window in native resolution if possible
        self._window = None
        self._window_surface = None
        self.resize(size)

        # initialize the cursor
        self._cursor = CursorOverlay()
        # initialize the debug overlay
        self._debug = DebugOverlay()

    @property
    def surface(self):
        '''
        get the drawing surface in native resolution
        '''
        return self._native_surface

    @property
    def cursor(self):
        '''
        produce the cursor overlay
        '''
        return self._cursor

    @property
    def debug(self):
        '''
        produce the debug overlay
        '''
        return self._debug

    def resize(self, size):
        '''
        update the size of the window
        '''
        # try to resize the window to the given size
        try:
            self._window = pygame.display.set_mode(size)
        except pygame.error:
            self._window = pygame.display.set_mode()

        # create the a scaled subsurface for the window surface
        scaled = self._native_surface.get_rect().fit(self._window.get_rect())
        self._window_surface = self._window.subsurface(scaled)

    def flip(self):
        '''
        map the surface to the window and flip the buffers
        '''
        # scale native surface to window surface
        surface = self._native_surface.copy()
        self._debug.draw(surface)

        pygame.transform.scale(
            surface,
            self._window_surface.get_size(),
            self._window_surface)

        # swap buffers and to next frame
        pygame.display.flip()
