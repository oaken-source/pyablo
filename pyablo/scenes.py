'''
This module defines the scenes used in pyablo
'''

import pygame
from pyablo.resources import Resources
from pyablo.scene import Scene
from pyablo.image import SolidColorImage
from pyablo.game import Game


def intro_logos():
    '''
    show the blizzard logos
    '''
    def on_event(_scene, event):
        '''
        event callbacks
        '''
        if (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE or
                event.type == pygame.MOUSEBUTTONDOWN):
            raise StopIteration

    def on_stop(_scene):
        '''
        finish callback
        '''
        pygame.mixer.stop()

    root = SolidColorImage(Game.screen.surface.get_size())
    video = Resources.open('intro_logos.smk')
    video.rect = video.rect.fit(Game.screen.surface.get_rect())
    root.add_child(video)

    return Scene(
        root,
        on_event=on_event,
        on_stop=on_stop,
        cursor_visible=False)


def intro_cinematic():
    '''
    show the game intro cinematic
    '''
    def on_event(_scene, event):
        '''
        event callbacks
        '''
        if (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE or
                event.type == pygame.MOUSEBUTTONDOWN):
            raise StopIteration

    def on_stop(_scene):
        '''
        stop callback
        '''
        pygame.mixer.stop()

    root = SolidColorImage(Game.screen.surface.get_size())
    video = Resources.open('intro_cinematic.smk')
    video.rect = video.rect.fit(Game.screen.surface.get_rect())
    root.add_child(video)

    return Scene(
        root,
        on_event=on_event,
        on_stop=on_stop,
        cursor_visible=False)


def intro_splash():
    '''
    show the intro splash screen
    '''
    def on_event(_scene, event):
        '''
        event callbacks
        '''
        if (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE or
                event.type == pygame.MOUSEBUTTONDOWN):
            raise StopIteration

    def on_resume(scene):
        '''
        resume callback
        '''
        scene.start_time = pygame.time.get_ticks()

    def on_update(scene):
        '''
        update callback
        '''
        if scene.elapsed_time > 10000:  # ms
            raise StopIteration

    root = Resources.open('intro_splash.pcx')
    root.add_child(Resources.open('logo_flames_large.pcx'), pos=(45, 182))

    return Scene(
        root,
        on_event=on_event,
        on_resume=on_resume,
        on_update=on_update,
        cursor_visible=False)


def main_menu():
    '''
    show the main menu
    '''
    def on_event(scene, event):
        '''
        event callback
        '''
        if event.type in (pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            scene.start_time = pygame.time.get_ticks()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            raise StopIteration

    def on_update(scene):
        '''
        update callback
        '''
        if scene.elapsed_time > 20000:  # ms
            Game.screen.scenes.push('intro_cinematic')

    def on_resume(scene):
        '''
        resume callback
        '''
        scene.start_time = pygame.time.get_ticks()

    root = Resources.open('menu_background.pcx')
    root.add_child(Resources.open('logo_flames_medium.pcx'), pos=(125, 0))

    return Scene(
        root,
        on_update=on_update,
        on_event=on_event,
        on_resume=on_resume)
