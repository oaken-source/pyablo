'''
This module provides management methods for the pygame screen
'''

import pygame

class Screen(object):
    '''
    manage the pygame screen
    '''
    def __init__(self):
        '''
        constructor - initialize pygame and create the screen
        '''
        pygame.mixer.pre_init(channels=1)
        pygame.init()

        self._fps = 60
        self._clock = pygame.time.Clock()

        self._screen = None
        self.size = (640, 480)

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
        get the current screen resolution
        '''
        return (self._screen.get_width(), self._screen.get_height())

    @size.setter
    def size(self, value):
        '''
        set the current screen resolution
        '''
        self._screen = pygame.display.set_mode(value)

    def sound(self, samples):
        '''
        play the given sound and return a handle
        '''
        sound = pygame.mixer.Sound(array=samples)
        sound.play()
        return sound

    def show(self, frame, rect, scaled=False, centered=False):
        '''
        display the given frame data on the screen
        '''
        surface = pygame.image.frombuffer(frame, rect.size, 'RGB')

        if scaled:
            rect = rect.scaled_to(self.size)
            surface = pygame.transform.smoothscale(surface, rect.size)
        if centered:
            rect = rect.centered_in(self.size)

        self._screen.blit(surface, rect.offset)

    def flip(self):
        '''
        flip the buffers and wait for the next frame
        '''
        pygame.display.flip()
        self._clock.tick(self._fps)
