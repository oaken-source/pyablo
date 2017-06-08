'''
This module provides methods for cutscene handling and playback
'''

import av
import pygame
from pyablo.util import Rect, QuitGame


class Cutscene(object):
    '''
    a helper class for dealing with cutscenes
    '''
    def __init__(self, resource):
        '''
        constructor - store the given resource for later use
        '''
        self._resource = resource
        self._size = None

    def _frames(self):
        '''
        a generator for the frames of the video as numpy arrays
        '''
        self._resource.seek(0)
        data = av.open(self._resource)
        self._size = Rect(data.streams.video[0].format.width, data.streams.video[0].format.height)
        for frame in data.decode(video=0):
            yield frame.to_nd_array(format='rgb24')

    def _audio(self):
        '''
        produce the audio track of the video as mono numpy array
        '''
        fifo = av.AudioFifo()
        data = av.open(self._resource)
        for frame in data.decode(audio=0):
            fifo.write(frame)

        resampler = av.AudioResampler(format='s16p', layout='mono')
        return resampler.resample(fifo.read()).to_nd_array()[0]

    def play(self, screen):
        '''
        play the cutscene in the given screen
        '''
        screen.fps = 15
        sound = screen.sound(self._audio())
        for frame in self._frames():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise QuitGame()
                elif event.type == pygame.VIDEORESIZE:
                    screen.size = event.dict['size']
                elif event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    sound.stop()
                    return

            surface = pygame.image.frombuffer(frame, self._size.size, 'RGB')
            screen.show(surface, scaled=True, centered=True)
            screen.flip()
