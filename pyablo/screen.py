'''
This module provides management methods for the pygame screen
'''

import sys
import pygame
from pyablo.geometry import Rect


class Screen(object):
    '''
    manage the pygame screen
    '''
    def __init__(self, title='pygame'):
        '''
        constructor - initialize pygame and create the screen
        '''
        pygame.mixer.pre_init(channels=1)
        pygame.init()
        pygame.display.set_caption(title)

        self._fps = 60
        self._clock = pygame.time.Clock()

        self._native = (640, 480)

        self._surface = pygame.surface.Surface(self._native)
        self._window = None
        self.size = self._native

    @property
    def fps(self):
        '''
        get the current fps limit
        '''
        return self._fps

    @fps.setter
    def fps(self, value):
        '''
        set the current fps limit
        '''
        self._fps = value

    @property
    def size(self):
        '''
        get the current window resolution
        '''
        return self._window.get_size()

    @size.setter
    def size(self, value):
        '''
        set the current window resolution
        '''
        self._window = pygame.display.set_mode(value)

    def play(self, video):
        '''
        play the given video
        '''
        saved_fps = self.fps
        self.fps = video.fps

        video.audio.play()

        def handle_event(event):
            '''
            additional event callbacks
            '''
            if (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE
                    or event.type == pygame.MOUSEBUTTONDOWN):
                pygame.mixer.stop()
                raise StopIteration

        try:
            for frame in video.frames:
                self.process_events(handle_event)

                size = self._surface.get_size()
                rect = Rect(*video.size.size).scaled_to(size).centered_in(size)

                surface = pygame.transform.smoothscale(frame, rect.size)

                self.show(surface, rect.offset)
                self.flip()
        except StopIteration:
            pass

        self.fps = saved_fps

    def show(self, surface, pos=(0, 0)):
        '''
        display the given frame data on the screen
        '''
        self._surface.blit(surface, pos)

    def process_events(self, callback=None):
        '''
        process events in the main loop
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.VIDEORESIZE:
                self.size = event.dict['size']
            elif callback is not None:
                callback(event)

    def flip(self):
        '''
        map the surface to the window and flip the buffers
        '''
        size = self._window.get_size()
        rect = Rect(*self._surface.get_size()).scaled_to(size).centered_in(size)

        surface = pygame.transform.smoothscale(self._surface, rect.size)
        self._window.blit(surface, rect.offset)

        pygame.display.flip()
        self._clock.tick(self._fps)
