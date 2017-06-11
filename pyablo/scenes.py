'''
This module defines the scenes used in pyablo
'''

import pygame
from pyablo.resources import Resources
from pyablo.scene import Scene, VideoSceneObject, ImageSceneObject, AnimationSceneObject


def intro_logos(_screen):
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

    return Scene(
        [
            VideoSceneObject(Resources.open('intro_logos.smk'), scaled=True, centered=True)
        ],
        on_event=on_event,
        on_stop=on_stop,
        cursor_visible=False)


def intro_cinematic(_screen):
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

    return Scene(
        [
            VideoSceneObject(Resources.open('intro_cinematic.smk'), scaled=True, centered=True)
        ],
        on_event=on_event,
        on_stop=on_stop,
        cursor_visible=False)


def intro_splash(_screen):
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
        if scene.elapsed_time > 4000:  # ms
            raise StopIteration

    splash = Resources.open('intro_splash.pcx')
    logo = Resources.open('logo_flames_large.pcx')

    return Scene(
        [
            ImageSceneObject(splash),
            AnimationSceneObject(logo, pos=(45, 182)),
        ],
        on_event=on_event,
        on_resume=on_resume,
        on_update=on_update,
        cursor_visible=False)


def main_menu(screen):
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
        if scene.elapsed_time > 30000:  # ms
            screen.scenes.push('intro_cinematic')

    def on_resume(scene):
        '''
        resume callback
        '''
        scene.start_time = pygame.time.get_ticks()

    background = Resources.open('menu_background.pcx')
    logo = Resources.open('logo_flames_medium.pcx')

    return Scene(
        [
            ImageSceneObject(background),
            AnimationSceneObject(logo, pos=(125, 0)),
        ],
        on_update=on_update,
        on_event=on_event,
        on_resume=on_resume)
