'''
This module provides classes to manage the scene graph stack
'''

import importlib
from inspect import getmembers, isfunction
import pygame
from pyablo.geometry import Rect


class SceneStack(object):
    '''
    custom stack class for scenes
    '''
    def __init__(self, screen):
        '''
        constructor
        '''
        self._screen = screen
        self._scenedir = dict()
        self._stack = list()

    def load(self, module):
        '''
        load scenes from a module
        '''
        mod = importlib.import_module(module)
        for (name, value) in getmembers(mod, isfunction):
            self._scenedir[name] = value

    def push(self, value):
        '''
        push to the stack and invoke callbacks
        '''
        self._screen.clear()

        scene = self._scenedir[value](self._screen)
        scene.screen = self._screen

        if self._stack:
            self._stack[-1].on_pause()
        self._stack.append(scene)
        scene.on_resume()

    def peek(self):
        '''
        peek on the stack
        '''
        return self._stack[-1]

    def pop(self):
        '''
        pop from the stack and invoke callbacks
        '''
        self._screen.clear()

        scene = self._stack.pop()
        scene.on_stop()
        if self._stack:
            self._stack[-1].on_resume()
        return scene

    def __bool__(self):
        '''
        produce a boolean representation of the scene stack
        '''
        return bool(self._stack)


class Scene(object):
    '''
    a scene in the scene stack
    '''
    def __init__(self, scenegraph, **kwargs):
        '''
        constructor
        '''
        self._screen = None

        self._scenegraph = scenegraph
        self._callbacks = {k: v for (k, v) in kwargs.items() if k.startswith('on_')}
        self._properties = {k: v for (k, v) in kwargs.items() if not k.startswith('on_')}

        self._start_time = pygame.time.get_ticks()

    @property
    def screen(self):
        '''
        produce the screen reference
        '''
        return self._screen

    @screen.setter
    def screen(self, screen):
        '''
        set the screen reference
        '''
        self._screen = screen

    def on_event(self, event):
        '''
        invoke the event callback if present
        '''
        if 'on_event' in self._callbacks:
            self._callbacks['on_event'](self, event)

    def on_pause(self):
        '''
        invoke the pause callback if present
        '''
        if 'on_pause' in self._callbacks:
            self._callbacks['on_pause'](self)

    def on_resume(self):
        '''
        invoke the resume callback if present
        '''
        self._screen.cursor.visible = self._properties.get('cursor_visible', True)

        if 'on_resume' in self._callbacks:
            self._callbacks['on_resume'](self)

    def on_update(self):
        '''
        invoke the update callback if present
        '''
        if 'on_update' in self._callbacks:
            self._callbacks['on_update'](self)

    def on_stop(self):
        '''
        invoke the stop callback if present
        '''
        if 'on_stop' in self._callbacks:
            self._callbacks['on_stop'](self)

    @property
    def start_time(self):
        '''
        produce the start time
        '''
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        '''
        set a custom start time
        '''
        self._start_time = value

    @property
    def elapsed_time(self):
        '''
        produce the time elapsed since start_time
        '''
        return pygame.time.get_ticks() - self._start_time

    def update(self, screen):
        '''
        update the scene
        '''
        for node in self._scenegraph:
            node.update(screen)
        self.on_update()


class VideoSceneObject(object):
    '''
    a video object in the scene graph
    '''
    def __init__(self, resource, scaled=False, centered=False):
        '''
        constructor
        '''
        self._resource = resource
        self._scaled = scaled
        self._centered = centered
        self._elapsed = 0
        self._frame = next(resource.frames)

    def update(self, screen):
        '''
        update the video on screen
        '''
        if self._elapsed == 0:
            self._resource.audio.play()

        self._elapsed += screen.clock.get_time()
        if self._elapsed >= 1000.0 / self._resource.fps:
            self._elapsed -= 1000.0 / self._resource.fps
            self._frame = next(self._resource.frames)

        surface = self._frame
        rect = Rect(*self._frame.get_size())

        if self._scaled:
            rect = rect.scaled_to(screen.size)
            surface = pygame.transform.smoothscale(surface, rect.size)
        if self._centered:
            rect = rect.centered_in(screen.size)

        screen.blit(surface, rect.offset)


class ImageSceneObject(object):
    '''
    an image object in the scene graph
    '''
    def __init__(self, resource, pos=(0, 0)):
        '''
        constructor
        '''
        self._resource = resource
        self._pos = pos

    def update(self, screen):
        '''
        update the image on screen
        '''
        screen.blit(self._resource.frame, self._pos)


class AnimationSceneObject(object):
    '''
    an animated image object in the scene graph
    '''
    def __init__(self, resource, pos=(0, 0)):
        '''
        constructor
        '''
        self._resource = resource
        self._pos = pos
        self._elapsed = 0
        self._frame = next(resource.frames)

    def update(self, screen):
        '''
        update the animated image on screen
        '''
        self._elapsed += screen.clock.get_time()
        if self._elapsed >= 1000.0 / self._resource.fps:
            self._elapsed -= 1000.0 / self._resource.fps
            self._frame = next(self._resource.frames)

        screen.blit(self._frame, self._pos)
