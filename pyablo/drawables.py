'''
This module provides drawables used in pyablo scenes
'''

import itertools
import av
import pygame
from pygame import Rect
from pyablo.game import Game


class Drawable(object):
    '''
    a node in the scene graph
    '''
    def __init__(self):
        '''
        constructor
        '''
        self._rect = Rect(0, 0, 0, 0)
        self._children = []

        self.transparent = False
        self._surface = None
        self.redraw = False
        self._redraw_rects = []
        self.parent = None

    @property
    def rect(self):
        '''
        produce the rect of the sceneobject
        '''
        return self._rect

    @rect.setter
    def rect(self, value):
        '''
        set the rect of the sceneobject
        '''
        self._rect = value

    def add_child(self, child, pos=(0, 0)):
        '''
        add a child sceneobject
        '''
        child.rect.topleft = pos
        child.parent = self
        child.redraw = True

        self._children.append(child)

    def on_update(self):
        '''
        update callback
        '''
        pass

    def update(self):
        '''
        update method - advance time and calculate redraw and dirty regions
        '''
        self.on_update()

        dirty = []
        for child in self._children:
            dirty.extend(child.update())

        if self.redraw:
            dirty = [self.rect]

        self._redraw_rects = dirty
        return dirty if self.transparent else []

    def do_draw(self, surface, rect):
        '''
        default draw callback
        '''
        area = rect.copy()
        area.topleft = (area.left - self.rect.left, area.top - self.rect.top)
        surface.blit(self._surface, rect.topleft, area)
        self.redraw = False
        Game.screen.debug.redraws.append(rect)

    def draw(self, surface, rects):
        '''
        redraw method - do the actual redrawing into the given rects
        '''
        for rect in self._redraw_rects:
            self.do_draw(surface, rect)

        for child in self._children:
            redraw = [rect.clip(child.rect) for rect in rects if rect.collideswith(child.rect)]
            child.draw(surface, redraw)


class Image(Drawable):
    '''
    a helper class for dealing with image files
    '''
    def __init__(self, resource, colorkey=None):
        '''
        constructor - store resource for later use
        '''
        super(Image, self).__init__()

        self._resource = resource

        self._surface = pygame.image.load(self._resource).convert()
        self.rect = self._surface.get_rect()

        # key out given color
        if colorkey is not None:
            pos = (colorkey[0] % self.rect.width, colorkey[1] % self.rect.height)
            self._surface.set_colorkey(self._surface.get_at(pos))
            self.transparent = True


class AnimatedImage(Image):
    '''
    a base class for dealing with animated images
    '''
    def __init__(self, resource, colorkey, fps, count):
        '''
        constructor
        '''
        super(AnimatedImage, self).__init__(resource, colorkey)

        self._fps = fps
        self._elapsed = 0

        # split into animated frames
        self._full_height = self.rect.height
        self._full_surface = self._surface

        self.rect.height //= count
        self._frames = itertools.cycle(
            self._full_surface.subsurface(0, y, *self.rect.size)
            for y in range(0, self._full_height, self.rect.height))

        self._surface = next(self._frames)

    def on_update(self):
        '''
        update the animated image on screen
        '''
        self._elapsed += Game.clock.get_time()
        while self._elapsed >= 1000.0 / self._fps:
            self._elapsed -= 1000.0 / self._fps
            self._surface = next(self._frames)
            self.redraw = True


class Video(Drawable):
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

        self._surface = next(self._frames)
        self.rect = self._surface.get_rect()

    def on_update(self):
        '''
        update the video on screen
        '''
        if self._elapsed == 0:
            self._audio.play()

        self._elapsed += Game.clock.get_time()
        if self._elapsed >= 1000.0 / self._fps:
            self._elapsed -= 1000.0 / self._fps
            self._surface = next(self._frames)
            self.redraw = True
