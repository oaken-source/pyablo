'''
This module provides methods for video handling
'''

import av
import pygame
from pyablo.scene import SceneObject
from pyablo.game import Game


class Video(SceneObject):
    '''
    a helper class for dealing with cutscenes
    '''
    def __init__(self, resource, fps):
        '''
        constructor - decode audio and video
        '''
        super(Video, self).__init__()

        self._resource = resource
        self._fps = fps
        self._elapsed = 0

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

        self._frames = (
            pygame.image.frombuffer(
                frame.to_nd_array(format='rgb24'),
                (frame.width, frame.height),
                'RGB')
            for frame in data.decode(video=0))

        self.surface = next(self._frames)
        self.rect = self.surface.get_rect()

    def update(self):
        '''
        update the video on screen
        '''
        if self._elapsed == 0:
            self._audio.play()

        self._elapsed += Game.clock.get_time()
        if self._elapsed >= 1000.0 / self._fps:
            self._elapsed -= 1000.0 / self._fps
            self.surface = next(self._frames)
