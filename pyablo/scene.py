'''
This module provides classes to manage the scene graph stack
'''

import importlib
from inspect import getmembers, isfunction
import pygame
from pygame import Rect
from pyablo.game import Game


class SceneStack(object):
    '''
    custom stack class for scenes
    '''
    def __init__(self, module):
        '''
        constructor
        '''
        self._scenedir = dict()
        self._stack = list()

        mod = importlib.import_module(module)
        for (name, value) in getmembers(mod, isfunction):
            self._scenedir[name] = value

    def push(self, value):
        '''
        push to the stack and invoke callbacks
        '''
        scene = self._scenedir[value]()

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
        self._scenegraph = scenegraph
        self._callbacks = {k: v for (k, v) in kwargs.items() if k.startswith('on_')}
        self._properties = {k: v for (k, v) in kwargs.items() if not k.startswith('on_')}

        self._start_time = pygame.time.get_ticks()

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
        Game.screen.cursor.visible = self._properties.get('cursor_visible', True)
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

    def update(self):
        '''
        update the scene
        '''
        self.on_update()

        dirty = self._scenegraph.update_tree()
        self._scenegraph.redraw_tree(Game.screen.surface, dirty)
        Game.screen.debug.dirty_frames.extend(dirty)


class SceneObject(object):
    '''
    a node in the scene graph
    '''
    def __init__(self):
        '''
        constructor
        '''
        self._rect = Rect(0, 0, 0, 0)
        self._last_rect = self._rect.copy()
        self._surface = None
        self._children = []
        self.parent = None
        self.dirty = 1

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

    @property
    def surface(self):
        '''
        produce the surface of the sceneobject
        '''
        return self._surface

    @surface.setter
    def surface(self, value):
        '''
        set the surface of the sceneobject
        '''
        self._surface = value
        self.dirty = 1

    def add_child(self, child, pos=None):
        '''
        add a child sceneobject
        '''
        if pos is not None:
            child.rect.topleft = pos

        child.dirty = 1
        child.parent = self
        self._children.append(child)

    def update(self):
        '''
        update method - to be overwritten by child sceneobjects
        '''
        pass

    def update_tree(self):
        '''
        update method
        '''
        self.update()

        dirty = []
        for child in self._children:
            dirty.extend(child.update_tree())

        if self.dirty:
            self.dirty = 0
            return [self.rect]
        return dirty

    def redraw(self, surface, rect):
        '''
        redraw method
        '''
        source = self.surface
        if self.rect.size != self.surface.get_size():
            source = pygame.transform.smoothscale(source, self.rect.size)

        source_rect = rect.move(-self.rect.left, -self.rect.top)
        surface.blit(source, rect.topleft, area=source_rect)

    def redraw_tree(self, surface, dirty):
        '''
        draw method
        '''
        for rect in dirty:
            if rect.colliderect(self.rect):
                self.redraw(surface, rect)

        for child in self._children:
            child.redraw_tree(surface, dirty)
