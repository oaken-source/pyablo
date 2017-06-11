'''
This module provides game resource handling used by pyablo
'''

import mpq
from pyablo.video import Video
from pyablo.image import Image


_ERROR_UNITIALIZED = 'Resources.open called, but resource store uninitialized.'
_ERROR_OPEN_FAILED = 'unable to open resources file - incomplete installation?'


class Resource(object):
    '''
    simple helper class to keep track of resource properties
    '''
    def __init__(self, name, *args, **kwargs):
        '''
        constructor
        '''
        self._name = name
        self._args = args
        self._kwargs = kwargs

    @property
    def name(self):
        '''
        produce the resource name
        '''
        return self._name

    @property
    def args(self):
        '''
        produce the resource args
        '''
        return self._args

    @property
    def kwargs(self):
        '''
        produce the resource kwargs
        '''
        return self._kwargs


_NAMED_RESOURCES = {
    # videos
    'intro_logos.smk':          Resource('File00002910.smk', fps=15),
    'intro_cinematic.smk':      Resource('File00001475.smk', fps=15),
    # images
    'cursor.pcx':               Resource('File00002905.pcx', colorkey=(0, -1)),
    'glyph_xlarge_gold.pcx':    Resource('File00000017.pcx'),
    'glyph_xlarge_grey.pcx':    Resource('File00000018.pcx'),
    'glyph_large_gold.pcx':     Resource('File00000008.pcx'),
    'glyph_large_grey.pcx':     Resource('File00000009.pcx'),
    'glyph_medium_gold.pcx':    Resource('File00000011.pcx'),
    'glyph_medium_grey.pcx':    Resource('File00000012.pcx'),
    'glyph_small_gold.pcx':     Resource('File00000014.pcx'),
    'glyph_small_grey.pcx':     Resource('File00000015.pcx'),
    'intro_splash.pcx':         Resource('File00000000.pcx'),
    'logo_flames_large.pcx':    Resource('File00000019.pcx', colorkey=(0, 0), fps=20, count=15),
    'logo_flames_medium.pcx':   Resource('File00000022.pcx', colorkey=(0, 0), fps=20, count=15),
    'logo_flames_small.pcx':    Resource('File00000034.pcx', colorkey=(0, 0), fps=20, count=15),
    'menu_background.pcx':      Resource('File00000020.pcx'),
}


class Resources(object):
    '''
    Resource management static class
    '''
    _mpq = None

    @classmethod
    def load(cls, path):
        '''
        Load the game resources from the mpq file
        '''
        try:
            cls._mpq = mpq.MPQFile(path)
        except OSError as ex:
            raise OSError(_ERROR_OPEN_FAILED) from ex

    @classmethod
    def _open(cls, name):
        '''
        produce a resource from the given name
        '''
        try:
            return cls._mpq.open(name)
        except AttributeError as ex:
            raise ValueError(_ERROR_UNITIALIZED) from ex

    @classmethod
    def fopen(cls, name):
        '''
        return the queried resource as a file-like object
        '''
        resource = _NAMED_RESOURCES.get(name, Resource(name))
        return cls._open(resource.name)

    @classmethod
    def open(cls, name):
        '''
        return the queried resource as a game object
        '''
        resource = _NAMED_RESOURCES.get(name, Resource(name))
        data = cls._open(resource.name)

        if resource.name.endswith('.smk'):
            return Video(data, *resource.args, **resource.kwargs)
        elif resource.name.endswith('.pcx'):
            return Image(data, *resource.args, **resource.kwargs)
        return data
