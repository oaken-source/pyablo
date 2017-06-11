'''
This module provides methods for video handling
'''

import av
import pygame
from pyablo.geometry import Rect


class Video(object):
    '''
    a helper class for dealing with cutscenes
    '''
    def __init__(self, resource, fps):
        '''
        constructor - decode audio and video
        '''
        self._resource = resource
        self._fps = fps

        # decode the audio stream
        self._resource.seek(0)
        data = av.open(self._resource)

        fifo = av.AudioFifo()
        for frame in data.decode(audio=0):
            fifo.write(frame)

        resampler = av.AudioResampler(format='s16p', layout='mono')
        self._audio = pygame.mixer.Sound(
            resampler.resample(fifo.read()).to_nd_array()[0])

        # decode the video stream
        self._resource.seek(0)
        data = av.open(self._resource)

        self._size = Rect(data.streams.video[0].format.width, data.streams.video[0].format.height)
        self._frames = (
            pygame.image.frombuffer(
                frame.to_nd_array(format='rgb24'),
                self._size.size,
                'RGB')
            for frame in data.decode(video=0))

    @property
    def fps(self):
        '''
        produce the fps of the video
        '''
        return self._fps

    @property
    def frames(self):
        '''
        a generator for the frames of the video as numpy arrays
        '''
        return self._frames

    @property
    def audio(self):
        '''
        produce the audio track of the video as mono numpy array
        '''
        return self._audio

    @property
    def size(self):
        '''
        produce the size of the video
        '''
        return self._size
