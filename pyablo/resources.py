'''
This module provides game resource handling used by pyablo
'''

import mpq
from pyablo.video import Video
from pyablo.image import Image


_ERROR_UNITIALIZED = 'Resources.open called, but resource store uninitialized.'
_ERROR_OPEN_FAILED = 'unable to open resources file - incomplete installation?'


_NAMED_RESOURCES = {
    # video files
    'intro_logos.smk':          'File00002910.smk',
    'intro_cinematic.smk':      'File00001475.smk',
    # image files
    'intro_splash.pcx':         'File00000000.pcx',
    'logo_flames_large.pcx':    'File00000019.pcx',
    'logo_flames_medium.pcx':   'File00000022.pcx',
    'logo_flames_small.pcx':    'File00000034.pcx',
    'cursor.pcx':               'File00002905.pcx',
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
    def _open(cls, resource):
        '''
        return the queried resource as a file-like object
        '''
        if resource in _NAMED_RESOURCES:
            resource = _NAMED_RESOURCES[resource]

        try:
            return cls._mpq.open(resource)
        except AttributeError as ex:
            raise ValueError(_ERROR_UNITIALIZED) from ex

    @classmethod
    def open(cls, resource):
        '''
        return the queried resource as a game object
        '''
        res = cls._open(resource)

        if resource.endswith('.smk'):
            return Video(res)
        elif resource.endswith('.pcx'):
            return Image(res)
        return res
