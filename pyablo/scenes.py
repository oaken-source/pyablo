'''
This module defines the scenes used in pyablo
'''

import pygame
from pyablo.resources import Resources
from pyablo.scene import Scene, VideoSceneObject, ImageSceneObject, AnimationSceneObject


def intro_logos(screen):
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
        screen.scenes.push('intro_splash')
        screen.scenes.push('intro_cinematic')

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


def intro_splash(screen):
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

    def on_update(scene):
        '''
        update callback
        '''
        if scene.elapsed_time > 4000:  # ms
            raise StopIteration

    def on_stop(_scene):
        '''
        finish callback
        '''
        screen.scenes.push('main_menu')

    splash = Resources.open('intro_splash.pcx')
    logo = Resources.open('logo_flames_large.pcx', colorkey=(0, 0))
    logo.animate(fps=20, length=15)

    return Scene(
        [
            ImageSceneObject(splash),
            AnimationSceneObject(logo, pos=(45, 182)),
        ],
        on_event=on_event,
        on_update=on_update,
        on_stop=on_stop,
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

    return Scene(
        [
            ImageSceneObject(background),
        ],
        on_update=on_update,
        on_event=on_event,
        on_resume=on_resume)
