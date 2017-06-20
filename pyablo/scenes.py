'''
This module defines the scenes used in pyablo
'''

import pygame
from pyablo.resources import Resources
from pyablo.game import Game


class Scene(object):
    '''
    a scene in the scene stack
    '''
    def __init__(self):
        '''
        constructor
        '''
        self._children = list()
        self._cursor_visible = True

    def on_event(self, event):
        '''
        invoke the event callback if present
        '''
        pass

    def on_pause(self):
        '''
        invoke the pause callback if present
        '''
        pass

    def on_resume(self):
        '''
        invoke the resume callback if present
        '''
        Game.screen.cursor.visible = self._cursor_visible
        Game.screen.surface.fill((0, 0, 0))

        for child in self._children:
            child.redraw = True

    def on_update(self):
        '''
        invoke the update callback if present
        '''
        pass

    def on_stop(self):
        '''
        invoke the stop callback if present
        '''
        pass

    def add_child(self, drawable, pos=(0, 0)):
        '''
        add a drawable to the scenegraph
        '''
        drawable.rect.topleft = pos
        drawable.parent = self
        drawable.redraw = 1

        self._children.append(drawable)

    def update(self):
        '''
        update the scene
        '''
        self.on_update()

        dirty = []
        for child in self._children:
            dirty.extend(child.update())

        for rect in dirty:
            Game.screen.surface.fill((0, 0, 0), rect)

        for child in self._children:
            redraw = [rect.clip(child.rect) for rect in dirty if rect.collideswith(child.rect)]
            child.draw(Game.screen.surface, redraw)


class CutScene(Scene):
    '''
    show the blizzard logos
    '''
    def __init__(self, resource):
        '''
        constructor
        '''
        super(CutScene, self).__init__()

        cutscene = Resources.open(resource)
        cutscene.rect = cutscene.rect.fit(Game.screen.surface.get_rect())

        self.add_child(cutscene)
        self._cursor_visible = False

    def on_event(self, event):
        '''
        event callbacks
        '''
        super(CutScene, self).on_event(event)

        if (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE or
                event.type == pygame.MOUSEBUTTONDOWN):
            raise StopIteration

    def on_stop(self):
        '''
        finish callback
        '''
        super(CutScene, self).on_stop()

        pygame.mixer.stop()


class IntroSplashScene(Scene):
    '''
    show the intro splash screen
    '''
    def __init__(self):
        '''
        constructor
        '''
        super(IntroSplashScene, self).__init__()

        background = Resources.open('intro_splash.pcx')
        background.add_child(Resources.open('logo_flames_large.pcx'), (45, 182))

        self.add_child(background)
        self._cursor_visible = False

        self._timer_start = None

    def on_event(self, event):
        '''
        event callbacks
        '''
        super(IntroSplashScene, self).on_event(event)

        if (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE or
                event.type == pygame.MOUSEBUTTONDOWN):
            raise StopIteration

    def on_resume(self):
        '''
        resume callback
        '''
        super(IntroSplashScene, self).on_resume()

        self._timer_start = pygame.time.get_ticks()

    def on_update(self):
        '''
        update callback
        '''
        super(IntroSplashScene, self).on_update()

        if pygame.time.get_ticks() - self._timer_start > 10000:  # ms
            raise StopIteration


class MainMenuScene(Scene):
    '''
    show the main menu
    '''
    def __init__(self):
        '''
        constructor
        '''
        super(MainMenuScene, self).__init__()

        background = Resources.open('menu_background.pcx')
        background.add_child(Resources.open('logo_flames_medium.pcx'), (125, 0))

        self.add_child(background)
        self._timer_start = None

    def on_event(self, event):
        '''
        event callback
        '''
        super(MainMenuScene, self).on_event(event)

        if event.type in (pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self._timer_start = pygame.time.get_ticks()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Game.quit()

    def on_update(self):
        '''
        update callback
        '''
        super(MainMenuScene, self).on_update()

        if pygame.time.get_ticks() - self._timer_start > 20000:  # ms
            Game.scenes.push('CutScene', args=('intro_cinematic.smk',))

    def on_resume(self):
        '''
        resume callback
        '''
        super(MainMenuScene, self).on_resume()

        self._timer_start = pygame.time.get_ticks()
